import streamlit as st

def riskProfileQuiz():
    st.header("Risk Profile Quiz")
    st.write("#")
    st.subheader("Answer this quiz to map your investor profile.")
    st.write("#")
    # Constants for responses
    agree = "agree"
    disagree = "disagree"
    neutral = "neutral"

    # Questions and answers
    questions = [
        "I am willing to take risks in the long term because I believe that in the long run the return will be higher.",
        "Winning as much as possible is important to me, even if there is a risk of losing part of the capital.",
        "I prefer to see my investments growing steadily, without highs and lows, even if in the long run I have a lower return.",
        "Avoiding losses this year is more important than long-term growth. I want to protect my savings in the short term."
    ]

    answers = {
        disagree:0,
        neutral:1,
        agree:3

    }

    # Ask questions and get responses
    profile_counter = 0
    for i, question in enumerate(questions):
        st.write(question)
        answer = st.selectbox('Answer:',answers.keys(), key=i, index=None)
        st.write("#")
        if answer:
            profile_counter += answers[answer]

    # Determine profile
    if profile_counter < 4:
        profile = "Conservative."
    elif profile_counter > 8:
        profile = "Aggressive."
    else:
        profile = "Moderate."

    return profile
