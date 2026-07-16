import sys
import os
import streamlit as st

# Add project root to sys.path to allow imports from app.telephony
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.telephony.twilio_client import TwilioClient
from app.telephony.config import TelephonyConfig

def main():
    st.set_page_config(page_title="Twilio Call Portal", page_icon="📞")
    st.title("📞 Twilio Call Trigger Portal")
    st.caption(f"From Number: {TelephonyConfig.FROM_NUMBER}")

    to_number = st.text_input("Enter Mobile Number", placeholder="e.g., +918760022251")
    call_button = st.button("📢 Make Call", type="primary")

    if call_button:
        if not to_number:
            st.error("⚠️ Please enter a valid mobile number.")
        else:
            with st.spinner("Initiating call..."):
                client = TwilioClient()
                result = client.make_call(to_number)

            if result.get("success"):
                st.success(f"✅ Call initiated successfully!")
                st.info(f"**Call SID:** `{result['call_sid']}`  \n**Status:** `{result['status']}`")
            else:
                st.error(f"❌ Failed to initiate call.")
                st.error(f"**Error:** `{result['error']}`")

if __name__ == "__main__":
    main()