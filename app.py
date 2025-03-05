import streamlit as st
import string
import re
import pandas as pd
from io import BytesIO

# Function to Check Password Strength
def check_strength(password):
    length = len(password)
    has_digits = any(char.isdigit() for char in password)
    has_special = any(char in string.punctuation for char in password)
    
    if length < 8:
        return "Weak", "🔴", "Increase password length to at least 8 characters.", 0.3
    elif length < 12 or (not has_digits or not has_special):
        return "Moderate", "🟡", "Try adding numbers & special characters.", 0.6
    else:
        return "Strong", "🟢", "Your password is strong! 🎉", 1.0
    

# Function to Download Password as CSV
def download_password_csv(password):
    df = pd.DataFrame([[password]], columns=["Password"])
    output = BytesIO()
    df.to_csv(output, index=False)
    output.seek(0)
    return output


# Streamlit UI
st.title("🔐 Password Strength Meter")
if "password" not in st.session_state:
    st.session_state.password = ""
if "password_visibility" not in st.session_state:
    st.session_state.password_visibility = False

# Toggle Eye Button for Password Visibility
password = st.text_input("Enter Your Password", value=st.session_state.password, key="password_input", type="password" if not st.session_state.password_visibility else "default")

if st.button("👁 Toggle Password Visibility"):
    st.session_state.password_visibility = not st.session_state.password_visibility
    st.rerun()

if st.button("🔍 Analyze Password"):
    if password:
        strength, color, tip, progress = check_strength(password)
        st.markdown(f"### {color} **Password Strength: {strength}**")
        st.progress(progress)
        st.info(tip)

        st.markdown("---")
        csv = download_password_csv(password)
        st.download_button(label="📂 Download as CSV", data=csv, file_name="password.csv", mime="text/csv")
        
    else:
        st.warning("⚠️ Please enter a password to analyze.")
        if st.button("🔄 Reset Password Field"):
            st.session_state.password = ""
            st.session_state.password_visibility = False
            st.rerun()
        
st.write("----------------------------------------------------------------")
st.write("Build with 💖 by [Faria Mustaqim](https://github.com/Zaibunis)")
