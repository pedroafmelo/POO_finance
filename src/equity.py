# -- coding: UTF-8 --
"""Import modules"""
from random import choice

import streamlit as st
import yfinance as yf
from bs4 import BeautifulSoup
from cryptocmd import CmcScraper
from requests import get

from src.assets import Equity
from src.iface_config import Config


class Stock(Equity):
    """Stock Assets Class"""

    def __init__(self, name = "Stock"):

        self.config = Config()

        super().__init__(name)
        self.name = name

    def __repr__(self):
        """Basic instance representation"""
        return "Stock Assets Class"

    def __str__(self):
        """Print instance representation"""
        return "Stock Assets Class"
    
    def __eq__(self, other):
        if self.type == other.type:
            return True
        else: 
            return False
    
    def _get_codes(self) -> list:
        """Get B3 Stock Tickers"""

        url = self.config.vars.stock_tickers_url

        try:
            tickers = []
            response = get(url, 
                           headers={'User-Agent':
                                    choice(self.config._user_agent)})


            if not response.ok:
                raise FileNotFoundError("Couldn't request website")

            soup = BeautifulSoup(response.content, 'html.parser')
            strongs = soup.find_all('strong')


            for ticker in strongs:
                ticker = ticker.find("a")

                if ticker:
                    tickers.append(ticker.text)
        
        except Exception as error:
            raise OSError(error) from error

        return tickers

    @st.cache_data
    def get_dataframe(_self, company, start_date):
        """Get dataframe of closing
         stocks"""
    
        try:
            business = yf.Ticker(f"{company}.SA")
            ticker_df = business.history(period="1d", 
                                         start = start_date)

        except Exception as e:
            raise (f"An error occurred: {str(e)}")
        
        return ticker_df
    

class Crypto(Equity):
    """Crypto Class"""

    def __init__(self, name = "Crypto"):

        self.config = Config()

        super().__init__(name)

    def __repr__(self):
        """Basic instance representation"""
        return "Crypto Class"

    def __str__(self):
        """Print instance representation"""
        return "Crypto Class"
    
    def __eq__(self, other):
        if self.type == other.type:
            return True
        else: 
            return False
    
    def _get_codes(self) -> list:
        """Get Crypto Codes"""

        url = self.config.vars.crypto_tickers_url

        try:
            tickers = []
            response = get(url, 
                           headers={'User-Agent':
                                    choice(self.config._user_agent)})

            if not response.ok:
                raise FileNotFoundError("Couldn't request website")

            soup = BeautifulSoup(response.content, 'html.parser')
            crypto_code = soup.find_all("a", 
                                        class_ = "cmc-table__column-name--symbol cmc-link")
            crypto_name = soup.find_all("a", 
                                        class_ = "cmc-table__column-name--name cmc-link")
            
            tickers = [code.text for code in crypto_code]
            names = [name.text for name in crypto_name]

            coins = dict(zip(tickers, names))
        
        except Exception as error:
            raise OSError(error) from error

        return coins

    @st.cache_data
    def get_dataframe(_self, company, start_date):
        """Get dataframe of closing
         cryptos"""
    
        try:
            scraper = CmcScraper(company)
            dados_btc = scraper.get_dataframe()
            dados_btc = dados_btc.query("Date >= @start_date")

        except Exception as e:
            raise (f"An error occurred: {str(e)}")
        
        return dados_btc
