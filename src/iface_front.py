# -- coding: UTF-8 --
"""Import modules"""
from os import path
from pandas import DataFrame
import yfinance as yf
import json
import streamlit as st
from streamlit_extras.stylable_container import stylable_container 
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
from datetime import datetime
import matplotlib.pyplot as plt

from src.quiz import Quiz
from src.iface_config import Config
from src.iface_back import CompoundCalc, InvestRecomend
from src.fixed import CDB, LCA, DI
from src.equity import Stock, Crypto

class FrontEnd:
    """ Iface_frontend """
        
    def __init__(self):
        """ Initialize instance """

        self.config = Config()
        self.calc = CompoundCalc()
        self.invest = InvestRecomend()
        self.stock = Stock()
        self.crypto = Crypto()
        self.quiz = Quiz()
        self.cdb = CDB()
        self.lca = LCA()
        self.di = DI()
        self.filename = f"{self.config.vars.filename}{self.config.vars.extension}"

        self.logo_path = path.join(self.config.project_dir, "img", 
                                  self.config.vars.logo)
        
        self.calc_gif_path = path.join(self.config.project_dir, "img", 
                                  self.config.vars.calc_gif)
        
        self.file_path = path.join(self.config.project_dir, 
                               self.config.vars.data_dir,
                               self.filename)
        
    def __repr__(self):
        """Basic instance representation"""
        return "FrontEnd class"
    
    def __str__(self):
        """Print instance representation"""
        return "FrontEnd class"
        
    def basic_layout(self):
        """Streamlit Page Loayout"""

        st.set_page_config(self.config.vars.project_name,
                           page_icon = self.config.vars.project_icon,
                           layout = "wide")
        
        c1, c2, c3 = st.columns([5, 5, 5])
        
        lot = self.import_json(self.logo_path)

        with c1:
            st.lottie(lot, width = 170, height = 170)

        c1, c2, c3 = st.columns(3)

        c1.markdown(
            f"""
            <div style="padding-top: 0px; padding-bottom: 0px;">
                <h1 style="margin: 0; text-align: left;">{self.config.vars.project_name}</h1>
            </div>
            """,
            unsafe_allow_html=True
)    
        st.markdown("""<h4 style = 'color: grey;'>Investment Control</h4>""",
            unsafe_allow_html= True)
    
        st.markdown("""<hr style="height:2px;border:none;color:grey;background-color:red;" /> """,
                unsafe_allow_html=True)
        
        st.write("#")
        st.write("#")


    def menu(self):
        """Streamlit nav menu"""

        selector = option_menu(
            menu_title = "",
            options = ["Calculator", "Equity", "Fixed Income","Quiz"],
            default_index = 0,
            icons = ["calculator", "cash-coin", "piggy-bank", "question"],
            orientation = "horizontal",
            styles = {
                "container": {"padding": "0!important", 
                              "background-color": "#FF708E"},

                "icon": {"color": "white", "font-size": "20px"}, 

                "nav-link": {"font-size": "20px", "text-align": "center", 
                             "margin":"0px", "--hover-color": "#eee"},

                "nav-link-selected": {"background-color": "#FF0000"},
            }
    )
        if selector == "Calculator":
            st.write("#")
            self.compound_calc()

        elif selector == "Equity":
            st.write("#")
            st.spinner("Loading your wallet")
            self.invest_rec()
            c1, c2, c3, c4 = st.columns([3, 2, 2, 2])
            c1.header("Assets closing prices historic")
            c1.write('#')
            c4.write("#")
            #crypto = c4.toggle("Crypto")
            #if not crypto: 
            c1.subheader("Stocks")
            self.stock_hist_closing()
            # else:
                # c1.subheader("Crypto")
                # self.crypto_hist_closing()

        elif selector == "Fixed Income":
            c1, c2 = st.columns(2)
            c1.write("#")
            c1.write("#")
            c2.write("#")
            c2.write("#")

            self.cdbs(c1)
            self.lcas(c2)
            #self.compare_fixed()

        elif selector == "Quiz":
            with st.form("Quiz", border = False):
                counter,column = self.quiz.riskProfileQuiz()
                submit_button = st.form_submit_button("Done")

            if submit_button:
                profile = self.quiz.decide(counter)
                if profile:
                    self.quiz.plot_wallet(profile, column)


    def import_json(self, path):
        """Load json files"""

        with open(path, "r", encoding="utf8", errors="ignore") as file:
            url = json.load(file)
        return url


    def compound_calc(self):
        """Call compound calc class
        prints number"""
        

        st.header("Compound Interest Calculator")
        st.write("#")

        col1, col2 = st.columns(2)

        time = int(col1.number_input("Please, enter the time of your application (years): ", 
                                     min_value = 0, max_value= 50, format = "%i"))

        init = float(col1.number_input("Please, enter your initial contribution: ", 
                                       0, step = 100, format = "%i"))
        
        month_fee = float(col2.number_input("Please, enter the monthly fee: ",
                                            0.0, step = 0.10)) 
        
        cont = float(col2.number_input("Now enter your monthly contribution: ",
                                       0, step = 100, format = "%i"))

        result = self.calc.calculator(time, init, month_fee, cont)

        col1.write("#")

        if init or cont:
            with stylable_container(
                key="container_with_border",
                css_styles="""
                    {
                        border: 3px solid rgba(49, 51, 63, 0.2);
                        border-radius: 0.5rem;
                        padding: calc(1em - 1px)
                    }
                    """,
            ):  
                st.markdown(f"""<h4 style= 'text-align: left; color: white;'
                        >The Compound Interest works for you! 
                            After {time} year(s), you would have an 
                            amount of ${result:.2f}</h4>""", unsafe_allow_html= True)
                

        if not cont:

            c1, c2, c3 = st.columns([1, 5, 1])
            co1, co2, co3 = c2.columns(3)
                
            lot2 = self.import_json(self.calc_gif_path)

            with co2:
                st.lottie(lot2, width = 300, height = 300)
            
        elif cont:
            st.write("#")
            st.write("#")
            graph_result = self.calc.get_simulation()
            dados = DataFrame(graph_result)
            st.line_chart(dados,  x = "Month", 
                          y = ["With Compound Interest", "Without Compound Interest"],
                          color = ["#FF0000", "#FF708E"])
            

    @st.cache_data
    def invest_rec(_self):
        """Call invest recommend class
        prints table"""

        c1, c2 = st.columns([4, 3])

        chosen_tickers = _self.invest._portfolio_management(_self.invest.fund_tickers())

        c1.header(f"Top 5 Stocks to Invest in B3 today")

        c1.write("#")

        with stylable_container(
                key="container_with_border",
                css_styles="""
                    {
                        border: 3px solid rgba(49, 51, 63, 0.2);
                        border-radius: 0.5rem;
                        padding: calc(1em - 1px)
                    }
                    """
            ):
                columns = st.columns(5)
                
                for index, ticker in enumerate(chosen_tickers):
                    company = yf.Ticker(ticker)
                    company_name = company.info.get('longName', 'N/A')
                    area = company.info.get('industryDisp', 'N/A')
                    price = company.info.get('currentPrice', 'N/A')

                    columns[index].markdown(f"""<h3 style= 'text-align: left; color: white;'
                                >Ticker: {ticker.replace(".SA", "")}</h3>""", unsafe_allow_html = True)
                    columns[index].write(f"Company: \n {company_name}")
                    columns[index].write(f"Market : \n{area}")
                    columns[index].write(f"Current Price: \n{price}")
        
        st.write("#")
        st.write("#")


    def stock_hist_closing(self):
        """Print historical assets 
        closing prices"""

        st.write("#")

        c1, c2, c3 = st.columns([1, 1, 1])

        tickers = self.stock._get_codes()

        ticker = c1.selectbox("Choose the B3 Ticker", 
                              tickers,
                              index = tickers.index("PETR4"))
        c1.write("#")
        
        if ticker:
            second_tickers = tickers.copy()
            second_tickers.remove(ticker)

            second_ticker_select = c2.selectbox(
                "Choose the second B3 Ticker",
                second_tickers,
                index=None
            )
            c2.write("#")

            if not second_ticker_select:
                time = c3.selectbox(
                    "Choose the timestamp",
                    ['1 year','6 months','1 month','5 years'],
                )
                c3.write("#")
                first_company = yf.Ticker(f"{ticker}.SA")
                first_ticker_df = first_company.history(period="1d", start=self.stock.get_dates(time),
                                                         end=datetime.now().strftime("%Y-%m-%d"))
                st.spinner("Loading...")

                if first_company.info is None:
                    st.error("Invalid Ticker Symbol or Company not listed")
                else:
                    company_name = first_company.info.get('longName', 'N/A')
                    area = first_company.info.get('industryDisp', 'N/A')
                    price = first_company.info.get('currentPrice', 'N/A')
                    c1, c2, c3 = st.columns([1, 1, 1])
                    c1.write(f"Company: {company_name}")
                    c2.write(f"Market Area: {area}")
                    c3.write(f"Current Price: {price}BRL")

                st.line_chart(first_ticker_df.Close, color ='#FF0000')
            
            if second_ticker_select:

                time = c3.selectbox(
                    "Choose the timestamp",
                    ['1 year','6 months','1 month','5 years'],
                )
                c3.write("#")

                try:
                    first_company = yf.Ticker(f"{ticker}.SA")
                    second_company = yf.Ticker(f"{second_ticker_select}.SA")
                    first_ticker_df = first_company.history(period="1d", 
                                                            start=self.stock.get_dates(time),
                                                            end=datetime.now().strftime("%Y-%m-%d"))
                    second_ticker_df = second_company.history(period="1d", 
                                                              start=self.stock.get_dates(time),
                                                              end=datetime.now().strftime("%Y-%m-%d"))
                    combined_df = DataFrame({
                        f"{ticker}": first_ticker_df['Close'],
                        f"{second_ticker_select}": second_ticker_df['Close']
                    })

                    st.spinner("Loading...")

                    if first_company.info is None and second_company is None:
                        st.error("Invalid Ticker Symbol or Company not listed")
                    else:
                        first_company_name = first_company.info.get('longName', 'N/A')
                        first_area = first_company.info.get('industryDisp', 'N/A')
                        first_price = first_company.info.get('currentPrice', 'N/A')
                        second_company_name = second_company.info.get('longName', 'N/A')
                        second_area = second_company.info.get('industryDisp', 'N/A')
                        second_price = second_company.info.get('currentPrice', 'N/A')

                        st.write("#")
                        c1, c2, c3, c4 = st.columns([1, 1, 1, 1])
                        col1,col2,col3 = c1.columns([1,2,1])
                        col2.write(f"Ticker: {ticker}")
                        c2.write(f"Company: {first_company_name}")
                        c3.write(f"Market Area: {first_area}")
                        c4.write(f"Current Price: {first_price}BRL")

                        st.divider()

                        c5, c6, c7, c8 = st.columns([1, 1, 1, 1])
                        col4,col5,col6 = c5.columns([1,2,1])
                        col5.write(f"Ticker: {second_ticker_select}")
                        c6.write(f"Company: {second_company_name}")
                        c7.write(f"Market Area: {second_area}")
                        c8.write(f"Current Price: {second_price}BRL")

                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

                st.write("#")
                st.line_chart(combined_df, color =['#0000FF', '#FF0000'])
        

    def crypto_hist_closing(self):
        """Print historical assets 
        closing prices"""

        st.write("#")

        c1, c2, c3 = st.columns([1, 1, 1])

        ticker = c1.selectbox("Choose the Coin Ticker", 
                              self.crypto._get_codes().keys(),
                              index = 0)
        

        time = c2.selectbox("Choose a timestamp",
                            ["1 month", "6 months", 
                             "1 year", "5 years"],
                             index = 2)
        
        time = self.crypto.get_dates(time)
        
        try:

            ticker_df = self.crypto.get_dataframe(ticker, time)

            with st.spinner("Loading..."):
                if len(ticker_df) != 0:
                    c1, c2, c3 = st.columns([1, 1, 1])
                    c1.write("#")
                    c1.write(f"Coin: {self.crypto._get_codes()[ticker]}")
                    c1.write("#")
                    st.line_chart(data=ticker_df.set_index("Date")["Close"])

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
        

    def cdbs(self, column):
        """Print the CDBS
        avaiable in Info Money"""
        
        column.header("CDBS avaiable in XP Investments")

        column.write("#")

        dados = self.cdb.get_dataframe().drop("code", axis = 1)

        column.dataframe(dados, hide_index= True)


    def lcas(self, column):
        """Print the CDBS
        avaiable in Info Money"""

        col1, col2, col3 = st.columns(3)
        
        column.header("LCAS avaiable in XP Investments")

        column.write("#")

        dados = self.lca.get_dataframe().drop("code", axis = 1)

        column.dataframe(dados, hide_index= True)

        column.write("#")
        column.write("#")

        col3.link_button("Investir", "https://www.xpi.com.br/")


    def compare_fixed(self):
        """Compare the selected
        asset with the DI curl"""

        st.write("#")

        cdb_df = self.cdb.get_dataframe()
        lca_df = self.lca.get_dataframe()
        di_df = self.di.get_dataframe()

        # c1, c2, c3 = st.columns(3)

        # ticker = c1.selectbox("Choose the Fixed Income Ticker", 
        #                       self.cdb._get_codes(cdb_df),
        #                       index = 0)
        
        # try:

        # st.spinner("Loading...")

        # if len(cdb_df) != 0:
        
        #     c1, c2, c3 = st.columns([1, 1, 1])
        #     c1.write("#")
        #     c1.write(f"Fixed Income: {ticker}")
        #     c1.write("#")

        # except Exception as e:
        #     st.error(f"An error occurred: {str(e)}")

        st.header("DI Future Contracts")
        st.write("#")

        st.dataframe(di_df, hide_index= True)
        
        # st.line_chart(data = di_df,
        #               x = "Vecto.", y = "Ajuste_Anterior",
        #               color = "#FF0000")
        
        # combined_df = DataFrame({
        #         f"{ticker}": first_ticker_df['Close'],
        #         f"{second_ticker_select}": second_ticker_df['Close']
        #             })