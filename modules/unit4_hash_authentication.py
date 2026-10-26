import streamlit as st
from modules.common import heading, explain, learning_check, sha256_hex, hmac_hex

def render():
    heading("Unit 4 — Hash functions and message authentication",
            "Experiment with SHA-256, avalanche behavior, message authentication codes (MACs), HMAC, and CMAC concepts.")
    tab1, tab2, tab3 = st.tabs(["Hash lab", "HMAC lab", "Concepts & quiz"])

    with tab1:
        st.subheader("SHA-256 fingerprint")
        message = st.text_area("Input message", "Cryptography protects information.", key="u4_hash")
        digest = sha256_hex(message)
        st.code(digest)
        st.caption(f"Digest length: {len(digest)*4} bits (SHA-256 always outputs 256 bits).")
        changed = st.text_input("Try a tiny change", message + "!", key="u4_changed")
        st.write("Changed digest")
        st.code(sha256_hex(changed))
        st.write("Digests equal:", digest == sha256_hex(changed))
        st.caption("A cryptographic hash is one-way by design; it is not encryption and has no decryption key.")
        explain("Hash properties",
                "- **Preimage resistance:** given a digest, finding an input is computationally infeasible.\n"
                "- **Second-preimage resistance:** given one input, finding a different input with the same digest is infeasible.\n"
                "- **Collision resistance:** finding any two distinct inputs with the same digest is infeasible.\n"
                "- **Avalanche effect:** a small input change should produce a substantially different digest.")
        explain("Password storage",
                "Do not store plain passwords or use a fast general-purpose hash alone. Use a dedicated password-hashing scheme such as Argon2id, scrypt, or bcrypt with a unique salt and suitable cost settings.")

    with tab2:
        st.subheader("HMAC-SHA-256 — keyed integrity/authentication")
        message = st.text_area("Message", "Transfer 100 rupees to account 123.", key="u4_hmac_message")
        secret = st.text_input("Shared secret for this demo", "demo-shared-secret", key="u4_hmac_key")
        tag = hmac_hex(message, secret)
        st.write("HMAC tag")
        st.code(tag)
        candidate = st.text_input("Message to verify", message, key="u4_hmac_candidate")
        candidate_tag = st.text_input("Tag to verify", tag, key="u4_hmac_tag")
        import hmac as hm
        if st.button("Verify HMAC", key="u4_hmac_verify"):
            expected = hmac_hex(candidate, secret)
            if hm.compare_digest(expected, candidate_tag.strip().lower()):
                st.success("Valid tag: message matches the shared secret.")
            else:
                st.error("Invalid tag: message or tag changed, or the secret is different.")
        st.caption("HMAC authenticates data for parties sharing a secret. It does not provide non-repudiation because either key holder can create a valid tag.")
        explain("CMAC",
                "CMAC is a block-cipher-based message authentication code, commonly based on AES. It provides integrity/authentication with a shared secret. HMAC is hash-based; CMAC is block-cipher-based. Both require correct key handling and protocol design.")

    with tab3:
        explain("Hash vs MAC vs encryption",
                "| Tool | Key? | Main purpose | Reversible? |\n|---|---:|---|---|\n| Hash | No | Fingerprint / integrity support | No |\n| MAC / HMAC / CMAC | Yes, shared secret | Integrity + data-origin authentication among key holders | No |\n| Encryption | Yes (or public/private keys) | Confidentiality | Intended to be reversible by authorized key holder |")
        learning_check("Which choice is best for authenticating a message between parties sharing a secret?",
                       ["SHA-256 alone", "HMAC-SHA-256", "Base64", "Caesar cipher"], 1,
                       "HMAC uses a secret key and a hash to authenticate messages.", "u4q1")
        learning_check("Can a SHA-256 digest normally be decrypted to recover the message?",
                       ["Yes, with the public key", "Yes, with the same hash", "No, hashing is not encryption", "Only when the message is short"], 2,
                       "Hash functions are one-way; they do not provide decryption.", "u4q2")

    from modules.common import further_learning_resources
    further_learning_resources("Hash functions and message authentication", [
        ("NIST: Secure Hash Standard (SHS)", "https://csrc.nist.gov/pubs/fips/180-4/upd1/final", "official SHA family specification"),
        ("Python hmac documentation", "https://docs.python.org/3/library/hmac.html", "HMAC generation and verification"),
        ("GeeksforGeeks: Hashing in Cryptography", "https://www.geeksforgeeks.org/computer-networks/cryptography-hash-functions/", "hashing concepts and use cases"),
        ("Cloudflare Learning: What is a cryptographic hash?", "https://www.cloudflare.com/learning/ssl/what-is-a-cryptographic-hash/", "hash properties and applications"),
    ])
