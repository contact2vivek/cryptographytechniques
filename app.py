import streamlit as st
from modules import unit1_security, unit2_number_theory, unit3_encryption
from modules import unit4_hash_authentication, unit5_signatures_protocols, unit6_applied_security

st.set_page_config(
    page_title="CRYPTOLAB | Network Security & Cryptography",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Polished, responsive styling. All existing learning modules remain unchanged.
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
:root {
  --ink: #182235;
  --muted: #5f6b7d;
  --accent: #635bdb;
  --accent2: #12a594;
  --surface: #ffffff;
  --soft: #f3f5fb;
}
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.block-container { padding-top: 1.5rem; padding-bottom: 3rem; max-width: 1400px; }
h1, h2, h3 { font-family: 'Space Grotesk', sans-serif !important; letter-spacing: -0.025em; }
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #151d31 0%, #202b46 100%);
  border-right: 1px solid rgba(255,255,255,.08);
}
[data-testid="stSidebar"] * { color: #f3f5ff; }
[data-testid="stSidebar"] [data-testid="stRadio"] label {
  padding: .58rem .65rem; margin: .16rem 0; border-radius: 10px;
  transition: background .15s ease;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
  background: rgba(255,255,255,.09);
}
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,.16); }
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] { color: #bdc7dd; }
.hero {
  padding: 2.1rem 2.2rem; border-radius: 24px; color: white;
  background: radial-gradient(circle at 88% 12%, rgba(18,165,148,.45), transparent 27%),
              linear-gradient(125deg, #171f36 0%, #34316d 57%, #635bdb 100%);
  border: 1px solid rgba(255,255,255,.13); margin-bottom: 1.25rem;
  box-shadow: 0 18px 45px rgba(31, 38, 80, .16);
}
.hero h1 { color: white; font-size: clamp(2.3rem, 5vw, 3.7rem); margin: .25rem 0 .4rem; }
.hero p { color: #e3e8ff; font-size: 1.05rem; max-width: 850px; }
.eyebrow { text-transform: uppercase; letter-spacing: .16em; font-size: .75rem; font-weight: 700; color: #a9f4e6; }
.pill {
 display: inline-block; padding: .35rem .7rem; border-radius: 999px;
 background: rgba(255,255,255,.12); border: 1px solid rgba(255,255,255,.2);
 color: #f4f5ff; font-size: .82rem; margin: .2rem .25rem .1rem 0;
}
.section-kicker { color: #635bdb; font-weight: 700; letter-spacing: .11em; text-transform: uppercase; font-size: .76rem; }
.feature-card {
  border: 1px solid #e4e8f2; background: linear-gradient(145deg, #fff, #f7f8fd);
  border-radius: 17px; padding: 1.15rem 1.2rem; min-height: 150px;
}
.feature-card h3 { margin-top: .3rem; font-size: 1.08rem; }
.feature-card p { color: #5f6b7d; font-size: .94rem; margin-bottom: .2rem; }
.unit-card {
  border: 1px solid #e1e6f1; border-radius: 16px; padding: 1rem 1.1rem;
  background: white; min-height: 138px; box-shadow: 0 5px 18px rgba(30,45,80,.035);
}
.unit-num { font-size: .75rem; font-weight: 700; letter-spacing: .12em; color: #635bdb; }
.unit-card h3 { font-size: 1.02rem; margin: .3rem 0; }
.unit-card p { color: #657185; font-size: .9rem; margin: 0; }
.callout {
  border-left: 4px solid #12a594; background: #eefaf7; color: #1d4d49;
  border-radius: 0 12px 12px 0; padding: 1rem 1.1rem; margin: .6rem 0 1rem;
}
.stButton > button { border-radius: 10px; font-weight: 600; }
div[data-testid="stMetric"] { background: #f7f8fc; padding: .8rem; border-radius: 12px; border: 1px solid #e6e9f2; }
[data-testid="stExpander"] { border-radius: 12px; }
hr { border-color: #e7eaf2; }
@media (max-width: 700px) {
 .hero { padding: 1.4rem; border-radius: 18px; }
 .block-container { padding-left: 1rem; padding-right: 1rem; }
}
</style>
""", unsafe_allow_html=True)

units = [
    ("Unit 1 · Security foundations", "Threats, services, security models and classical ciphers", "🛡️"),
    ("Unit 2 · Number theory", "Modular arithmetic, primes, inverses and CRT", "🔢"),
    ("Unit 3 · Encryption", "AES-GCM, RSA concepts, key exchange and cipher modes", "🔐"),
    ("Unit 4 · Hash & authentication", "Hashing, HMAC, integrity and authentication", "🧾"),
    ("Unit 5 · Signatures & TLS", "Digital-signature concepts, certificates and TLS flow", "✍️"),
    ("Unit 6 · Applied security", "PGP, IPsec, IDS, firewalls and emerging cryptography", "🌐"),
]

st.sidebar.markdown("""
<div style="padding:.7rem .45rem 1.1rem">
  <div style="font-size:1.55rem;font-weight:800;letter-spacing:-.04em">🔐 CRYPTOLAB</div>
  <div style="font-size:.72rem;letter-spacing:.12em;color:#a9f4e6;font-weight:700">NETWORK SECURITY LAB</div>
  <div style="margin-top:.8rem;padding:.65rem .75rem;border-radius:12px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.12)">
    <div style="font-size:.7rem;color:#bdc7dd;text-transform:uppercase;letter-spacing:.1em">Created by</div>
    <div style="font-size:1rem;font-weight:700;color:white">Vivek Raj</div>
    <div style="font-size:.75rem;color:#bdc7dd">M.Tech CSE · Learning project</div>
  </div>
</div>
""", unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.markdown("#### 📚 EXPLORE THE COURSE")
choices = ["🏠 Home · Overview"] + [u[0] for u in units]
selection = st.sidebar.radio("Choose a unit", choices, label_visibility="collapsed")
st.sidebar.markdown("---")
st.sidebar.markdown("#### HOW TO STUDY")
st.sidebar.markdown("""
<div style="font-size:.88rem;line-height:1.95;color:#e2e8f7">
<span style="color:#a9f4e6">01</span> &nbsp; Read the concept<br>
<span style="color:#a9f4e6">02</span> &nbsp; Predict the result<br>
<span style="color:#a9f4e6">03</span> &nbsp; Run the lab<br>
<span style="color:#a9f4e6">04</span> &nbsp; Check your learning
</div>
""", unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="font-size:.78rem;color:#bdc7dd;line-height:1.6">
A self-paced companion for M.Tech CSE506.<br><br>
<strong style="color:#f3f5ff">Learn it. Test it. Understand it.</strong>
</div>
""", unsafe_allow_html=True)

if selection.startswith("🏠 Home"):
    st.markdown("""
    <div class="hero">
      <div class="eyebrow">M.Tech CSE506 · NETWORK SECURITY & CRYPTOGRAPHY</div>
      <h1>CRYPTOLAB</h1>
      <div style="font-weight:600;color:#b8fff0;margin-bottom:.7rem">Created by Vivek Raj · M.Tech CSE</div>
      <p>A hands-on companion for learning cryptography and network security — explore a concept, experiment with inputs, and see what changes instead of memorising definitions alone.</p>
      <span class="pill">6 learning units</span><span class="pill">Interactive labs</span><span class="pill">Concept checks</span><span class="pill">Self-paced learning</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-kicker">Why this project matters</div>', unsafe_allow_html=True)
    st.subheader("Built to help the next M.Tech student go deeper")
    st.write(
        "Network Security & Cryptography combines mathematical ideas, algorithms, protocols, and real-world security decisions. "
        "For future M.Tech students, CRYPTOLAB is designed to make those connections easier to explore in one place. "
        "Students can browse units at their own pace, change example inputs, run small experiments, compare outputs, and revisit explanations "
        "whenever a classroom topic feels abstract. The goal is to make the syllabus easier to explore independently and help students connect theory with practice."
    )
    st.markdown("""
    <div class="callout"><b>The learning goal:</b> move from “I have read this topic” to “I can explain the idea, try it, interpret the result, and recognise its limitations.”</div>
    """, unsafe_allow_html=True)

    feature_cols = st.columns(3)
    features = [
        ("🧠", "Understand, don't just memorise", "Short explanations and examples connect definitions to the underlying idea."),
        ("🧪", "Learn by experimenting", "Change values in interactive labs and observe how the output responds."),
        ("🧭", "One place to revisit topics", "Browse six modules as a study companion before class, after class, or during revision."),
    ]
    for col, (icon, title, desc) in zip(feature_cols, features):
        with col:
            st.markdown(f'<div class="feature-card"><div style="font-size:1.65rem">{icon}</div><h3>{title}</h3><p>{desc}</p></div>', unsafe_allow_html=True)

    st.write("")
    st.markdown('<div class="section-kicker">Explore the syllabus</div>', unsafe_allow_html=True)
    st.subheader("Choose a learning unit")
    st.caption("Use the left navigation to open any unit. You can study them in syllabus order or jump directly to a topic you want to practise.")
    for start in range(0, 6, 3):
        cols = st.columns(3)
        for col, unit_data in zip(cols, units[start:start+3]):
            title, desc, emoji = unit_data
            num = title.split(" · ")[0].upper()
            with col:
                st.markdown(f'<div class="unit-card"><div class="unit-num">{num}</div><h3>{emoji} {title.split(" · ", 1)[1]}</h3><p>{desc}</p></div>', unsafe_allow_html=True)
        st.write("")
    st.markdown('<div class="section-kicker">Recommended workflow</div>', unsafe_allow_html=True)
    st.subheader("How to get the most out of CRYPTOLAB")
    steps = st.columns(5)
    for col, n, title, desc in zip(
        steps,
        ["01", "02", "03", "04", "05"],
        ["Preview", "Predict", "Experiment", "Explain", "Revise"],
        ["Read the topic overview.", "Think about the expected result.", "Try the lab with sample inputs.", "Describe why the output happened.", "Finish with the unit's checks."]
    ):
        with col:
            st.markdown(f'<div class="feature-card" style="min-height:145px"><div class="unit-num">{n}</div><h3>{title}</h3><p>{desc}</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-kicker">Keep learning beyond this app</div>', unsafe_allow_html=True)
    st.subheader("For more, you can visit here")
    st.write("Use these trusted learning resources alongside the interactive labs. Each unit also includes links matched to its topics.")
    ext1, ext2, ext3 = st.columns(3)
    with ext1:
        st.markdown("**[GeeksforGeeks — Computer Networks](https://www.geeksforgeeks.org/computer-networks/)**")
        st.caption("Accessible explanations and worked examples.")
    with ext2:
        st.markdown("**[Crypto 101](https://www.crypto101.io/)**")
        st.caption("A free introductory cryptography guide.")
    with ext3:
        st.markdown("**[NIST Computer Security Resource Center](https://csrc.nist.gov/)**")
        st.caption("Standards and authoritative security references.")
    st.markdown("**Project author:** Vivek Raj · Created as an educational companion for future M.Tech students studying Network Security & Cryptography.")
    st.info("Learning note: simplified examples are for education. They do not replace the official course syllabus, standards, or production security implementations.")

else:
    unit_name = selection.split(" · ", 1)[0]
    unit_meta = next((u for u in units if u[0] == selection), None)
    if unit_meta:
        st.markdown(f"""
        <div class="hero" style="padding:1.25rem 1.6rem">
          <div class="eyebrow">CRYPTOLAB · LEARNING MODULE</div>
          <h1 style="font-size:2.15rem">{unit_meta[2]} {unit_meta[0]}</h1>
          <p>{unit_meta[1]}</p>
        </div>
        """, unsafe_allow_html=True)

    if selection.startswith("Unit 1"):
        unit1_security.render()
    elif selection.startswith("Unit 2"):
        unit2_number_theory.render()
    elif selection.startswith("Unit 3"):
        unit3_encryption.render()
    elif selection.startswith("Unit 4"):
        unit4_hash_authentication.render()
    elif selection.startswith("Unit 5"):
        unit5_signatures_protocols.render()
    else:
        unit6_applied_security.render()

st.divider()
st.caption("Created by Vivek Raj · CRYPTOLAB is an educational learning aid. Verify course requirements against your official syllabus. Never enter real passwords, private keys, confidential data, or production secrets.")
