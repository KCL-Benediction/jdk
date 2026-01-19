import os
import time
from typing import Any, Dict, List, Optional

import requests


def call_deepseek_chat(
    deepseekModelEndpoint: str,
    messages: List[Dict[str, str]],
    *,
    api_key: Optional[str] = None,
    model: str = "deepseek-chat",
    temperature: float = 0.7,
    max_tokens: int = 512,
    timeout_s: int = 60,
    max_retries: int = 3,
) -> Dict[str, Any]:
    """
    Call a DeepSeek model via an OpenAI-compatible Chat Completions endpoint.

    Args:
        deepseekModelEndpoint: The full URL to the chat completions endpoint.
            Example:
              - "https://api.deepseek.com/v1/chat/completions"
              - or your gateway URL, as long as it accepts OpenAI-style payloads.
        messages: OpenAI-style messages, e.g.
            [{"role": "system", "content": "You are helpful."},
             {"role": "user", "content": "Hello!"}]
        api_key: API key for the endpoint. If None, read from env DEEPSEEK_API_KEY.
        model: Model name expected by the endpoint (varies by provider/gateway).
        temperature, max_tokens: Generation parameters.
        timeout_s: Per-request timeout.
        max_retries: Simple retry on transient failures (429/5xx/network).

    Returns:
        The decoded JSON response as a dict.

    Raises:
        requests.HTTPError: On non-retriable HTTP errors.
        ValueError: If endpoint returns non-JSON response.
    """
    api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise ValueError("Missing api_key. Pass api_key=... or set DEEPSEEK_API_KEY env var.")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        # Many OpenAI-compatible gateways accept this; safe to include.
        "Accept": "application/json",
    }

    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        # You can add more OpenAI-compatible fields if your endpoint supports them:
        # "top_p": 0.9,
        # "presence_penalty": 0.0,
        # "frequency_penalty": 0.0,
        # "stream": False,
    }

    last_err: Optional[Exception] = None

    for attempt in range(1, max_retries + 1):
        try:
            resp = requests.post(
                deepseekModelEndpoint,
                headers=headers,
                json=payload,
                timeout=timeout_s,
            )

            # Retry on rate-limit or server errors
            if resp.status_code in (429, 500, 502, 503, 504):
                # Backoff (simple exponential)
                wait_s = min(2 ** (attempt - 1), 8)
                time.sleep(wait_s)
                continue

            resp.raise_for_status()

            try:
                return resp.json()
            except Exception as e:
                raise ValueError(f"Endpoint returned non-JSON: {resp.text[:200]}") from e

        except Exception as e:
            last_err = e
            # Network-ish errors: retry a bit
            if attempt < max_retries:
                time.sleep(min(2 ** (attempt - 1), 8))
                continue
            raise

    # Shouldn't reach here, but just in case:
    raise RuntimeError("Request failed") from last_err


if __name__ == "__main__":
    # Example usage
    deepseekModelEndpoint = "https://api.deepseek.com/v1/chat/completions"  # <- replace with yours

    result = call_deepseek_chat(
        deepseekModelEndpoint,
        messages=[
            {"role": "system", "content": "You are a concise assistant."},
            {"role": "user", "content": "用一句话解释什么是向量数据库？"},
        ],
        model="deepseek-chat",   # <- adjust if your endpoint expects a different model name
        temperature=0.2,
        max_tokens=200,
    )

    # OpenAI-style response usually looks like: result["choices"][0]["message"]["content"]
    print(result["choices"][0]["message"]["content"])
