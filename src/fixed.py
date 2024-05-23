# -- coding: UTF-8 --
"""Import modules"""
from random import choice

from pandas import read_html, concat, to_datetime
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

    def __repr__(self):
        """Basic instance representation"""
        return "CDB Fixed Income"
    
    def __str__(self):
        """Print instance representation"""
        return "CDB Fixed Income"
        
    def _get_codes(_self, dataframe):
        """Get CDBS
        Codes"""
        
        return dataframe["code"]
    
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
                code = lambda x: x["Banco"].str.split("-").str[0]
            ).filter(["code", "Banco", "Liquidez", "Vencimento" ,"Rentabilidade",
                       "Aplicação Mínima", "Rende mais que a poupança?"])

        except Exception as error:
            raise OSError from error
        
        return cdbs_codes
    

class LCA(Fixed):
    """Bank Deposite 
    Certificates"""

    def __init__(self, name = "LCA"):
        
        self.config = Config()
        super().__init__(name)

    def __repr__(self):
        """Basic instance representation"""
        return "LCA Fixed Income"
    
    def __str__(self):
        """Print instance representation"""
        return "LCA Fixed Income"
        
    def _get_codes(self, dataframe):
        """Get LCA
        Codes"""
        return dataframe["code"]
    
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
                code = lambda x: x["Banco"].str.split("-").str[0]
            ).filter(["code", "Banco", "Liquidez", "Vencimento" ,"Rentabilidade",
                        "Aplicação Mínima", "Rende mais que a poupança?"])

        except Exception as error:
            raise OSError from error
        
        return lcas_codes
    
class DI():
    """Di Future 
    Contracts scrapping"""

    def __init__(self, name = "DI"):
        
        self.config = Config()

    def __repr__(self):
        """Basic instance representation"""
        return "Future DI Contracts"
    
    def __str__(self):
        """Print instance representation"""
        return "Future DI Contracts"
    
    @st.cache_data
    def get_dataframe(_self):
        """Get DI 
        Dataframes"""
        url = _self.config.vars.future_contracts_url
        chrome_options = Options()
        chrome_options.add_argument("--headless")  
        chrome_options.add_argument("--disable-gpu")  
        chrome_options.add_argument("--no-sandbox")
        try:
            driver = webdriver.Chrome(options = chrome_options)
            driver.get(url)
            
            table_di = driver.find_element(By.XPATH, 
                                        '//*[@id="principal"]').get_attribute("outerHTML")
            
            driver.quit()

            tabela_full = read_html(table_di, decimal = ",", thousands= ".")[1]
            
            for i in range(1,4):
                dados_final = concat([tabela_full, read_html(table_di, decimal = ",",
                                                                thousands= ".")[i]], 
                                                                axis = 1)
                
            dados_final.drop(['Gráfico', 'C/V', 'Preço Exerc.', 'Ajuste', 'Sit. Ajuste',
                                    'Taxa Ef.Período', 'Taxa Ef.Anual.(252)'],
                                        axis = 1, inplace = True)
            
            dados_final = dados_final.iloc[:-1]

            dados_final = dados_final.assign(
                Ajuste_Anterior = lambda x: x["Ajuste Anterior"].astype(float)
            )
            
            dados_final["Vecto."] = to_datetime(dados_final["Vecto."]).dt.date
            

        except Exception as error:
            raise OSError from error
        
        return dados_final
