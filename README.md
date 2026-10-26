# CRYPTOLAB

**Created by Vivek Raj** · M.Tech CSE educational learning companion — Interactive Network Security & Cryptography Learning Lab

Created for learning and classroom demonstrations. The redesigned home page explains why the project matters for future M.Tech students, introduces a recommended learning workflow, and provides a clearer visual map of the six syllabus units. The app includes interactive explanations, calculations, visual workflows, small quizzes, and practical labs.

## Project purpose
CRYPTOLAB is intended as a self-paced companion to M.Tech CSE506 Network Security & Cryptography. It helps learners revisit topics in one place and connect explanations with small interactive experiments. It is designed to support understanding and revision, not to replace lectures, textbooks, official course material, or standards-compliant tools.

## 1. Requirements
- Python 3.10+
- Internet is not needed after installing the packages.
- Install packages in your project's virtual environment:
  ```bash
  python -m pip install -r requirements.txt
  ```

## 2. Run
From the CRYPTOLAB folder:
```bash
python -m streamlit run app.py
```
Streamlit prints a local URL (usually `http://localhost:8501`). Open it in your browser.

## 3. Project structure
```text
CRYPTOLAB/
├── app.py
├── requirements.txt
├── README.md
└── modules/
    ├── __init__.py
    ├── common.py
    ├── unit1_security.py
    ├── unit2_number_theory.py
    ├── unit3_encryption.py
    ├── unit4_hash_authentication.py
    ├── unit5_signatures_protocols.py
    └── unit6_applied_security.py
```

## 4. Learning and safety notes
- Caesar cipher and RSA toy calculations are deliberately small educational examples, not secure for real use.
- AES-GCM, SHA-256 and HMAC use PyCryptodome for real cryptographic primitives. Use unique nonces with AES-GCM; never reuse a nonce with the same key.
- The app does not scan networks, attack devices, collect passwords, or provide a production VPN/firewall/IDS.
- TLS, IPsec, PGP, intrusion detection, post-quantum cryptography and homomorphic encryption are explained with interactive models and diagrams. The simplified models are not standards-compliant implementations.
- Never enter real passwords, private keys, confidential data, or production secrets into a classroom demo.

## 5. If something fails
1. Confirm the terminal is in the `CRYPTOLAB` folder.
2. Activate your virtual environment if you use one.
3. Run `python -m pip install -r requirements.txt`.
4. Run `python -m streamlit run app.py`.
5. If Streamlit reports a missing module, install dependencies using the same Python interpreter: `python -m pip install -r requirements.txt`.


## Further reading links
Each unit now ends with topic-aligned external resources, including GeeksforGeeks, NIST standards, RFCs, PyCryptodome documentation, Cloudflare Learning, and Crypto 101. These links are supplementary reading; check official standards and your course syllabus for authoritative requirements.
