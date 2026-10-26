import streamlit as st
from modules.common import heading, explain, learning_check

def render():
    heading("Unit 6 — Applied security: PGP, IPsec, IDS, firewalls, and emerging cryptography",
            "Explore how security mechanisms fit into real systems. These are interactive learning models, not production network tools.")
    tab1, tab2, tab3, tab4 = st.tabs(["PGP & IPsec", "IDS & firewall lab", "Emerging crypto", "Quiz"])

    with tab1:
        st.subheader("PGP-style email protection flow")
        st.write("Choose the properties you want to demonstrate:")
        confidentiality = st.checkbox("Confidentiality (encrypt for recipient)", True, key="pgp_conf")
        integrity = st.checkbox("Integrity (hash / authenticated protection)", True, key="pgp_int")
        signature = st.checkbox("Sender signature", True, key="pgp_sig")
        flow = ["Compose message"]
        if integrity:
            flow.append("Calculate integrity check")
        if signature:
            flow.append("Sign with sender private key")
        if confidentiality:
            flow.append("Encrypt for recipient")
        flow.extend(["Transmit over untrusted channel", "Recipient processes in reverse order", "Verify integrity / signature"])
        for i, item in enumerate(flow, 1):
            st.markdown(f"**{i}.** {item}")
        st.caption("PGP/OpenPGP combines public-key cryptography, symmetric encryption, signatures, and key management. This flow is conceptual; this app does not implement OpenPGP.")
        explain("IPsec architecture",
                "IPsec protects IP traffic at the network layer. **AH (Authentication Header)** provides integrity and data-origin authentication but not confidentiality; it is generally difficult to use with NAT. **ESP (Encapsulating Security Payload)** can provide confidentiality and can also provide integrity/authentication. A Security Association (SA) defines parameters such as algorithms, keys, and lifetimes. Transport mode protects payloads; tunnel mode encapsulates an entire IP packet.")
        mode = st.radio("IPsec mode", ["Transport mode", "Tunnel mode"], horizontal=True, key="ipsec_mode")
        if mode == "Transport mode":
            st.info("Conceptual packet: [IP header][protected transport payload]. Commonly used host-to-host.")
        else:
            st.info("Conceptual packet: [Outer IP header][protected inner IP packet]. Commonly used gateway-to-gateway VPN.")
        explain("Intruders and password management",
                "Common intruder behaviors include credential theft, privilege escalation, persistence, and lateral movement. Defensive password management includes long unique passwords, password managers, MFA, rate limiting, breached-password checks, secure password hashing, and monitoring. Never store plaintext passwords.")

    with tab2:
        st.subheader("Toy intrusion-detection rule engine")
        events = st.multiselect("Select sample events", [
            "Five failed logins in a minute", "Connection to known malicious IP",
            "Unusual outbound data volume", "Successful login from usual device",
            "Port scan pattern", "Repeated access denied"
        ], default=["Five failed logins in a minute", "Port scan pattern"])
        rules = {
            "Five failed logins in a minute": ("HIGH", "Possible password guessing; rate-limit and review account activity."),
            "Connection to known malicious IP": ("HIGH", "Check threat intelligence, isolate if warranted, and investigate endpoint context."),
            "Unusual outbound data volume": ("MEDIUM", "Possible exfiltration or legitimate bulk transfer; correlate with user and process."),
            "Successful login from usual device": ("LOW", "Usually normal, but continue baseline monitoring."),
            "Port scan pattern": ("MEDIUM", "Could be reconnaissance; confirm source and whether activity is authorized."),
            "Repeated access denied": ("LOW", "May indicate misconfiguration or probing; correlate with other signals.")
        }
        for event in events:
            severity, action = rules[event]
            st.markdown(f"**{severity} — {event}**")
            st.write(action)
        st.caption("This is a static toy rule set, not a live IDS. Real systems need telemetry, tuning, baselines, false-positive handling, and incident response.")
        st.subheader("Firewall policy simulator")
        source = st.selectbox("Source zone", ["Internet", "Student network", "Admin network", "Server subnet"], key="fw_src")
        dest = st.selectbox("Destination", ["Public web server", "Database", "Admin console", "DNS resolver"], key="fw_dest")
        service = st.selectbox("Service", ["HTTPS", "SSH", "Database port", "DNS", "Any"], key="fw_service")
        allowed = (
            (source == "Internet" and dest == "Public web server" and service == "HTTPS") or
            (source == "Student network" and dest == "DNS resolver" and service == "DNS") or
            (source == "Admin network" and dest in ("Admin console", "Server subnet") and service in ("SSH", "HTTPS")) or
            (source == "Server subnet" and dest == "DNS resolver" and service == "DNS")
        )
        st.success("ALLOW by this demo policy" if allowed else "DENY by this demo policy")
        st.caption("Example least-privilege policy only; it is not connected to a real firewall.")

    with tab3:
        explain("Homomorphic encryption",
                "Homomorphic encryption permits certain computations on ciphertexts so that decrypting the result yields the result of the corresponding computation on plaintexts. It can support privacy-preserving analytics but often has substantial performance and design costs. This app explains the concept but does not implement an HE scheme.")
        st.subheader("Toy homomorphic-addition idea")
        a = st.number_input("Plain value A", min_value=0, max_value=100, value=7, key="he_a")
        b = st.number_input("Plain value B", min_value=0, max_value=100, value=12, key="he_b")
        offset = st.number_input("Toy reversible offset", min_value=1, max_value=100, value=19, key="he_offset")
        ca, cb = int(a)+int(offset), int(b)+int(offset)
        encrypted_sum = ca + cb
        recovered = encrypted_sum - 2*int(offset)
        st.write(f"Toy encoded values: E(A)={ca}, E(B)={cb}")
        st.write(f"Operate on encoded values: E(A)+E(B)={encrypted_sum}")
        st.write(f"Decode result: {recovered} (expected A+B = {int(a)+int(b)})")
        st.warning("This offset trick is NOT encryption and provides no security. It only illustrates the idea of operating on transformed values.")
        explain("Post-quantum cryptography (PQC)",
                "PQC refers to cryptographic algorithms designed to resist known quantum-computer attacks. Standards work includes lattice-based key establishment and digital signatures. Migration requires crypto inventory, protocol support, hybrid deployments where appropriate, and attention to implementation and interoperability. Do not invent or hand-roll a PQC scheme for production.")
        explain("Security monitoring and firewall design",
                "A defense-in-depth design combines segmentation, default-deny rules, explicit allowed flows, logging, IDS/IPS, endpoint controls, patching, backups, and incident response. Detection rules are only useful when alerts are triaged and false positives are managed.")

    with tab4:
        learning_check("Which IPsec protocol can provide confidentiality?",
                       ["AH only", "ESP", "Neither AH nor ESP", "DNS"], 1,
                       "ESP can provide confidentiality and may also provide integrity/authentication.", "u6q1")
        learning_check("What does a default-deny firewall policy mean?",
                       ["Allow all unless blocked", "Block all unless explicitly allowed", "Allow only encrypted email", "Disable logging"], 1,
                       "Default-deny reduces exposure by requiring explicit allow rules.", "u6q2")
        learning_check("Does the toy offset example implement secure homomorphic encryption?",
                       ["Yes, production-grade", "No, it is only an illustration", "Yes, if the offset is large", "Only for numbers above 10"], 1,
                       "A reversible offset reveals the data and is not cryptographic protection.", "u6q3")

    from modules.common import further_learning_resources
    further_learning_resources("Applied security and emerging cryptography", [
        ("RFC 4301: IPsec Security Architecture", "https://www.rfc-editor.org/rfc/rfc4301", "the IPsec architecture specification"),
        ("RFC 9580: OpenPGP", "https://www.rfc-editor.org/rfc/rfc9580", "the OpenPGP message format standard"),
        ("NIST: Post-Quantum Cryptography", "https://csrc.nist.gov/projects/post-quantum-cryptography", "NIST's post-quantum cryptography programme"),
        ("OWASP: Web Application Security Testing Guide", "https://owasp.org/www-project-web-security-testing-guide/", "structured security testing guidance"),
    ])
