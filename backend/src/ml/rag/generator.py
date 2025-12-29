import requests

from src.config import settings

API_URL = "https://router.huggingface.co/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {settings.HUGGINGFACE_KEY}",
    "Content-Type": "application/json",
}


def generate_answer(context, query):
    system_prompt = (
        "You are a friendly and caring assistant"
        "who responds based on the provided context."
        "You aim to explain things thoroughly,"
        "using examples and helpful advice to make the answer clear and reassuring."
        "If the information is insufficient, be honest about it — "
        "but still try to help as much as you can."
    )

    user_prompt = f"Context:\n{context}\n\nQuestion: {query}\n\nAnswer:"

    payload = {
        "model": "mistralai/Mistral-7B-Instruct-v0.2:featherless-ai",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.5,
        "max_tokens": 512,
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()
