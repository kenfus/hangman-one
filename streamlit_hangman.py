
import streamlit as st
import string
import time
import dataclasses

# [start] [persistent states]__________________________________________
@dataclasses.dataclass
class gameState:
    # HangMan
    hm_word: str = ""
    hm_word_letters = set(hm_word)
    hm_alphabet = set(string.ascii_uppercase)
    hm_used_letters = set()
    hm_word_list = []
    hm_idxml_key: int = 0


@st.cache(allow_output_mutation=True)
def _gameState() -> gameState:
    return gameState()


hm = _gameState()


# [start] [HangMan]____________________________________________________


def HangMan():
    word = '7kbo39yy9yl86artud7k'
    if hm.hm_word == "":
        if word == "":
            st.sidebar.warning("**Please enter the hidden word.**")
        else:
            hm.hm_word = word.upper()
            hm.hm_word_letters = set(hm.hm_word)
            st.experimental_rerun()
    elif hm.hm_word != "":
        st.sidebar.success("**Game in progress...**")

    word_list = [letter if letter in hm.hm_used_letters else "-" for letter in hm.hm_word]

    st.sidebar.markdown("___")
    b_reset, b_show_answer = st.sidebar.columns([3, 3])
    if st.checkbox('Show hint 🔭', False):
        st.markdown(
        f"""
        <br>
            The hidden word is made up of 20 letters and numbers. Thus, it has  (26 + 10) ** 20 = 1.33674945 x 10^31 possible combinations. Because you can feedback per letter, you will need (in the worst case) 20 * 36 trys to guess the word.
            If you make one guess every 5 second, it will take you 20 * 36 * 5 / 60 = 1 hour to guess the word.
            Maybe there is another way to figure this out? 
        
            Hint: After applying the sha256 algorithm, the hidden word is as following:
            700C2FF3575E9B09E7342BF6E5C5144DE16D20D4EB3A8E1766C9C9A38A7CE138

            However, no inverse function to the sha256 algorithm is know, so I guess the previous hint is useless (it is, really).
        <br>
        """,
        unsafe_allow_html=True,
    )

    show_answer = b_show_answer.button("🔍 Show Answer 🔭")

    st.markdown(
        f"""
        <br>
            You have used these letters: {" ".join(hm.hm_used_letters)}
            Current word: {"".join(word_list)}
        <br>
        """,
        unsafe_allow_html=True,
    )
    holder1, holder2, holder3 = st.empty(), st.empty(), st.empty()
    user_letter = holder1.text_input(
        "Guess a letter:", max_chars=1, key=str(hm.hm_idxml_key + 1)
    ).upper()

    if (
        len(hm.hm_word_letters) > 0 and user_letter != ""
    ) and hm.hm_word:

        if user_letter in hm.hm_alphabet - hm.hm_used_letters:
            hm.hm_used_letters.add(user_letter)
            if user_letter in hm.hm_word_letters:
                hm.hm_word_letters.remove(user_letter)
                holder2.success("Good guess. Keep going!")
            else:
                holder2.error("Character is not in word. Try again!")

        elif user_letter in hm.hm_used_letters:
            holder2.info("You have already used that character. Try again!")

        elif user_letter not in hm.hm_alphabet and user_letter != "":
            holder2.error("Invalid character. Try again!")

    elif (
        len(hm.hm_word_letters) == 0 or show_answer
    ) and hm.hm_word:
        holder1.empty()

        if "".join(word_list) == hm.hm_word:
            holder1.success(
                f"\nCongratulations! You guessed the word [{hm.hm_word}] correctly!!"
            )
            st.balloons()
        else:
            holder3.error("Game over! Try again!")
            time.sleep(1)

    time.sleep(1)

    if user_letter != "":
        hm.hm_idxml_key += 1
        st.experimental_rerun()

    if show_answer:
        raise CheaterWarning('I think the player is a cheater LOL')

    st.sidebar.markdown("""___""")
    st.markdown("""___""")


class CheaterWarning(Exception):
    pass
if __name__ == "__main__":
    HangMan()