import streamlit as st
import random

st.title("🎰 Mini-Casino Slot Machine")

symbols = ["🍒", "🍋", "🔔", "💎", "🍀"]

if st.button("🎲 Drehen!"):
    result = [random.choice(symbols) for _ in range(3)]
    st.write(" | ".join(result))

    if result[0] == result[1] == result[2]:
        st.success("🎉 Jackpot! Alle Symbole gleich!")
    elif len(set(result)) == 2:
        st.info("Fast! Zwei gleiche Symbole.")
    else:
        st.warning("Leider kein Gewinn. Versuch's nochmal!")
