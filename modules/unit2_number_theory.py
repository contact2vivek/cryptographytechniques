import streamlit as st
from modules.common import heading, explain, learning_check, is_prime, mod_inverse

def render():
    heading("Unit 2 — Number theory for cryptography",
            "Explore modular arithmetic, primes, groups/rings/fields, Fermat's theorem, Euler's theorem, and the Chinese Remainder Theorem (CRT).")

    tab1, tab2, tab3, tab4 = st.tabs(["Modular arithmetic", "Prime & inverse lab", "Theorems", "Quiz"])

    with tab1:
        st.subheader("Modular arithmetic")
        a = st.number_input("Integer a", value=29, step=1, key="u2a")
        b = st.number_input("Integer b", value=8, step=1, key="u2b")
        m = st.number_input("Modulus m", min_value=2, value=7, step=1, key="u2m")
        st.latex(r"a \bmod m")
        st.write(f"**a mod m = {int(a) % int(m)}**")
        st.write(f"**(a + b) mod m = {(int(a)+int(b)) % int(m)}**")
        st.write(f"**(a × b) mod m = {(int(a)*int(b)) % int(m)}**")
        st.write(f"**aᵇ mod m = {pow(int(a), int(b) % 10000, int(m))}** (using modular exponentiation)")
        explain("Why modulo matters",
                "Cryptographic algorithms often operate on a finite set of values. Modular arithmetic wraps results around a modulus, keeping calculations bounded. Efficient modular exponentiation computes powers without constructing enormous intermediate integers.")

    with tab2:
        n = st.number_input("Check whether n is prime", min_value=0, max_value=1000000, value=97, step=1)
        st.success(f"{int(n)} is prime." if is_prime(int(n)) else f"{int(n)} is not prime.")
        a = st.number_input("Find inverse of a modulo m: a", value=3, step=1, key="inv_a")
        m = st.number_input("Modulus m", min_value=2, value=11, step=1, key="inv_m")
        inv = mod_inverse(int(a), int(m))
        if inv is None:
            st.error(f"No multiplicative inverse exists because gcd({int(a)}, {int(m)}) is not 1.")
        else:
            st.success(f"Inverse = {inv}; verification: ({int(a)} × {inv}) mod {int(m)} = {(int(a)*inv)%int(m)}")
        st.caption("An inverse exists exactly when gcd(a, m) = 1.")

    with tab3:
        explain("Groups, rings and fields",
                "- A **group** has a set and operation with closure, associativity, identity, and inverses.\n"
                "- A **ring** supports addition and multiplication with ring axioms; multiplication need not have inverses for every nonzero element.\n"
                "- A **field** has addition and multiplication, and every nonzero element has a multiplicative inverse. Integers modulo a prime p form a finite field GF(p).")
        explain("Fermat's Little Theorem",
                "If p is prime and p does not divide a, then a^(p−1) ≡ 1 (mod p). It supports modular arithmetic and primality-related reasoning.")
        explain("Euler's theorem",
                "If gcd(a,n)=1, then a^φ(n) ≡ 1 (mod n), where φ(n) counts integers from 1 to n that are coprime to n. Fermat's theorem is a special case for prime modulus.")
        explain("Chinese Remainder Theorem",
                "When moduli are pairwise coprime, a system of congruences has a unique solution modulo their product. CRT can speed up RSA calculations, but implementations must still guard against faults and side channels.")
        st.subheader("CRT calculator")
        r1 = st.number_input("x ≡ r1 (mod m1)", value=2, step=1, key="crt_r1")
        m1 = st.number_input("m1", min_value=2, value=3, step=1, key="crt_m1")
        r2 = st.number_input("x ≡ r2 (mod m2)", value=3, step=1, key="crt_r2")
        m2 = st.number_input("m2", min_value=2, value=5, step=1, key="crt_m2")
        if __import__("math").gcd(int(m1), int(m2)) != 1:
            st.warning("This demo expects pairwise-coprime moduli.")
        else:
            solution = next(x for x in range(int(m1)*int(m2)) if x % int(m1) == int(r1) % int(m1) and x % int(m2) == int(r2) % int(m2))
            st.success(f"x ≡ {solution} (mod {int(m1)*int(m2)})")
            st.write(f"Check: {solution} mod {int(m1)} = {solution%int(m1)}; {solution} mod {int(m2)} = {solution%int(m2)}")

    with tab4:
        learning_check("A modular inverse of a modulo m exists when:",
                       ["a is even", "m is prime always", "gcd(a,m)=1", "a is greater than m"], 2,
                       "The multiplicative inverse exists exactly when a and m are coprime.", "u2q1")
        learning_check("Fermat's Little Theorem requires which condition for a^(p−1) ≡ 1 mod p?",
                       ["p is prime and p does not divide a", "a is prime", "p is even", "a=m"], 0,
                       "The modulus p must be prime and a must not be divisible by p.", "u2q2")

    from modules.common import further_learning_resources
    further_learning_resources("Number theory for cryptography", [
        ("GeeksforGeeks: Modular Arithmetic", "https://www.geeksforgeeks.org/maths/modular-arithmetic/", "remainders and modular operations"),
        ("GeeksforGeeks: Euclidean Algorithm", "https://www.geeksforgeeks.org/dsa/euclidean-algorithms-basic-and-extended/", "GCD and modular inverses"),
        ("Khan Academy: Modular arithmetic", "https://www.khanacademy.org/computing/computer-science/cryptography", "guided mathematical foundations for cryptography"),
        ("Wikipedia: Chinese Remainder Theorem", "https://en.wikipedia.org/wiki/Chinese_remainder_theorem", "the theorem and worked mathematical context"),
    ])
