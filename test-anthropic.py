"""Test an Anthropic API key and check which models respond.

Usage:
    pip install anthropic
    export ANTHROPIC_API_KEY=sk-ant-...
    python test_claude_key.py            # tests every model the key can see
    python test_claude_key.py claude-haiku-5-5 claude-sonnet-5-5   # test specific ones
"""
import os
import sys
import time

import anthropic
from dotenv import load_dotenv

#Load environment variables from .env file if it exists
load_dotenv()

api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    sys.exit("ANTHROPIC_API_KEY is not set.")

client = anthropic.Anthropic(api_key=api_key)

# 1. Does the key authenticate at all?
try:
    available = [m.id for m in client.models.list()]
    print(f"Key OK. {len(available)} model(s) visible.")
except anthropic.AuthenticationError as e:
    sys.exit(f"Key rejected: {e.message}")
except anthropic.APIError as e:
    sys.exit(f"API error on auth check: {e}")

# 2. Which models actually answer a request?
models = sys.argv[1:] or available
print(f"\n{'model':40} {'status':10} {'latency':>8}")
print("-" * 60)

for model in models:
    start = time.time()
    try:
        resp = client.messages.create(
            model=model,
            max_tokens=5,
            messages=[{"role": "user", "content": "Reply with OK."}],
        )
        text = " ".join(
            b.text for b in resp.content if getattr(b, "type", "") == "text"
        ).strip()
        status = "working"
        note = f'"{text}"'
    except anthropic.NotFoundError:
        status, note = "not found", "model id unknown or not enabled"
    except anthropic.PermissionDeniedError:
        status, note = "no access", "key lacks permission for this model"
    except anthropic.RateLimitError:
        status, note = "rate-limit", "key works; slow down or raise limits"
    except anthropic.BadRequestError as e:
        status, note = "bad req", e.message
    except anthropic.APIError as e:
        status, note = "error", str(e)
    ms = int((time.time() - start) * 1000)
    print(f"{model:40} {status:10} {ms:>6}ms  {note}")