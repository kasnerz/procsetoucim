// Shared by the two forms that post to the feedback service (feedback/server.py, proxied at /api/ by nginx):
// "Připomínka ke kartě" (components/Feedback.astro) and the Kontakt page (components/ContactForm.astro).

export const FEEDBACK_ENDPOINT = `${import.meta.env.BASE_URL}api/feedback`;

export const ROLES = [
  { id: "pupil", label: "Žák nebo žákyně" },
  { id: "parent", label: "Rodič" },
  { id: "teacher", label: "Učitel nebo učitelka" },
  { id: "other", label: "Někdo jiný" },
];

/** Posts one message; resolves to nothing when it was stored, or rejects with the message to show. */
export async function sendFeedback(endpoint: string, body: Record<string, unknown>): Promise<void> {
  let r: Response;
  try {
    r = await fetch(endpoint, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
  } catch {
    r = new Response(null, { status: 503 });
  }
  if (r.status === 429) throw new Error("Odsud už toho teď přišlo hodně. Zkus to znovu za hodinu.");
  if (!r.ok) throw new Error("Odeslání se nepovedlo. Zkus to prosím znovu za chvíli.");
}
