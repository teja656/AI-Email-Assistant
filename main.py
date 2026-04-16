import argparse
import os
import sys
from typing import Dict

import google.generativeai as genai

DEFAULT_MODEL = "gemini-2.5-flash"


def get_google_api_key() -> str:
    api_key = os.getenv("")
    if not api_key:
        raise EnvironmentError(
            "GOOGLE_API_KEY is not set. Set it in your environment before running the script."
        )
    return api_key


def create_chat_completion(prompt: str, model: str = DEFAULT_MODEL) -> str:
    model_obj = genai.GenerativeModel(model_name=model)
    chat = model_obj.start_chat()
    response = chat.send_message(prompt)
    return response.text.strip()


def detect_emotion(email_text: str, model: str) -> str:
    prompt = (
        "Read the email below and identify the sender's primary emotion. "
        "Reply with a single word or a short phrase such as: frustrated, happy, urgent, concerned, calm, appreciative.\n\n"
        f"Email:\n{email_text}\n"
    )
    return create_chat_completion(prompt, model=model)


def detect_intent(email_text: str, model: str) -> str:
    prompt = (
        "Read the email below and identify the sender's main intent. "
        "Use a concise phrase such as: request update, arrange meeting, escalate issue, ask for help, thank you, provide feedback.\n\n"
        f"Email:\n{email_text}\n"
    )
    return create_chat_completion(prompt, model=model)


def generate_reply(email_text: str, emotion: str, intent: str, model: str) -> str:
    prompt = (
        "Using the email content, detected emotion, and intent, craft a professional reply. "
        "The response should acknowledge the sender's feeling, confirm the intent, and provide a clear next step. "
        "Keep the tone respectful and helpful.\n\n"
        f"Email:\n{email_text}\n\n"
        f"Detected emotion: {emotion}\n"
        f"Detected intent: {intent}\n"
    )
    return create_chat_completion(prompt, model=model)


def run_email_assistant(email_text: str, model: str = DEFAULT_MODEL, api_key: str | None = None) -> Dict[str, str]:
    if api_key:
        genai.configure(api_key=api_key)
    emotion = detect_emotion(email_text, model=model)
    intent = detect_intent(email_text, model=model)
    reply = generate_reply(email_text, emotion, intent, model=model)
    return {
        "email": email_text,
        "emotion": emotion,
        "intent": intent,
        "reply": reply,
    }


def parse_args():
    parser = argparse.ArgumentParser(description="AI Email Assistant with prompt chaining")
    parser.add_argument("--email-text", help="Email content to analyze and respond to.")
    parser.add_argument("--email-file", help="Path to a text file containing the email.")
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help="Google generative AI model to use.",
    )
    parser.add_argument(
        "--api-key",
        help="Google API key (or set GOOGLE_API_KEY environment variable).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.email_file:
        if not os.path.exists(args.email_file):
            print(f"Error: File not found: {args.email_file}", file=sys.stderr)
            return 1
        with open(args.email_file, "r", encoding="utf-8") as f:
            email_text = f.read().strip()
    elif args.email_text:
        email_text = args.email_text.strip()
    else:
        print("Provide either --email-text or --email-file.", file=sys.stderr)
        return 1

    api_key = args.api_key or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "GOOGLE_API_KEY is not set. Pass it with --api-key or set GOOGLE_API_KEY environment variable."
        )
    genai.configure(api_key=api_key)

    print("Running AI Email Assistant...\n")
    result = run_email_assistant(email_text, model=args.model)

    print("Detected Emotion:", result["emotion"])
    print("Detected Intent:", result["intent"])
    print("\nGenerated Reply:\n")
    print(result["reply"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
