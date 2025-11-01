import streamlit as st
import random

# Initialisierung
if "lives" not in st.session_state:
    st.session_state.lives = 30
if "score" not in st.session_state:
    st.session_state.score = 0
if "level" not in st.session_state:
    st.session_state.level = 1
if "game_over" not in st.session_state:
    st.session_state.game_over = False

st.title("🎮 Mini Game Quest")
st.write(f"❤️ Leben: {st.session_state.lives} | ⭐ Punkte: {st.session_state.score} | 🧩 Level: {st.session_state.level}")

# GAME OVER
if st.session_state.lives <= 0:
    st.session_state.game_over = True

if st.session_state.game_over:
    st.error("💀 GAME OVER! Du hast keine Leben mehr.")
    st.write(f"🏆 Dein Punktestand: {st.session_state.score}")
    if st.button("🔄 Neustarten"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
    st.stop()


# LEVEL 1: Slot Machine
if st.session_state.level == 1:
    st.subheader("🎰 Level 1: Slot Machine")
    symbols = ["🍒", "🍋", "🔔", "💎", "🍀"]
    if st.button("🎲 Drehen!"):
        result = [random.choice(symbols) for _ in range(3)]
        st.write(" | ".join(result))
        if result[0] == result[1] == result[2]:
            st.success("🎉 Jackpot! Weiter zu Level 2")
            st.session_state.score += 10
            st.session_state.level = 2
        else:
            st.warning("Leider kein Gewinn. Du verlierst ein Leben.")
            st.session_state.lives -= 1

# LEVEL 2: Hangman
if st.session_state.level == 2:
    st.subheader("🧩 Level 2: Hangman")
    word = "streamlit"
    st.write(f"🔠 Das Wort hat {len(word)} Buchstaben.")
    if "guesses" not in st.session_state:
        st.session_state.guesses = []
        st.session_state.wrong = 0

    guess = st.text_input("Gib einen Buchstaben ein:", max_chars=1).lower()
    if guess and guess not in st.session_state.guesses:
        st.session_state.guesses.append(guess)
        if guess not in word:
            st.session_state.wrong += 1
            st.session_state.lives -= 1

    display = [letter if letter in st.session_state.guesses else "_" for letter in word]
    st.write(" ".join(display))
    st.write(f"❌ Fehler: {st.session_state.wrong} / 6")
    
# Zeige falsche Buchstaben
wrong_letters = [g for g in st.session_state.guesses if g not in word]
if wrong_letters:
    st.write("🚫 Falsche Buchstaben:", ", ".join(wrong_letters))


    if "_" not in display:
        st.success("🎉 Du hast das Wort erraten! Weiter zu Level 3")
        st.session_state.score += 20
        st.session_state.level = 3
        st.session_state.guesses = []
        st.session_state.wrong = 0
    elif st.session_state.wrong >= 6:
        st.error("😢 Leider verloren. Weiter zu Level 3")
        st.session_state.level = 3
        st.session_state.guesses = []
        st.session_state.wrong = 0
    st.stop()


# LEVEL 3: Zahlenraten
if st.session_state.level == 3:
    st.subheader("🔢 Level 3: Zahlenraten")
    if "target" not in st.session_state:
        st.session_state.target = random.randint(1, 100)
        st.session_state.attempts = 0

    guess = st.number_input("Rate eine Zahl zwischen 1 und 100:", min_value=1, max_value=100, step=1)
    if st.button("🔍 Prüfen"):
        st.session_state.attempts += 1
        if guess == st.session_state.target:
            st.success("🎉 Richtig geraten! Weiter zu Level 4")
            st.session_state.score += 15
            st.session_state.level = 4
            del st.session_state.target
            del st.session_state.attempts
        elif guess < st.session_state.target:
            st.info("Zu niedrig!")
        else:
            st.info("Zu hoch!")
        if st.session_state.attempts >= 5:
            st.error("😢 Zu viele Versuche! Weiter zu Level 4")
            st.session_state.lives -= 1
            st.session_state.level = 4
            del st.session_state.target
            del st.session_state.attempts
    st.stop()

# LEVEL 4: Memory
if st.session_state.level == 4:
    st.subheader("🧠 Level 4: Memory")
    if "memory" not in st.session_state:
        emojis = ["🐶", "🐱", "🐶", "🐱"]
        random.shuffle(emojis)
        st.session_state.memory = emojis
        st.session_state.revealed = [False] * 4
        st.session_state.selected = []

    cols = st.columns(4)
    for i in range(4):
        with cols[i]:
            if st.session_state.revealed[i]:
                st.button(st.session_state.memory[i], key=f"mem{i}", disabled=True)
            else:
                if st.button("❓", key=f"mem{i}"):
                    st.session_state.revealed[i] = True
                    st.session_state.selected.append(i)

    if len(st.session_state.selected) == 2:
        i1, i2 = st.session_state.selected
        if st.session_state.memory[i1] == st.session_state.memory[i2]:
            st.success("🎉 Paar gefunden! Weiter zu Level 5")
            st.session_state.score += 25
            st.session_state.level = 5
        else:
            st.error("😢 Kein Paar! Weiter zu Level 5")
            st.session_state.lives -= 1
            st.session_state.revealed[i1] = False
            st.session_state.revealed[i2] = False
            st.session_state.level = 5
        st.session_state.selected = []
    st.stop()

# LEVEL 5: Mathe-Duell
if st.session_state.level == 5:
    st.subheader("➕ Level 5: Mathe-Duell")
    if "math_correct" not in st.session_state:
        st.session_state.math_correct = 0
        st.session_state.math_total = 0

    a, b = random.randint(1, 10), random.randint(1, 10)
    answer = st.number_input(f"{a} + {b} =", step=1)
    if st.button("✅ Prüfen"):
        st.session_state.math_total += 1
        if answer == a + b:
            st.success("Richtig!")
            st.session_state.math_correct += 1
        else:
            st.warning("Falsch!")
        if st.session_state.math_total >= 3:
            if st.session_state.math_correct >= 2:
                st.success("🎉 Mathe bestanden! Weiter zu Level 6")
                st.session_state.score += 20
            else:
                st.error("😢 Mathe nicht bestanden! Weiter zu Level 6")
                st.session_state.lives -= 1
            st.session_state.level = 6
            del st.session_state.math_correct
            del st.session_state.math_total
    st.stop()

# LEVEL 6: Quiz
if st.session_state.level == 6:
    st.subheader("❓ Level 6: Quiz")
    questions = [
        ("Was ist die Hauptstadt von Deutschland?", "Berlin"),
        ("Wie viele Beine hat eine Spinne?", "8"),
        ("Was ist 5 * 6?", "30")
    ]
    if "quiz_index" not in st.session_state:
        st.session_state.quiz_index = 0
        st.session_state.quiz_score = 0

    if st.session_state.quiz_index < len(questions):
        q, a = questions[st.session_state.quiz_index]
        user_answer = st.text_input(q)
        if st.button("Antwort prüfen"):
            if user_answer.strip().lower() == a.lower():
                st.success("Richtig!")
                st.session_state.quiz_score += 1
            else:
                st.warning("Falsch!")
            st.session_state.quiz_index += 1
    else:
        if st.session_state.quiz_score >= 2:
            st.success("🎉 Quiz bestanden! Du hast das Spiel geschafft!")
            st.balloons()
            st.session_state.score += 30
        else:
            st.error("😢 Quiz nicht bestanden!")
            st.session_state.lives -= 1
        st.session_state.level = 1
        del st.session_state.quiz_index
        del st.session_state.quiz_score
