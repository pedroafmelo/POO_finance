import streamlit as st
import plotly_express as px
from pandas import DataFrame

class Quiz:
    """Interface Quiz Class"""

    def __init__(self):
        """Initialize Instance"""

        self.questions = 4

    def __repr__(self):
        """Basic instance representation"""
        return "Quiz class"
    
    def __str__(self):
        """Print instance representation"""
        return "Quiz class"
    
    def riskProfileQuiz(self):
        """Build quiz"""

        st.write("#")
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
            """I am willing to take risks in the long term because 
            I believe that in the long run the return will be higher.""",

            """Winning as much as possible is important to me, 
            even if there is a risk of losing part of the capital.""",

            """I prefer to see my investments growing steadily,
            without highs and lows, even if in the long run I have a lower return.""",

            """Avoiding losses this year is more important 
            than long-term growth. I want to protect my savings in the short term."""
        ]

        answers = {
            disagree:0,
            neutral:1,
            agree:3

        }

        c1, c2 = st.columns(2)

        # Ask questions and get responses
        profile_counter = 0
        for i, question in enumerate(questions):
            c1.write(question)
            answer = c1.selectbox('Answer:',
                                  answers.keys(), key=i, index=None)
            st.write("#")
            if answer:
                profile_counter += answers[answer]

        return profile_counter, c2
    
    def decide(self, profile_counter):
        """Choose the profile"""
        # Determine profile
        if profile_counter < 4:
            profile = "Conservative"
        elif profile_counter > 8:
            profile = "Aggressive"
        else:
            profile = "Moderate"

        return profile


    def plot_wallet(self, profile, column):

        data = {
                "Conservative":{'Renda Fixa': 60,
                                 'Fundos Imbobiliários': 25,
                                 "B3 Stocks": 10,
                                 "Crypto": 5},
                "Moderate": {'Renda Fixa': 45,
                             'Fundos Imbobiliários': 25,
                             "B3": 20,
                             "Crypto": 10},
                "Aggressive": {'Renda Fixa': 25,
                               'Fundos Imbobiliários': 20,
                               "B3": 35,
                               "Crypto": 20}
                }
        
        # Plotar o gráfico de pizza
        graph = px.pie(values = data[profile].values(), 
                       names = data[profile].keys(), 
                       title = f"                                          Wallet Distribuction:\n{profile}")

        graph.update_qlayout(
            height= 500,
            font_size = 15,
        )

        column.plotly_chart(graph)

        

