import axios from "axios";

export async function askAssistant(question) {
  const response = await fetch("/rag", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });
  return response.json();
}
