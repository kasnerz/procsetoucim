#!/bin/sh
# Rebuild content + site and publish it as the version in progress: https://procsetoucim.internal.quxt.eu (tailnet
# only). The public https://procsetoucim.cz changes only with scripts/release.sh (user 2026-10-25).
# nginx serves /opt/stacks/procsetoucim/site-staging directly; no container restart needed.
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
STACK=/opt/stacks/procsetoucim
cd "$ROOT/pipeline" && uv run python -I build_all.py
cd "$ROOT/site" && npx astro build
rsync -a --delete "$ROOT/site/dist/" "$STACK/site-staging/"
# Feedback service (shared by both builds): copy the source; restart only when it changed.
mkdir -p "$STACK/feedback" "$STACK/data"
if ! cmp -s "$ROOT/feedback/server.py" "$STACK/feedback/server.py"; then
  cp "$ROOT/feedback/server.py" "$STACK/feedback/server.py"
  docker restart procsetoucim-feedback >/dev/null 2>&1 || echo "feedback: run 'docker compose up -d' in $STACK"
fi
echo "deployed (in progress): https://procsetoucim.internal.quxt.eu/"
echo "to make it public: scripts/release.sh"
