import streamlit as st
import hashlib
import hmac
import json
import math

def heading(title, intro):
    st.title(title)
    st.write(intro)
    st.divider()

def explain(title, body):
    with st.expander(title, expanded=False):
        st.markdown(body)

def learning_check(question, options, correct_index, explanation, key):
    choice = st.radio(question, options, index=None, key=key)
    if st.button("Check answer", key=key + "_check"):
        if choice is None:
            st.info("Choose an answer first.")
        elif options.index(choice) == correct_index:
            st.success("Correct! " + explanation)
        else:
            st.error("Not quite. " + explanation)

def progress_note():
    st.caption("Teaching note: use the explanation first, then change the inputs, predict the output, and finally run the lab.")

def sha256_hex(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def hmac_hex(message, key):
    return hmac.new(key.encode("utf-8"), message.encode("utf-8"), hashlib.sha256).hexdigest()

def is_prime(n):
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True

def egcd(a, b):
    if b == 0:
        return (a, 1, 0)
    g, x1, y1 = egcd(b, a % b)
    return (g, y1, x1 - (a // b) * y1)

def mod_inverse(a, m):
    g, x, _ = egcd(a, m)
    return x % m if g == 1 else None

def modular_power(base, exponent, modulus):
    return pow(base, exponent, modulus)

def quiz_table():
    st.caption("End-of-unit check: answer before opening the explanation.")


def further_learning_resources(title, resources):
    """Display topic-aligned external reading links at the end of a learning unit."""
    st.divider()
    st.subheader("🔎 For more, you can visit here")
    st.caption("Curated external reading to go deeper into the topics covered in this unit. Opens in a new browser tab.")
    with st.container(border=True):
        st.markdown(f"**{title} — further learning**")
        for label, url, note in resources:
            st.markdown(f"- [{label}]({url}) — {note}")
