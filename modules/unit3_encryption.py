import streamlit as st
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from modules.common import heading, explain, learning_check, is_prime, mod_inverse

def render():
    heading("Unit 3 — Symmetric and public-key encryption",
            "Compare AES, block-cipher modes, stream ciphers, random numbers, RSA, Diffie–Hellman, and elliptic-curve concepts.")
    tab1, tab2, tab3, tab4 = st.tabs(["AES-GCM real lab", "RSA toy lab", "Diffie–Hellman", "Concepts & quiz"])

    with tab1:
        st.subheader("AES-GCM: authenticated encryption")
        st.write("This lab uses the PyCryptodome AES implementation. It encrypts and authenticates a message; changing the ciphertext or tag causes verification to fail.")
        message = st.text_area("Message to protect", "Meet at the library at 3 PM.", key="aes_msg")
        key_text = st.text_input("Demo key phrase", "classroom-demo-key", key="aes_key")
        if st.button("Encrypt with AES-GCM", key="aes_encrypt"):
            key = __import__("hashlib").sha256(key_text.encode()).digest()
            nonce = get_random_bytes(12)
            cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
            ciphertext, tag = cipher.encrypt_and_digest(message.encode("utf-8"))
            st.session_state["u3_aes_payload"] = {
                "nonce": nonce.hex(), "ciphertext": ciphertext.hex(), "tag": tag.hex(),
                "key": key.hex()
            }
        payload = st.session_state.get("u3_aes_payload")
        if payload:
            st.write("**Demo payload**")
            st.json({k: v for k, v in payload.items() if k != "key"})
            st.caption("The key is kept in this Streamlit session for this teaching demo. In real systems, never hard-code or casually display keys.")
            if st.button("Decrypt and verify tag", key="aes_decrypt"):
                try:
                    cipher = AES.new(bytes.fromhex(payload["key"]), AES.MODE_GCM, nonce=bytes.fromhex(payload["nonce"]))
                    plain = cipher.decrypt_and_verify(bytes.fromhex(payload["ciphertext"]), bytes.fromhex(payload["tag"]))
                    st.success("Authentication tag valid. Plaintext: " + plain.decode("utf-8"))
                except Exception:
                    st.error("Authentication failed: payload was modified or the key/nonce/tag is wrong.")
            if st.button("Tamper with ciphertext (demo)", key="aes_tamper"):
                raw = bytearray.fromhex(payload["ciphertext"])
                if raw:
                    raw[0] ^= 1
                payload["ciphertext"] = bytes(raw).hex()
                st.session_state["u3_aes_payload"] = payload
                st.warning("Ciphertext changed. Now try decrypting; tag verification should fail.")
        explain("AES and modes",
                "AES is a symmetric block cipher with 128-bit blocks and 128/192/256-bit keys. ECB reveals repeated patterns and should generally be avoided. CBC needs correct padding and a secure IV plus separate integrity protection. CTR turns a block cipher into a stream-like mode and requires unique counter/nonce values. GCM provides authenticated encryption and is a good modern default when implemented correctly.")
        st.warning("A key phrase is SHA-256-derived only to make this lab easy to run. Real applications should use a proper key-management system or a password-based KDF such as scrypt/PBKDF2 with a salt.")

    with tab2:
        st.subheader("RSA — small numbers to understand the math")
        p = st.number_input("Prime p", min_value=3, max_value=97, value=11, step=1, key="rsa_p")
        q = st.number_input("Prime q", min_value=3, max_value=97, value=13, step=1, key="rsa_q")
        e = st.number_input("Public exponent e", min_value=3, max_value=1000, value=7, step=2, key="rsa_e")
        msg = st.number_input("Message integer m (must be less than n)", min_value=0, max_value=100000, value=42, step=1, key="rsa_m")
        p, q, e, msg = int(p), int(q), int(e), int(msg)
        if not is_prime(p) or not is_prime(q) or p == q:
            st.error("Choose two different prime numbers.")
        else:
            n = p*q
            phi = (p-1)*(q-1)
            d = mod_inverse(e, phi)
            st.write(f"n = p × q = **{n}**; φ(n) = **{phi}**")
            if d is None:
                st.error("e must be coprime to φ(n); choose another e.")
            elif msg >= n:
                st.error(f"Message must be smaller than n = {n}.")
            else:
                c = pow(msg, e, n)
                dec = pow(c, d, n)
                st.write(f"Public key: (e={e}, n={n})")
                st.write(f"Private exponent d: {d} (shown for teaching only)")
                st.write(f"Encrypted integer c = mᵉ mod n = **{c}**")
                st.success(f"Decrypted integer cᵈ mod n = **{dec}**")
                st.caption("Tiny RSA is completely insecure. Production RSA requires vetted libraries, secure padding such as OAEP, large keys, and careful implementation.")
        explain("RSA key-generation outline",
                "Choose distinct large primes p and q; calculate n=pq and φ(n)=(p−1)(q−1); choose e coprime to φ(n); compute d=e⁻¹ mod φ(n). Public key is (e,n); private key includes d and usually protected prime factors. This classroom arithmetic omits padding and implementation defenses.")

    with tab3:
        st.subheader("Diffie–Hellman key agreement simulator")
        prime = st.number_input("Small prime modulus p", min_value=5, max_value=97, value=23, step=1, key="dh_p")
        g = st.number_input("Generator/base g", min_value=2, max_value=20, value=5, step=1, key="dh_g")
        alice = st.number_input("Alice private value a", min_value=2, max_value=50, value=6, step=1, key="dh_a")
        bob = st.number_input("Bob private value b", min_value=2, max_value=50, value=15, step=1, key="dh_b")
        p, g, alice, bob = int(prime), int(g), int(alice), int(bob)
        A = pow(g, alice, p)
        B = pow(g, bob, p)
        shared_a = pow(B, alice, p)
        shared_b = pow(A, bob, p)
        st.write(f"Alice public value A = gᵃ mod p = **{A}**")
        st.write(f"Bob public value B = gᵇ mod p = **{B}**")
        st.write(f"Alice computes Bᵃ mod p = **{shared_a}**")
        st.write(f"Bob computes Aᵇ mod p = **{shared_b}**")
        st.success("Shared values match." if shared_a == shared_b else "Values do not match.")
        st.warning("This toy demo does not authenticate either party, so a man-in-the-middle can interfere. Real protocols use authenticated key exchange and vetted groups.")
        explain("Elliptic-curve cryptography (ECC)",
                "ECC uses arithmetic on points of an elliptic curve over a finite field. Its security relies on the difficulty of the elliptic-curve discrete logarithm problem. ECDH agrees on a shared secret; ECDSA signs messages. ECC often provides smaller keys than classic finite-field/RSA systems for comparable security, but curve choice and implementation must be standardized and vetted.")

    with tab4:
        explain("Stream ciphers and RC4",
                "A stream cipher combines plaintext with a keystream. Reusing a keystream can expose relationships between plaintexts. RC4 has serious known weaknesses and is deprecated; it is useful only as a historical syllabus topic.")
        explain("Random number generation",
                "Cryptography needs unpredictable random values for keys, nonces, salts, and ephemeral secrets. Use an operating-system-backed cryptographic random generator, not a general-purpose simulation PRNG.")
        learning_check("Which AES mode provides encryption and authentication together?",
                       ["ECB", "CBC alone", "GCM", "A textbook Caesar mode"], 2,
                       "AES-GCM is an authenticated-encryption mode when used with correct nonce discipline.", "u3q1")
        learning_check("What is the main weakness of unauthenticated Diffie–Hellman?",
                       ["It cannot derive a shared value", "It is vulnerable to man-in-the-middle attacks", "It requires no public values", "It only works with AES"], 1,
                       "Diffie–Hellman alone does not identify the communicating parties.", "u3q2")

    from modules.common import further_learning_resources
    further_learning_resources("Symmetric and public-key encryption", [
        ("NIST: Advanced Encryption Standard (AES)", "https://csrc.nist.gov/pubs/fips/197/final", "the official AES standard"),
        ("PyCryptodome documentation", "https://pycryptodome.readthedocs.io/en/latest/src/cipher/aes.html", "AES modes and implementation details"),
        ("Cloudflare Learning: What is RSA encryption?", "https://www.cloudflare.com/learning/ssl/what-is-rsa-encryption/", "public-key encryption concepts"),
        ("Crypto 101", "https://www.crypto101.io/", "symmetric encryption, public-key cryptography, and key exchange"),
    ])
