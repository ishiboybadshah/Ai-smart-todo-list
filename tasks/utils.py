import requests
import re
from decouple import config

def get_priority_from_ai(title, description):
    api_key = config("DEEPINFRA_API_KEY")

    url = "https://api.deepinfra.com/v1/openai/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "messages": [
            {
                "role": "system",
                "content": "You are an assistant that classifies task priority as High, Medium, or Low."
            },
            {
                "role": "user",
                "content": f"""Given this task:

                Title: {title}
                Description: {description}

                Classify the priority. Respond with ONLY one word: High, Medium, or Low."""
                            }
                        ],
                        "temperature": 0.3
                    }

    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    raw_response = result['choices'][0]['message']['content']
    print("🔎 AI Raw Response:", raw_response)

    match = re.search(r"\b(High|Medium|Low)\b", raw_response, re.IGNORECASE)
    priority = match.group(1).capitalize() if match else "Low"

    return priority
