"""Feedback on cards (error reports, suggestions, proposed revisions) and general messages from the Kontakt page,
stored in SQLite. A general message has no card and no part.

Stdlib only, so the container is a plain python:alpine image with this file mounted.
nginx proxies /api/ here, so the site posts same-origin and needs no CORS.

  python3 server.py serve                 # HTTP on $FEEDBACK_ADDR (default :8080)
  python3 server.py list [--status new]   # JSON lines, newest first
  python3 server.py set ID STATUS         # new | done | rejected
  python3 server.py passwd                # new dashboard password -> line for the env file

The database path comes from $FEEDBACK_DB (default ./feedback.sqlite) or --db.
No IP addresses are stored; the rate limit keeps them in memory only.

Dashboard (user 2026-10-29): the site page /pripominky/ (site/src/pages/pripominky.astro) holds only a login form and
talks to /api/admin/ here: login checks the password against $FEEDBACK_ADMIN_HASH (from `passwd`) and sets a signed
session cookie, which the rows (feedback) and status changes need. Without the hash every /api/admin/ path is a 404.
"""
import argparse
import hashlib
import hmac
import json
import os
import re
import secrets
import sqlite3
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit

KINDS = {"error", "suggestion", "revision"}
GENERAL_KINDS = {"question", "error", "suggestion", "other"}
PARTS = {"card", "title", "rvp", "comment", "tools", "jobs", "numbers", "learn", "other"}
ROLES = {"", "pupil", "parent", "teacher", "other"}
STATUSES = {"new", "done", "rejected"}
SLUG = re.compile(r"^[a-z0-9-]{1,120}$")
LIMITS = {"text": 4000, "revision": 8000, "original": 8000, "contact": 200, "page": 300}
MAX_BODY = 32 * 1024
# Per client: at most RATE_N posts per RATE_WINDOW seconds. Globally: DAILY_CAP per day,
# so a flood can fill a day, never the disk.
RATE_N, RATE_WINDOW, DAILY_CAP = 10, 3600, 1000
# Dashboard: at most AUTH_FAILS wrong passwords per client and AUTH_FAILS_ALL in all per RATE_WINDOW (the client comes
# from X-Forwarded-For, which a client can fake; the total cap also bounds the scrypt work).
AUTH_FAILS, AUTH_FAILS_ALL = 10, 100
ADMIN_PATH = "/api/admin/"
SESSION_DAYS = 30

SCHEMA = """
PRAGMA journal_mode = WAL;
CREATE TABLE IF NOT EXISTS feedback (
  id         INTEGER PRIMARY KEY,
  created_at TEXT NOT NULL,
  card       TEXT NOT NULL,  -- '' for a general message from the Kontakt page
  page       TEXT NOT NULL DEFAULT '',
  kind       TEXT NOT NULL,
  part       TEXT NOT NULL,
  text       TEXT NOT NULL DEFAULT '',
  -- For a revision: the text as shown on the page when the form opened, and the proposed one.
  original   TEXT NOT NULL DEFAULT '',
  revision   TEXT NOT NULL DEFAULT '',
  role       TEXT NOT NULL DEFAULT '',
  contact    TEXT NOT NULL DEFAULT '',
  status     TEXT NOT NULL DEFAULT 'new'
);
CREATE INDEX IF NOT EXISTS feedback_card ON feedback(card);
"""


def connect(path):
    db = sqlite3.connect(path, check_same_thread=False, isolation_level=None)
    db.executescript(SCHEMA)
    return db


def clean(payload):
    """Validated row, or an error message. Strings are trimmed and length-checked, never rewritten."""
    if not isinstance(payload, dict):
        return None, "bad payload"
    s = {k: payload.get(k, "") for k in ("card", "page", "kind", "part", "text", "original", "revision", "role", "contact")}
    if any(not isinstance(v, str) for v in s.values()):
        return None, "bad field type"
    s = {k: v.strip() for k, v in s.items()}
    if s["card"]:
        if not SLUG.match(s["card"]):
            return None, "bad card"
        if s["kind"] not in KINDS or s["part"] not in PARTS:
            return None, "bad choice"
    elif s["kind"] not in GENERAL_KINDS or s["part"]:
        return None, "bad choice"
    if s["role"] not in ROLES:
        return None, "bad choice"
    for k, n in LIMITS.items():
        if len(s[k]) > n:
            return None, f"{k} too long"
    if s["kind"] == "revision" and not s["revision"]:
        return None, "empty revision"
    if s["kind"] != "revision" and not s["text"]:
        return None, "empty text"
    if s["kind"] != "revision":
        s["original"] = s["revision"] = ""
    return s, None


class Limiter:
    def __init__(self):
        self.lock = threading.Lock()
        self.hits = {}
        self.day, self.today = "", 0

    def allow(self, client):
        now = time.time()
        with self.lock:
            day = time.strftime("%Y-%m-%d")
            if day != self.day:
                self.day, self.today, self.hits = day, 0, {}
            recent = [t for t in self.hits.get(client, []) if now - t < RATE_WINDOW]
            if len(recent) >= RATE_N or self.today >= DAILY_CAP:
                self.hits[client] = recent
                return False
            self.hits[client] = recent + [now]
            self.today += 1
            return True


def hash_password(password):
    salt = secrets.token_bytes(16)
    key = hashlib.scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1)
    return f"scrypt${salt.hex()}${key.hex()}"


def check_password(password, stored):
    try:
        algo, salt, key = stored.split("$")
        got = hashlib.scrypt(password.encode(), salt=bytes.fromhex(salt), n=2**14, r=8, p=1)
    except ValueError:
        return False
    return algo == "scrypt" and hmac.compare_digest(got.hex(), key)


class Admin:
    """The dashboard's settings, its password check and its sessions. A session is a cookie holding an expiry time
    signed with a key derived from the password hash, so nothing is stored and a new password ends every session."""

    def __init__(self, pw_hash):
        self.hash = pw_hash
        self.key = hashlib.sha256(b"feedback-session\0" + pw_hash.encode()).digest()
        self.lock = threading.Lock()
        self.fails = {}

    def login(self, client, password):
        """A session token, False (wrong password) or None (too many wrong ones)."""
        now = time.time()
        with self.lock:
            self.fails = {k: [t for t in v if now - t < RATE_WINDOW] for k, v in self.fails.items()}
            self.fails = {k: v for k, v in self.fails.items() if v}
            if len(self.fails.get(client, [])) >= AUTH_FAILS or sum(map(len, self.fails.values())) >= AUTH_FAILS_ALL:
                return None
        if isinstance(password, str) and password and check_password(password, self.hash):
            return self.sign(int(now) + SESSION_DAYS * 86400)
        with self.lock:
            self.fails.setdefault(client, []).append(now)
        return False

    def sign(self, expires):
        return f"{expires}.{hmac.new(self.key, str(expires).encode(), 'sha256').hexdigest()}"

    def valid(self, cookie_header):
        for part in (cookie_header or "").split(";"):
            name, _, token = part.strip().partition("=")
            if name == "fb_session":
                expires, _, _ = token.partition(".")
                if expires.isdigit() and int(expires) > time.time() and hmac.compare_digest(token, self.sign(int(expires))):
                    return True
        return False

    def cookie(self, token, max_age):
        return f"fb_session={token}; Path={ADMIN_PATH}; Max-Age={max_age}; HttpOnly; Secure; SameSite=Strict"


def make_handler(db, limiter, admin=None):
    lock = threading.Lock()

    class Handler(BaseHTTPRequestHandler):
        server_version = "feedback"

        def reply(self, code, body, cookie=None):
            data = json.dumps(body).encode()
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            if cookie:
                self.send_header("Set-Cookie", cookie)
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("Referrer-Policy", "no-referrer")
            self.end_headers()
            self.wfile.write(data)

        def client(self):
            return (self.headers.get("X-Forwarded-For") or self.client_address[0]).split(",")[0].strip()

        def body(self):
            """Parsed JSON body, or None after replying with the error."""
            n = int(self.headers.get("Content-Length") or 0)
            if n <= 0 or n > MAX_BODY:
                self.reply(413, {"error": "too large"})
                return None
            try:
                return json.loads(self.rfile.read(n))
            except ValueError:
                self.reply(400, {"error": "bad json"})
                return None

        def admin_route(self):
            """None when the path is not the dashboard's, else the rest of the path after /api/admin/."""
            path = urlsplit(self.path).path
            return path[len(ADMIN_PATH):] if admin and path.startswith(ADMIN_PATH) else None

        def signed_in(self):
            if admin.valid(self.headers.get("Cookie")):
                return True
            self.reply(401, {"error": "login"})
            return False

        def do_GET(self):
            if self.path == "/api/healthz":
                return self.reply(200, {"ok": True})
            route = self.admin_route()
            if route == "feedback" and self.signed_in():
                cur = db.cursor()
                cur.row_factory = sqlite3.Row
                return self.reply(200, [dict(r) for r in cur.execute("SELECT * FROM feedback ORDER BY id DESC")])
            if route != "feedback":
                self.reply(404, {"error": "not found"})

        def do_POST(self):
            route = self.admin_route()
            if route in ("login", "logout", "status"):
                # Only the dashboard's own script sends this header; a form on another site cannot (CSRF). The
                # cookie is SameSite=Strict as well.
                if self.headers.get("X-Feedback-Admin") != "1":
                    return self.reply(403, {"error": "forbidden"})
            if route == "login":
                payload = self.body()
                if payload is None:
                    return
                token = admin.login(self.client(), payload.get("password") if isinstance(payload, dict) else None)
                if token is None:
                    return self.reply(429, {"error": "slow down"})
                if not token:
                    return self.reply(401, {"error": "wrong password"})
                return self.reply(200, {"ok": True}, admin.cookie(token, SESSION_DAYS * 86400))
            if route == "logout":
                return self.reply(200, {"ok": True}, admin.cookie("", 0))
            if route == "status":
                if not self.signed_in():
                    return
                payload = self.body()
                if payload is None:
                    return
                fid, status = (payload.get("id"), payload.get("status")) if isinstance(payload, dict) else (None, None)
                if not isinstance(fid, int) or status not in STATUSES:
                    return self.reply(400, {"error": "bad choice"})
                with lock:
                    n = db.execute("UPDATE feedback SET status = ? WHERE id = ?", (status, fid)).rowcount
                return self.reply(200 if n else 404, {"ok": bool(n)})
            if route is not None or self.path != "/api/feedback":
                return self.reply(404, {"error": "not found"})
            payload = self.body()
            if payload is None:
                return
            # Honeypot: a field people never see. Bots that fill it get a quiet "ok".
            if isinstance(payload, dict) and payload.get("web"):
                return self.reply(201, {"ok": True})
            row, err = clean(payload)
            if err:
                return self.reply(400, {"error": err})
            if not limiter.allow(self.client()):
                return self.reply(429, {"error": "slow down"})
            row["created_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
            cols = ", ".join(row)
            with lock:
                cur = db.execute(f"INSERT INTO feedback ({cols}) VALUES ({', '.join('?' * len(row))})", list(row.values()))
            self.reply(201, {"ok": True, "id": cur.lastrowid})

        def log_message(self, fmt, *args):
            # Request lines only (method, path, status); never the client address.
            sys.stderr.write("%s %s\n" % (time.strftime("%Y-%m-%d %H:%M:%S"), fmt % args))

    return Handler


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=os.environ.get("FEEDBACK_DB", "feedback.sqlite"))
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("serve")
    ls = sub.add_parser("list")
    ls.add_argument("--status", choices=sorted(STATUSES))
    st = sub.add_parser("set")
    st.add_argument("id", type=int)
    st.add_argument("status", choices=sorted(STATUSES))
    sub.add_parser("passwd")
    args = ap.parse_args()
    if args.cmd == "passwd":
        password = secrets.token_urlsafe(15)
        print(f"password: {password}\nFEEDBACK_ADMIN_HASH={hash_password(password)}")
        return
    db = connect(args.db)

    if args.cmd == "serve":
        host, _, port = os.environ.get("FEEDBACK_ADDR", ":8080").rpartition(":")
        pw_hash = os.environ.get("FEEDBACK_ADMIN_HASH", "")
        admin = Admin(pw_hash) if pw_hash else None
        srv = ThreadingHTTPServer((host, int(port)), make_handler(db, Limiter(), admin))
        print(f"feedback: listening on {host or '*'}:{port}, db {args.db}, dashboard {'on' if admin else 'off'}",
              file=sys.stderr, flush=True)
        srv.serve_forever()
    elif args.cmd == "list":
        db.row_factory = sqlite3.Row
        q, p = "SELECT * FROM feedback", []
        if args.status:
            q, p = q + " WHERE status = ?", [args.status]
        for r in db.execute(q + " ORDER BY id DESC", p):
            print(json.dumps(dict(r), ensure_ascii=False))
    elif args.cmd == "set":
        if db.execute("UPDATE feedback SET status = ? WHERE id = ?", (args.status, args.id)).rowcount == 0:
            sys.exit(f"no feedback with id {args.id}")


if __name__ == "__main__":
    main()
