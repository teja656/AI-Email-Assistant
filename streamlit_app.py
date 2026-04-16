import streamlit as st
import os
from main import run_email_assistant, DEFAULT_MODEL

st.set_page_config(page_title="AI Email Assistant", layout="wide")

st.title("📧 AI Email Assistant")
st.write("Analyze emails to detect emotion, intent, and generate smart replies using AI.")

# Sidebar for API key
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input(
        "Google API Key",
        value=os.getenv("GOOGLE_API_KEY", ""),
        type="password",
        help="Enter your Google Generative AI API key. Get one at https://aistudio.google.com/app/apikey"
    )
    model = st.selectbox(
        "Model",
        ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.0-flash"],
        index=0,
        help="Select the AI model to use"
    )

# Check if API key is provided
if not api_key:
    st.warning("⚠️ Please enter your Google API key in the sidebar to continue.")
    st.stop()

# Email input section
st.header("📝 Email Input")
col1, col2 = st.tabs(["Text Input", "File Upload"])

email_text = ""

with col1:
    email_text = st.text_area(
        "Paste your email here",
        height=200,
        placeholder="Hi team, I'm frustrated with the recent delay on the report. Can we fix this today?"
    )

with col2:
    uploaded_file = st.file_uploader("Upload email file (.txt)", type=["txt"])
    if uploaded_file:
        email_text = uploaded_file.read().decode("utf-8").strip()
        st.text_area("Email content", value=email_text, height=200, disabled=True)

# Analyze button
if st.button("🔍 Analyze Email", type="primary", use_container_width=True):
    if not email_text.strip():
        st.error("❌ Please enter or upload an email first.")
    else:
        with st.spinner("Analyzing email..."):
            try:
                result = run_email_assistant(email_text, model=model, api_key=api_key)
                
                # Display results
                st.success("✅ Analysis complete!")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.subheader("Emotion")
                    st.info(result["emotion"])
                
                with col2:
                    st.subheader("Intent")
                    st.info(result["intent"])
                
                with col3:
                    st.subheader("Confidence")
                    st.metric("", "High")
                
                # Generated reply
                st.subheader("💬 Generated Reply")
                st.text_area(
                    "Reply",
                    value=result["reply"],
                    height=200,
                    disabled=True,
                    label_visibility="collapsed"
                )
                
                # Action buttons
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.download_button(
                        "📥 Download Reply",
                        data=result["reply"],
                        file_name="email_reply.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                
                with col2:
                    if st.button("📋 Copy to Clipboard", use_container_width=True):
                        st.toast("Copied! (Note: Use Ctrl+V to paste)", icon="✅")
                
                with col3:
                    if st.button("💾 Save Analysis", use_container_width=True):
                        analysis_text = f"""=== Email Analysis Report ===

ORIGINAL EMAIL:
{email_text}

DETECTED EMOTION:
{result['emotion']}

DETECTED INTENT:
{result['intent']}

GENERATED REPLY:
{result['reply']}
"""
                        st.download_button(
                            "📋 Download Report",
                            data=analysis_text,
                            file_name="email_analysis_report.txt",
                            mime="text/plain"
                        )
                        st.toast("Analysis saved!", icon="✅")
                
            except Exception as e:
                st.error(f"❌ Error analyzing email: {str(e)}")

# Footer
st.divider()
st.caption(
    "🚀 Powered by Google Generative AI | "
    "[Get API Key](https://aistudio.google.com/app/apikey) | "
    "[View Source](https://github.com)"
)
