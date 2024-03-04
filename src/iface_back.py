# -- coding: UTF-8 --
"""Import modules"""
import yfinance as yf
from os import path
import pandas as pd
from bs4 import BeautifulSoup
from requests import get
import random


class CompoundCalc:
    """ Compound Interest Calc class """

    def _init_(self) -> int:
        """Initialize instance"""
        self.simulation = None
        self.state = False

    def _repr_(self):
        """Basic instance representation"""
        return "Compound Interest Calculator"
    
    def _str_(self):
        """Print instance representation"""
        return "Compound Interest Calculator"

    def __calculator(self, years: int, initial_cont: float, 
                  fee: float, monthly_cont: float) -> int:
        
        """Calculate the mountant after investment"""
        
        fee = fee / 100
        months = [''.join([str(1),'º Mês'])]
        amounts = [initial_cont]

        if monthly_cont:
            m = initial_cont  # Initialize the total amount

            for month in range(1, years * 12 + 1):

                m = m * (1 + fee) + monthly_cont  # Compound interest formula
                months.append(''.join([str(month),'º Mês']))
                amounts.append(m)

            ganho_com_juros = m - initial_cont
            self.simulation = dict(zip(months, amounts))
            self.state = True

        return ganho_com_juros
    
    def get_simulation(self) -> dict:
        if self.state:
            return self.simulation
    

class InvestRecomend:
    """ Investiment recomendation class """


    def _init_(self):
        """Initialize instance
        actions_qt: number of assets to be recommended"""

        # Import config iface
        from src.iface_config import Config

        self.config = Config()

    def __extract_data(self) -> pd.DataFrame:
        """Extract table from 
        Fundamentus website"""

        try:
            response = get(self.config.vars.data_url, headers={'User-Agent': random.choice(self.config.user_agent)})
            if not response.ok:
                raise FileNotFoundError("Couldn't request website")
            soup = BeautifulSoup(response.content, "html.parser")

            table_content = soup.find("table", class_ = "resultado rowstyle-par colstyle-col no-arrow")
            if table_content is None:
                raise PermissionError("Can't have access to the server")

            dados = pd.read_html(str(table_content), 
                        thousands = ".", 
                        decimal = ",")[0].to_csv(path.join(self.config.vars.data_dir), 
                                              thousands = ".", 
                                              decimal = ",",
                                              compression = "gzip")

        except Exception as error:
            raise OSError(error) from error

        return dados
    
    def __get_tickers(self) -> list:

        try:
            tickers = []
            response = get(self.config.vars.tickers_url, headers={'User-Agent':random.choice(self.config.__user_agent)})

            if not response.ok:
                raise FileNotFoundError("Couldn't request website")

            soup = BeautifulSoup(response.content, 'html.parser')
            strongs = soup.find_all('strong')

            for a in strongs:
                ticker = a.find(a)

                if ticker:
                    tickers.append(ticker.text)
        
        except Exception as error:
            raise OSError(error) from error

        return tickers
    
    def __transform(self, filename: str, qt_asset: int = 10) -> pd.DataFrame:
        """Transform companies data"""

        try:

            dados = (
                pd.read_csv(filename, 
                            usecols = self.config.columns,
                            index_col = "Papel")
                    .rename(columns = lambda x: x.lower())
                    .rename(columns = {"liq.2meses": "liq_2_meses", 
                                       "ev/ebit": "ev_ebit"})
                    .assign(
                        roic = lambda x: x["roic"].str.replace(".", "")
                        .str.replace(",", ".").str.replace("%", "").astype(float),
                    )
                    .query("(roic > 0) and (ev_ebit > 0) and (liq_2_meses > 1000000)")
                    .assign(
                        ranking_evebit = lambda x: x["ev_ebit"].rank(),
                        ranking_roic = lambda x: x["roic"].rank(ascending = False),
                        ranking_geral = lambda x: x["ranking_evebit"] + x["ranking_roic"],
                        ranking_final = lambda x: x["ranking_geral"].rank(),
                        ranking = lambda x: x["ranking_geral"].rank()
                    )
                .sort_values("ranking")
                .query("ranking <= qt_asset")
                .filter(["cotação", "roic", "ranking"])
            )


        except Exception as error:
            raise OSError(error) from error
        
        
        return dados