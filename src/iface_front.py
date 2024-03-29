# -- coding: UTF-8 --
"""Import modules"""
from os import path
from pandas import DataFrame, set_option
import yfinance as yf
import json
import streamlit as st
from streamlit_extras.stylable_container import stylable_container 
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie


class FrontEnd:
    """ Iface_frontend """
        
    def __init__(self):
        """ Initialize instance """

        # Import config, back end iface
        from src.iface_config import Config
        from src.iface_back import CompoundCalc, InvestRecomend

        self.config = Config()
        self.calc = CompoundCalc()
        self.invest = InvestRecomend()
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
            options = ["Calculator", "Assets"],
            default_index = 0,
            icons = ["calculator", "coin"],
            orientation = "horizontal",
            styles = {
                "container": {"padding": "0!important", "background-color": "#FF708E"},
                "icon": {"color": "white", "font-size": "20px"}, 
                "nav-link": {"font-size": "20px", "text-align": "center", "margin":"0px", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "#FF0000"},
            }
    )
        if selector == "Calculator":
            st.write("#")
            self.compound_calc()

        elif selector == "Assets":
            st.write("#")
            st.spinner("Loading your wallet")
            self.invest_rec()
            self.hist_closing()


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

        set_option('display.html.table_schema', True)

        c1, c2 = st.columns([4, 3])

        _self.invest._extract_data()

        data = _self.invest._transform(_self.file_path)

        c1.header(f"Top {data.shape[0]} B3 Assets to Invest Today")

        c1.write("#")
        c1.dataframe(data, use_container_width= True, 
                     hide_index = True)
        c1.write("#")

        c2.write("#")
        c2.write("#")
        c2.write("#")

        col1, col2, col3 = c2.columns([1,4,1])


        with col2.expander("Cotação"):
            st.write("This is the price of that asset in the present moment")

        col2.write("#")

        with col2.expander("roic"):     
            st.write("""This is the Return on Invested Capital, an 
                        indicator that shows the rentability of that asset""")
        col2.write("#")

        with col2.expander("ev_ebit"): 
            st.write("""This is the Enterprise Value over 
                        the Earnings Before Interest and Taxes, that 
                        shows the company profit after all discounts """)
        col2.write("#")

        with col2.expander("preco_valor_patrimonial"):
            st.write("""This indicator shows the price of that asset over
                        the patrimonial value of that company, which can be a great price indicator""")


    def hist_closing(self):
        """Print historical assets 
        closing prices"""

        st.header("B3 assets closing prices historic")
        st.write("#")

        ticker = st.selectbox("Choose the B3 Ticker", 
                              self.invest._get_tickers(), 
                              self.invest._get_tickers().index("PETR4"))

        
        try:
            company = yf.Ticker(f"{ticker}.SA")
            ticker_df = company.history(period="1d", start="2023-01-01", end="2024-02-29")

            st.spinner("Loading...")

            if company.info is None:
                st.error("Invalid Ticker Symbol or Company not listed")
            else:
                company_name = company.info.get('longName', 'N/A')
                area = company.info.get('industryDisp', 'N/A')
                price = company.info.get('currentPrice', 'N/A')
        
                c1, c2, c3 = st.columns([1, 1, 1])
                c1.write(f"Company: {company_name}")
                c2.write(f"Market Area: {area}")
                c3.write(f"Current Price: {price}BRL")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
        
        

        st.line_chart(ticker_df.Close, color = "#FF0000")
