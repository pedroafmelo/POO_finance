# -- coding: UTF-8 --
"""Import modules"""
import streamlit as st
import yfinance as yf

class FrontEnd:
    """ Iface_frontend """
        
    def _init_(self):
        """ Initialize instance """

        # Import config, back end iface
        from iface_config import Config
        import iface_back as back

        self.config = Config()
        self.calc = back.CompoundCalc()
        self.invest = back.InvestRecomend()
        
    def basic_layout(self):
        """Streamlit Page Loayout"""
        st.set_page_config(self.config.vars.project_name,
                           page_icon = self.config.vars.project_icon,
                           layout = "wide")
        
        st.title(self.config.vars.project_name)
        st.markdown("""<h5 style = 'color: grey;'>Investment Control</h5>""",
            unsafe_allow_html= True)
    
        st.markdown("""<hr style="height:2px;border:none;color:grey;background-color:red;" /> """,
                unsafe_allow_html=True)


    def compound_calc(self):
        """Call compound calc class
        prints number"""
        time = st.slider("Please, enter the time of your application (years): ", 1, 50)
        init = float(st.number_input("Please, enter your initial contribution: "))
        month_fee = float(st.number_input("Please, enter the monthly fee: ")) / 100
        cont = float(st.number_input("Now enter your monthly contribution: "))

        result = self.calc.__calculator(time, init, month_fee, cont )

        st.write(f"Awesome! At the end of {time} years, you will have an amount of R$ {result:.2f}")
        
        return 
    
    @st.cache_data
    def invest_rec(self, filename: str):
        """Call invest recommend class
        prints table"""

        row_data = self.invest.__extract_data

        data = self.invest.__transform(self.config.vars.df_dir)

        st.header("Top 10 B3 Assets to Invest Today")

        st.write("#")

        st.dataframe(data)

    def hist_return(self):
        



    def main(self):
        self.basic_layout()
        self.compound_calc()
        self.invest_rec()



if __name__ == "_main_":
    main = FrontEnd()
    main.main()