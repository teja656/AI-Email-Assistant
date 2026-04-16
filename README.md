# AI Email Assistant

This mini project is an AI-powered email assistant that:
- Detects the sender's emotion
- Understands the sender's intent
- Generates a smart reply using prompt chaining

## Setup

1. Create and activate a Python environment:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

2. Set your Google Generative AI API key:
   ```powershell
   $env:GOOGLE_API_KEY = "your_api_key_here"
   ```

## Run

### Web UI (Streamlit)
```powershell
streamlit run streamlit_app.py
```
Then paste your email text or upload a file, and the app will display emotion, intent, and a generated reply.

### Command Line
```powershell
python main.py --email-text "Hi team, I'm frustrated with the recent delay on the report. Can we fix this today?"
```

You can also read the email from a file:

```powershell
python main.py --email-file sample-email.txt
```

## Project structure

- `main.py` - prompt chaining workflow and runtime entrypoint
- `requirements.txt` - Python dependency list
