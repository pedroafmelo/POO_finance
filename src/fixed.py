# -- coding: UTF-8 --
"""Import modules"""
from random import choice

from pandas import read_html
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import streamlit as st

from src.iface_config import Config
from src.assets import Fixed


class CDB(Fixed):
    """Bank Deposite 
    Certificates"""

    def __init__(self, name = "CDB"):
        
        self.config = Config()
        super().__init__(name)
        
    def _get_codes(self):
        """Get CDBS
        Codes"""
        return self.bancos 
    
    @st.cache_data
    def get_dataframe(_self):
        """Get CDBS 
        Dataframes"""
        url = _self.config.vars.cdbs_tickers_url
        chrome_options = Options()
        chrome_options.add_argument("--headless")  
        chrome_options.add_argument("--disable-gpu")  
        chrome_options.add_argument("--no-sandbox")
        try:
            driver = webdriver.Chrome(options = chrome_options)
            driver.get(url)
            
            cdbs = driver.find_element(By.XPATH, 
                                        "//*[@id='DataTables_Table_0']").get_attribute("outerHTML")
            
            driver.quit()
            
            cdbs = read_html(cdbs, thousands=".", decimal = ",")[0].drop("Unnamed: 8", axis = 1)

            cdbs_codes = cdbs.assign(
                code = lambda x: x["Banco"].str.split().str[1]
            ).filter(["code", "Banco", "Liquidez", "Vencimento" ,"Rentabilidade",
                       "Aplicaçãp Mínima", "Rende mais que a poupança?"])

            _self.bancos = cdbs_codes["code"].unique()

        except Exception as error:
            raise OSError from error
        
        return cdbs_codes
    

class LCA(Fixed):
    """Bank Deposite 
    Certificates"""

    def __init__(self, name = "LCA"):
        
        self.config = Config()
        super().__init__(name)
        
    def _get_codes(self):
        """Get LCA
        Codes"""
        return self.bancos_agro
    
    @st.cache_data
    def get_dataframe(_self):
        """Get LCA
        Dataframes"""

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")

        url = _self.config.vars.cdbs_tickers_url

        try:
            driver = webdriver.Chrome(options = chrome_options)
            driver.get(url)
            
            lcas = driver.find_element(By.XPATH,
                    "//*[@id='DataTables_Table_1']").get_attribute("outerHTML")
            
            driver.quit()
            
            lcas = read_html(lcas, thousands=".", decimal = ",")[0].drop("Unnamed: 8", axis = 1)

            lcas_codes = lcas.assign(
                code = lambda x: x["Banco"].str.split().str[1]
            ).filter(["code", "Banco", "Liquidez", "Vencimento" ,"Rentabilidade",
                        "Aplicaçãp Mínima", "Rende mais que a poupança?"])

            _self.bancos_agro = lcas_codes["code"].unique()

        except Exception as error:
            raise OSError from error
        
        return lcas_codes