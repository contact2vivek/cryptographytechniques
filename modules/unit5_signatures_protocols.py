import streamlit as st
from modules.common import heading, explain, learning_check, sha256_hex

def render():
    heading("Unit 5 — Digital signatures and secure protocols",
            "Understand digital signatures, authentication protocols, DSS/DSA concepts, and the TLS handshake.")
    tab1, tab2, tab3 = st.tabs(["Signature concept lab", "TLS handshake", "Quiz"])

    with tab1:
        st.subheader("Digital signature: what changes when a message changes?")
        message = st.text_area("Document to sign", "I approve the network security lab.", key="u5_doc")
        signature_demo = sha256_hex("EDUCATIONAL-SIGNING-KEY|" + message)
        st.write("**Educational signature token**")
        st.code(signature_demo)
        changed = st.text_area("Document to verify", message, key="u5_verify_doc")
        if st.button("Verify demo token", key="u5_verify"):
            if sha256_hex("EDUCATIONAL-SIGNING-KEY|" + changed) == signature_demo:
                st.success("Demo token matches this document.")
            else:
                st.error("Verification failed: the document differs.")
        st.warning("This is a teaching simulation, NOT a digital signature. It uses a hard-coded phrase and has no public/private key pair. Never use it to sign real documents.")
        explain("Real digital signatures",
                "A signer uses a private key to produce a signature over a message or its digest. Anyone with the corresponding public key can verify it. Depending on the scheme and trust model, signatures support integrity, origin authentication, and evidence useful for non-repudiation. Common schemes include RSA-PSS, ECDSA, and EdDSA. DSA/DSS is an important historical syllabus topic; use current standards and vetted libraries in real systems.")
        explain("Authentication protocol pitfalls",
                "Protocols must prevent replay, reflection, downgrade, and man-in-the-middle attacks. Nonces, sequence numbers, timestamps, channel binding, certificate validation, and explicit key confirmation may be required. Authentication should be bound to the intended session and identities.")

    with tab2:
        st.subheader("TLS handshake — message-flow model")
        step = st.slider("Move through the handshake", 1, 6, 1)
        steps = [
            ("1. ClientHello", "Client proposes supported TLS versions, cipher suites, and key-share parameters."),
            ("2. ServerHello", "Server selects parameters and sends its key share."),
            ("3. Certificate and proof", "Server presents its certificate and proves possession of the corresponding private key."),
            ("4. Certificate validation", "Client validates chain, hostname, dates, and trust policy."),
            ("5. Key derivation and Finished", "Both sides derive traffic keys and authenticate the handshake transcript."),
            ("6. Protected application data", "Application data is protected with negotiated authenticated encryption.")
        ]
        title, desc = steps[step-1]
        st.subheader(title)
        st.write(desc)
        st.progress(step / len(steps))
        st.caption("This is a simplified learning sequence. Exact messages vary by TLS version and configuration.")
        explain("TLS security checks",
                "A secure connection requires certificate validation, hostname matching, modern protocol versions, safe cipher suites, correct randomness, and correct key handling. Encryption without authenticating the server can still leave users vulnerable to impersonation.")
        explain("DSS / DSA",
                "Digital Signature Standard (DSS) describes approved digital-signature approaches; DSA is a signature algorithm historically associated with DSS. Signature algorithms require carefully generated parameters and per-message nonces. Nonce reuse or bias can reveal a private key. Use vetted cryptographic libraries rather than hand-coding signature algorithms.")

    with tab3:
        learning_check("What key is used to verify a conventional public-key digital signature?",
                       ["The signer's private key", "The corresponding public key", "A shared AES key only", "No key"], 1,
                       "The public key verifies a signature created with the corresponding private key.", "u5q1")
        learning_check("Why must a TLS client validate the server certificate and hostname?",
                       ["To make the page load faster", "To verify the server identity", "To avoid using encryption", "To create a shorter URL"], 1,
                       "Certificate and hostname validation help prevent connecting securely to an impostor.", "u5q2")

    from modules.common import further_learning_resources
    further_learning_resources("Digital signatures and secure protocols", [
        ("NIST: Digital Signature Standard (DSS)", "https://csrc.nist.gov/pubs/fips/186-5/final", "official digital signature standard"),
        ("Cloudflare Learning: What is a TLS handshake?", "https://www.cloudflare.com/learning/ssl/what-happens-in-a-tls-handshake/", "the stages of a TLS connection"),
        ("MDN: Transport Layer Security (TLS)", "https://developer.mozilla.org/en-US/docs/Web/Security/Transport_Layer_Security", "TLS security concepts and browser context"),
        ("GeeksforGeeks: Digital Signature", "https://www.geeksforgeeks.org/computer-networks/digital-signature/", "signature purpose and verification concepts"),
    ])
