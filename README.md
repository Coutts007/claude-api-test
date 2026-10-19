# Claude API Test

A small Python utility for checking whether an Anthropic API key is valid and which Claude models the key can access.

This repository is designed to help you quickly validate a key, detect which models are enabled for that account, and confirm that those models can successfully respond to a basic prompt.

## What it does

- Reads your `ANTHROPIC_API_KEY` from the environment or a `.env` file
- Authenticates against the Anthropic API
- Lists all models visible to the key
- Tests each available model with a simple prompt
- Reports whether each model is working, missing, unauthorised, rate-limited, or failing for another reason

## Repository contents

- `test-anthropic.py` — main validation script
- `requirements.txt` — Python dependencies
- `.gitignore` — excludes local virtual environments and environment files

## Requirements

- Python 3.10+
- An Anthropic API key
- Internet access to reach the Anthropic API

## Setup

1. Clone the repository:

```bash
git clone https://github.com/Coutts007/claude-api-test.git
cd claude-api-test
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
# or
venv\Scripts\activate      # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Add your API key.

You can either export it in your shell:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

Or create a `.env` file in the project root:

```env
ANTHROPIC_API_KEY=sk-ant-...
```

The script loads `.env` automatically using `python-dotenv`.

## Usage

Run the script with no arguments to test every model visible to the key:

```bash
python test-anthropic.py
```

Run it against specific models only:

```bash
python test-anthropic.py claude-haiku-5-5 claude-sonnet-5-5
```

## Example output

```text
Key OK. 5 model(s) visible.

model                                     status     latency  note
------------------------------------------------------------
claude-haiku-5-5                          working      420ms  "OK"
claude-sonnet-5-5                         working      580ms  "OK"
claude-opus-4-1                           no access  ...
claude-3-5-haiku-20241022                 not found ...
```

## What the statuses mean

- `working` — the model exists, is accessible, and answered the test prompt successfully.
- `not found` — the model ID is unknown or not enabled for the account.
- `no access` — the key has no permission for that model.
- `rate-limit` — the key works but has hit a request or rate limit.
- `bad req` — the request was rejected due to an invalid or unsupported request shape.
- `error` — another API-side error occurred.

## Scripts and behavior

The script performs a basic two-step check:

1. Authenticates by calling `client.models.list()`
2. Sends a short message to each model using `client.messages.create()` with `max_tokens=5`

This is intentionally lightweight so it can quickly tell you whether a key is valid and which models are usable.

## Troubleshooting

### `ANTHROPIC_API_KEY is not set.`

Make sure the environment variable is exported or present in `.env`.

### `Key rejected`

Check that the key is copied correctly and is valid for your Anthropic account.

### Some models say `not found` or `no access`

This usually means the model is not available for your account or your key does not have access to it.

### Rate limiting

The script will report a `rate-limit` status if the account is currently limited. Wait a bit and retry, or check your Anthropic account usage limits.

## Security notes

- Never commit your real API key to version control.
- Keep `.env` and any secret files out of Git history.
- The repository already includes `.env` in `.gitignore` to help reduce accidental exposure.

## License

This repository does not currently include a formal license file. If you plan to share or reuse it publicly, add an appropriate license before distribution.

## Contributing

Pull requests and improvements are welcome. For example, you could add:

- a richer CLI interface
- CSV/JSON reporting output
- model sorting and filtering
- support for testing multiple providers or fallback keys

## Notes

This project is intentionally simple and focused on quick API validation. It is best suited for local testing and debugging of Anthropic access and model availability.
