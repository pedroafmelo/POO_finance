# -- coding: UTF-8 --
"""Import modules"""
from random import choice
from abc import ABC, abstractmethod
from datetime import datetime, timedelta

import streamlit as st
import yfinance as yf
from bs4 import BeautifulSoup
from pandas import read_html
from requests import get
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from src.iface_config import Config

class Asset(ABC):
    """Assets Abstract Class
    Defines methods and attrs for henritage"""

    def __init__(self, name):
        self.name = name
        pass
        
    def __repr__(self):
        """Basic instance representation"""
        return "Assets Abstract Class"

    def __str__(self):
        """Print instance representation"""
        return "Assets Abstract Class"
    
    @abstractmethod
    def get_dates(self, time):
        """Get Dates bases 
        on user input"""
        pass

class Equity(Asset, ABC):
    """Assets Abstract Class
    Defines methods and attrs for henritage"""

    def __init__(self, name: str):
        
        super().__init__(name)
        self.config = Config()
        self.name = name
        
    def __repr__(self):
        """Basic instance representation"""
        return "Assets Abstract Class"

    def __str__(self):
        """Print instance representation"""
        return "Assets Abstract Class"
    
    @abstractmethod
    def _get_codes(self):
        """Get Equity 
        codes"""
        pass

    @abstractmethod
    def get_dataframe(self):
        """Get Equity
        Dataframes"""
        pass
    
    def get_dates(self, time):
        """Get Dates bases 
        on user input"""

        pattern = "%Y-%m-%d"

        times = {
            '1 year':timedelta(days=365),
            '5 years':timedelta(days=365 * 5),
            '1 month':timedelta(days=30),
            '6 months':timedelta(days=30*6)
        }

        date = datetime.now() - times[time]

        return date.strftime(pattern) 
    
class Fixed(Asset, ABC):
    """Fixed Assets Class"""

    def __init__(self, name: str):
            
            self.config = Config()
            super().__init__(name)

    def __repr__(self):
        """Basic instance representation"""
        return "Fixed Assets Class"

    def __str__(self):
        """Print instance representation"""
        return "Fixed Assets Class"
    
    def __eq__(self, other):
        if self.type == other.type:
            return True
        else: 
            return False
        
    @abstractmethod
    def _get_codes(self):
        """Get Equity 
        codes"""
        pass

    @abstractmethod
    def get_dataframe(self):
        """Get Equity
        Dataframes"""
        pass
    
    def get_dates(self, time):
        """Get Dates bases 
        on user input"""

        pattern = "%Y-%m-%d"

        times = {
            '1 year':timedelta(days=365),
            '5 years':timedelta(days=365 * 5),
            '1 month':timedelta(days=30),
            '6 months':timedelta(days=30*6)
        }

        date = datetime.now() - times[time]

        return date.strftime(pattern) 