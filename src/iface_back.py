# -- coding: UTF-8 --
"""Import modules"""
import yfinance as yf
from pandas_datareader import data as web
from pandas import DataFrame
from src.iface_config import Config
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
import streamlit as st
import riskfolio as rp

from src.iface_config import Config

yf.pdr_override()

class Calculator(ABC):
    """ Calculator Class """
    
    @abstractmethod
    def sum_numbers(self, *nums):
        """Basic args sum"""
        pass

    @abstractmethod
    def subtract(self, num1, num2):
        """Basic args subtract"""
        pass
    
    @abstractmethod
    def times(self,*nums):
        """Basic args multiplying"""
        pass
            

class CompoundCalc(Calculator):
    """ Compound Interest Calc class """

    def _init_(self) -> int:
        """Initialize instance"""
        
        self.simulation = None
        self.state = False

    def __repr__(self):
        """Basic instance representation"""
        return "Compound Interest Calculator"
    
    def __str__(self):
        """Print instance representation"""
        return "Compound Interest Calculator"
    
    def sum_numbers(self, *nums):
        """Basic args sum"""
        result = sum(nums)

        return result

    def subtract(self, num1, num2):
        """Basic args subtract"""

        return num1 - num2
    
    def times(self, *nums):
        """Basic args multiplying"""
        for i, value in enumerate(nums):
            result = value[i] * value[i+1]
        
        return result

    def calculator(self, years: int, initial_cont: float, 
                  fee: float, monthly_cont: float) -> int:
        
        """Calculate the mountant after investment"""
        
        fee = fee / 100
        months = []
        amounts = []
        no_fee_amount = []
        total_amount = 0
        amount_no_fee = initial_cont

        m = initial_cont  # Initialize the total amount

        for month in range(1, years * 12 + 1):

            m = m * (1 + fee) + monthly_cont# Compound interest formula
            amount_no_fee += monthly_cont
            months.append(int(month))
            amounts.append(m)
            no_fee_amount.append(amount_no_fee)


        total_amount = m 
        self.simulation = {"Month": months, "With Compound Interest": amounts, 
                           "Without Compound Interest": no_fee_amount}
        self.state = True

        return total_amount  # Compound interest formula

    def get_simulation(self) -> dict:
        if self.state:
            return self.simulation

class InvestRecomend:
    """ Investiment recomendation class """

    def __init__(self):
        """Initialize instance
        actions_qt: number of assets to be recommended"""

        self.config = Config()
        self.tickers = Config().bova11
        
    def __repr__(self):
        """Basic instance representation"""
        return "Invest Recommend Class"
    
    def __str__(self):
        """Print instance representation"""
        return "Invest Recommend Class"

    @st.cache_data
    def fund_tickers(_self) -> DataFrame:
        """Extract table from 
        Fundamentus website"""
        yf.pdr_override()
        
        pattern = "%Y-%m-%d"
        inicial_date = datetime.now() - timedelta(days = 365 * 5)
        inicial_date = inicial_date.strftime(pattern) 
        final_date = datetime.now()

        # try:
        tickers_yahoo = [ticker + '.SA' for ticker in _self.tickers]
        dados_tickers = web.get_data_yahoo(tickers_yahoo, 
                                        start = inicial_date, end = final_date)
        variation_df = dados_tickers['Adj Close'].pct_change()
        variation_df = variation_df[1:].dropna(axis = 1)

        # except NameError:
        #     raise OSError("Could not download Tickers")
        
        return variation_df


    def _portfolio_management(self, dataframe):

        """Portfolio Management"""

        portfolio = rp.Portfolio(returns = dataframe) 

        metodo_mu = 'hist' # method to calculate the future returns based on historical returns
        metodo_cov = 'hist' # method to calculate the cov matrix based on the historical returns

        portfolio.assets_stats(method_mu = metodo_mu, method_cov = metodo_cov, d = 0.94)

        model='Classic' # Markowitz Classic Model
        rm = 'MV' # Risk measure: mean-variance
        obj = 'Sharpe' # Main objective: Maximize Sharpe

        wallet = portfolio.optimization(model = model, rm = rm, obj = obj)

        top_5_tickers = wallet.sort_values(by='weights', ascending=False).head(5)
        top_5 = dataframe[top_5_tickers.index.tolist()]
        
        return top_5