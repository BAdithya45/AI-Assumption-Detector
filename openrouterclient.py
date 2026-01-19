import os
import httpx
import json
from typing import Any


OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "google/gemma-3-1b-it:free"
TIMEOUT = 60
MAX_RETRIES = 2


def get_api_key() -> str:
    key = os.environ.get("OPENROUTER_API_KEY", "")
    if not key:
        raise ValueError("OPENROUTER_API_KEY environment variable is not set")
    return key


def get_model() -> str:
    return os.environ.get("OPENROUTER_MODEL", DEFAULT_MODEL)


def build_headers(apikey: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {apikey}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://assumption-detector.app",
        "X-Title": "Assumption Detector"
    }


def build_payload(messages: list[dict], model: str) -> dict[str, Any]:
    return {
        "model": model,
        "messages": messages,
        "temperature": 0.3,
        "max_tokens": 2000
    }


def call(messages: list[dict]) -> str:
    apikey = get_api_key()
    model = get_model()
    headers = build_headers(apikey)
    payload = build_payload(messages, model)
    
    last_error = None
    
    for attempt in range(MAX_RETRIES + 1):
        try:
            with httpx.Client(timeout=TIMEOUT) as client:
                response = client.post(OPENROUTER_URL, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()
                return extract_content(data)
        except httpx.TimeoutException as e:
            last_error = e
            continue
        except httpx.HTTPStatusError as e:
            if e.response.status_code >= 500:
                last_error = e
                continue
            raise ModelError(f"API error: {e.response.status_code}") from e
        except Exception as e:
            raise ModelError(f"Unexpected error: {str(e)}") from e
    
    raise ModelError(f"Failed after {MAX_RETRIES + 1} attempts: {last_error}")


def extract_content(data: dict) -> str:
    choices = data.get("choices", [])
    if not choices:
        raise ModelError("No response from model")
    message = choices[0].get("message", {})
    content = message.get("content", "")
    if not content:
        raise ModelError("Empty response from model")
    return content


class ModelError(Exception):
    pass
