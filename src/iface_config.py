from dataclasses import dataclass
from yaml import load
from yaml.loader import SafeLoader
from os.path import join, dirname, abspath

@dataclass
class Variables:

    project_name: str
    project_icon: str
    data_dir: str
    data_url: str
    tickers_url: str
    extension: str
    file_dir: str

class Config:

    def __init__(self):
        
        data = {}
        with open(
            join(dirname(abspath(__file__)), 'env.yaml'), encoding = 'utf-8'
        ) as file:
            data = load(file, Loader=SafeLoader)
        self.vars = Variables(
            project_name = data.get('project_name'),
            project_icon = data.get('project_icon'),
            data_dir = data.get('data_dir'),
            data_url = data.get('data_url'),
            tickers_url = data.get('tickers_url'),
            extension = data.get('extension'),
            file_dir = data.get('file_dir'),    
            )
        self.columns = ["Papel","Cotação","EV/EBIT","ROIC","Liq.2meses"],
        self.__user_agent = [
                'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
                ]  