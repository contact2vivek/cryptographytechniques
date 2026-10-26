import streamlit as st
from modules.common import heading, explain, learning_check, progress_note

def render():
    heading("Unit 1 — Security foundations and classical ciphers",
            "Learn the security goals, attacks, mechanisms, network security model, and classical substitution/transposition ciphers.")
    progress_note()

    tab1, tab2, tab3, tab4 = st.tabs(["Concepts", "Attack & defense map", "Classical cipher lab", "Quiz"])

    with tab1:
        st.subheader("The CIA triad")
        cols = st.columns(3)
        for col, title, desc in zip(cols, ["Confidentiality", "Integrity", "Availability"],
                                    ["Only authorized people can read data.",
                                     "Data remains accurate and unaltered.",
                                     "Systems and data are accessible when needed."]):
            with col:
                st.markdown(f"### {title}")
                st.write(desc)
        explain("OSI security architecture — what to remember",
                "- **Security attacks:** actions that compromise security.\n"
                "- **Security services:** what protection is provided (authentication, access control, confidentiality, integrity, non-repudiation, availability).\n"
                "- **Security mechanisms:** how protection is implemented (encryption, digital signatures, access controls, audit trails, traffic padding, routing control).\n"
                "- **Passive attacks:** observe traffic (eavesdropping, traffic analysis).\n"
                "- **Active attacks:** alter, inject, replay, or disrupt traffic.")
        explain("Network security model",
                "A sender applies a security transformation (for example, encryption or a MAC), sends data over an untrusted channel, and a receiver verifies/decrypts it. A key-management or trusted third party may be required. Security depends on the algorithm, key secrecy, implementation, and protocol—not on hiding the algorithm.")
        explain("DES and cryptanalysis overview",
                "DES is a historical 64-bit block cipher with a 56-bit effective key. It is obsolete for new systems. Differential cryptanalysis studies how input differences affect output differences; linear cryptanalysis uses approximate linear relations among bits. These are concepts to understand, not attacks to run against real systems.")
        explain("Wireless and vehicular networks",
                "Typical risks include eavesdropping, rogue access points, spoofing, replay, jamming, Sybil attacks, and denial of service. Defenses include authenticated encryption, replay counters/timestamps, secure key provisioning, segmentation, monitoring, and resilient communication design.")

    with tab2:
        st.subheader("Choose a threat to see the security goal and defense")
        threat = st.selectbox("Threat", [
            "Eavesdropping", "Message tampering", "Replay attack", "Impersonation",
            "Denial of service", "Traffic analysis", "Rogue wireless access point",
            "Vehicular Sybil attack"
        ])
        mapping = {
            "Eavesdropping": ("Confidentiality", "Use modern authenticated encryption; protect keys and endpoints."),
            "Message tampering": ("Integrity", "Use an authenticated construction such as AES-GCM or a MAC."),
            "Replay attack": ("Freshness / authentication", "Use nonces, sequence numbers, timestamps, and replay windows."),
            "Impersonation": ("Authentication", "Use strong identity proof, certificates, MFA, and secure key management."),
            "Denial of service": ("Availability", "Rate limits, filtering, redundancy, monitoring, and incident response."),
            "Traffic analysis": ("Metadata privacy", "Reduce exposed metadata where feasible; padding can help but costs bandwidth."),
            "Rogue wireless access point": ("Confidentiality / authentication", "Validate network identity, use enterprise authentication, and avoid trusting unknown APs."),
            "Vehicular Sybil attack": ("Identity trust", "Use authenticated credentials, plausibility checks, revocation, and privacy-aware misbehavior detection.")
        }
        goal, defense = mapping[threat]
        st.metric("Primary security concern", goal)
        st.info(defense)
        st.caption("Real deployments combine multiple controls. One mechanism rarely solves every threat.")

    with tab3:
        st.subheader("Caesar cipher — a substitution cipher")
        text = st.text_input("Plaintext", "NETWORK SECURITY")
        shift = st.slider("Shift (key)", 0, 25, 3)
        def caesar(s, k):
            out = []
            for ch in s:
                if "A" <= ch <= "Z":
                    out.append(chr((ord(ch) - 65 + k) % 26 + 65))
                elif "a" <= ch <= "z":
                    out.append(chr((ord(ch) - 97 + k) % 26 + 97))
                else:
                    out.append(ch)
            return "".join(out)
        cipher = caesar(text, shift)
        st.write("**Encrypted text**")
        st.code(cipher)
        st.write("**Decrypted text**")
        st.code(caesar(cipher, -shift))
        st.warning("Caesar cipher is intentionally breakable and must never protect real data.")
        st.subheader("Transposition cipher — columnar rearrangement")
        plain = st.text_input("Text for transposition", "MEET ME AT NOON", key="trans_plain").replace(" ", "")
        width = st.slider("Columns", 2, 8, 4, key="trans_width")
        padded = plain + ("X" * ((-len(plain)) % width))
        rows = [padded[i:i+width] for i in range(0, len(padded), width)]
        st.write("Grid (rows are filled left-to-right)")
        st.code("\n".join(" ".join(row) for row in rows))
        trans = "".join("".join(row[c] for row in rows) for c in range(width))
        st.write("Read columns top-to-bottom:")
        st.code(trans)
        st.caption("This simple demo shows rearrangement, not a modern secure cipher.")

    with tab4:
        learning_check("Which security goal is most directly about preventing unauthorized reading?",
                       ["Integrity", "Confidentiality", "Availability", "Non-repudiation"], 1,
                       "Confidentiality protects information from unauthorized disclosure.", "u1q1")
        learning_check("Which is a passive attack?",
                       ["Replay", "Message modification", "Eavesdropping", "Denial of service"], 2,
                       "Eavesdropping observes communication without changing it.", "u1q2")
        learning_check("Why should DES not be used for new applications?",
                       ["It has no key", "Its effective key is too small by modern standards", "It is a hash", "It only works offline"], 1,
                       "DES has a 56-bit effective key and is obsolete.", "u1q3")

    from modules.common import further_learning_resources
    further_learning_resources("Security foundations and classical ciphers", [
        ("GeeksforGeeks: Network Security", "https://www.geeksforgeeks.org/computer-networks/network-security/", "security goals, threats, and network protection"),
        ("GeeksforGeeks: Cryptography", "https://www.geeksforgeeks.org/computer-networks/cryptography-and-network-security/", "cryptography basics and classical techniques"),
        ("Cloudflare Learning: What is the CIA triad?", "https://www.cloudflare.com/learning/security/glossary/what-is-the-cia-triad/", "confidentiality, integrity, and availability"),
        ("Crypto 101", "https://www.crypto101.io/", "a free introductory guide to cryptography"),
    ])
