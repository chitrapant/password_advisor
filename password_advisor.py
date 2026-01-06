import streamlit as st
import math
import string

# Function to estimate password entropy
def calculate_entropy(password):
    charset_size = 0
    if any(c.islower() for c in password):
        charset_size += 26
    if any(c.isupper() for c in password):
        charset_size += 26
    if any(c.isdigit() for c in password):
        charset_size += 10
    if any(c in string.punctuation for c in password):
        charset_size += len(string.punctuation)
    if charset_size == 0:
        return 0
    entropy = len(password) * math.log2(charset_size)
    return entropy

# Function to estimate time to crack (in years)
def time_to_crack(entropy, guesses_per_second=1e10):
    total_guesses = 2 ** entropy
    seconds = total_guesses / guesses_per_second
    years = seconds / (60 * 60 * 24 * 365)
    return years

# Function to give password suggestions
def suggest_password(password):
    suggestions = []
    if not any(c.isupper() for c in password):
        suggestions.append("Add uppercase letters")
    if not any(c.islower() for c in password):
        suggestions.append("Add lowercase letters")
    if not any(c.isdigit() for c in password):
        suggestions.append("Add numbers")
    if not any(c in string.punctuation for c in password):
        suggestions.append("Add special characters (!@#$...)")
    if len(password) < 12:
        suggestions.append("Increase password length to 12+ characters")
    return suggestions

# Streamlit UI
st.title("🔒 Adaptive Password Strength Advisor")

password = st.text_input("Enter your password", type="password")

if password:
    entropy = calculate_entropy(password)
    years = time_to_crack(entropy)

    st.subheader("Password Analysis")
    st.write(f"**Entropy:** {entropy:.2f} bits")
    st.write(f"**Estimated time to crack:** {years:.2e} years")

    # Strength indicator
    if years > 1e6:
        st.success("Strong password ✅")
    elif years > 1e3:
        st.warning("Moderate password ⚠️")
    else:
        st.error("Weak password ❌")

    # Suggestions
    suggestions = suggest_password(password)
    if suggestions:
        st.subheader("Suggestions to Improve Password")
        for s in suggestions:
            st.write(f"- {s}")
