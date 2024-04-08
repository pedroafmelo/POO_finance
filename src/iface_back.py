# -- coding: UTF-8 --
"""Import modules"""
import yfinance as yf
from os import path, makedirs
from pandas import read_csv, read_html, DataFrame
from bs4 import BeautifulSoup
from requests import get
import random
from abc import ABC, abstractmethod

class Calculator(ABC):
    """ Calculator Class """

    @abstractmethod
    def __repr__(self):
        """Basic instance representation"""
        pass
    
    @abstractmethod
    def __str__(self):
        """Print instance representation"""
        pass
    
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
            

#class Calculator(ABC):
#    """ Calculator Class """
#
#    def __repr__(self):
#        """Basic instance representation"""
#        return "Regular Calculator"
#    
#    def __str__(self):
#        """Print instance representation"""
#        return "Regular Calculator"
#    
#    def sum_array(self, *nums):
#        """Basic args sum"""
#        result = sum(nums)
#
#        return result
#
#    def subtract(self, num1, num2):
#        """Basic args subtract"""
#
#        return num1 - num2
#    
#    def times(self,*nums):
#        """Basic args multiplying"""
#        for i, value in enumerate(nums):
#            result = value[i] * value[i+1]
            

class CompoundCalc(Calculator):
    """ Compound Interest Calc class """


    def __init__(self) -> int:

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
    
    def times(self,*nums):
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

        # Import config iface
        from src.iface_config import Config

        self.config = Config()
        self.filename = f"{self.config.vars.filename}{self.config.vars.extension}"

        self.file_path = path.join(self.config.project_dir, 
                               self.config.vars.data_dir,
                               self.filename)
        
        self.data_dir = path.join(self.config.project_dir, 
                      self.config.vars.data_dir)
        
        makedirs(self.data_dir, 
                 exist_ok = True)

    def _extract_data(self) -> DataFrame:
        """Extract table from 
        Fundamentus website"""

        try:
            response = get(self.config.vars.data_url, 
                           headers={'User-Agent': random.choice(self.config._user_agent)})
            if not response.ok:
                raise FileNotFoundError("Couldn't request website")
            soup = BeautifulSoup(response.content, "html.parser")

            table_content = soup.find("table", 
                                      class_ = "resultado rowstyle-par colstyle-col no-arrow")
            if table_content is None:
                raise PermissionError("Can't have access to the server")

            dados = read_html(str(table_content), 
                                 encoding = "utf-8",
                                 thousands = ".", 
                                 decimal = ",")[0].to_csv(self.file_path,
                                                          index = False,
                                                          compression = "gzip")

        except Exception as error:
            raise OSError(error) from error

        return dados
    

    def _get_tickers(self) -> list:
        """Get B3 Tickers"""

        try:
            tickers = []
            response = get(self.config.vars.tickers_url, 
                           headers={'User-Agent':random.choice(self.config._user_agent)})


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
    

    def _transform(self, filename: str, qt_asset: int = 10) -> DataFrame:

        """Transform companies data"""

        try:
            
            dados = (

                read_csv(filename, 
                         usecols = self.config.columns,
                         encoding = "utf-8")

                .rename(columns = lambda x: x.lower())
                .rename(columns = {"liq.2meses": "liq_2_meses", 
                                       "ev/ebit": "ev_ebit",
                                       "p/vp": "preco_valor_patrimonial",
                                       "pl": "preco_lucro"})
                .assign(
                    roic = lambda x: x["roic"].str.replace(".", "")
                    .str.replace(",", ".").str.replace("%", "").astype(float),
                )
                .assign(
                    ebit_ev = lambda x: x["ev_ebit"].apply(lambda y: 1/y if y != 0 else 0),
                    ranking_evebit = lambda x: x["ebit_ev"].rank(ascending = False),
                    ranking_roic = lambda x: x["roic"].rank(ascending = False),
                    ranking_geral = lambda x: x["ranking_evebit"] + x["ranking_roic"],
                    ranking_final = lambda x: x["ranking_geral"].rank(),
                    ranking = lambda x: x["ranking_geral"].rank()
                )
                .drop(["ranking_evebit", "ranking_roic", "ranking_geral", "ranking_final", "ev_ebit"], axis = 1)
                .sort_values("ranking")
                .query("ranking <= 10")

            )

        except Exception as error:
            raise OSError(error) from error
        
        
        return dados
