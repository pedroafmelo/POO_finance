from dataclasses import dataclass
from yaml import load
from yaml.loader import SafeLoader
from os.path import join, dirname, abspath

@dataclass
class Variables:
    """Store config class"""
    
    project_name: str
    project_icon: str
    data_dir: str
    data_url: str
    stock_tickers_url: str
    crypto_tickers_url: str
    cdbs_tickers_url: str
    filename: str
    logo: str
    calc_gif: str
    extension: str

class Config:
    """Basic Config class"""

    def __init__(self):
        """Initialize instance"""
        
        self.project_dir = abspath(dirname(dirname(__file__)))
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
            stock_tickers_url = data.get('stock_tickers_url'),
            crypto_tickers_url = data.get('crypto_tickers_url'),
            cdbs_tickers_url = data.get('cdbs_tickers_url'),
            filename = data.get('file_name'),
            logo = data.get('logo'),
            calc_gif = data.get('calc_gif'),
            extension = data.get('extension'),
            )
        self.columns = ["Papel","Cotação", "P/L", "P/VP", "Div.Yield", 
                        "EV/EBIT", "ROIC", "Mrg. Líq.", "Liq.2meses"]
        
        self._user_agent = [
                'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
                ]
        self.bova11 = ['RRRP3', 'ALOS3', 'ALPA4', 'ABEV3', 'ARZZ3', 'ASAI3', 'AZUL4', 'B3SA3',
       'BBSE3', 'BBDC3', 'BBDC4', 'BRAP4', 'BBAS3', 'BRKM5', 'BRFS3', 'BPAC11',
       'CRFB3', 'CCRO3', 'CMIG4', 'CIEL3', 'COGN3', 'CPLE6', 'CSAN3', 'CPFE3',
       'CMIN3', 'CVCB3', 'CYRE3', 'DXCO3', 'ELET3', 'ELET6', 'EMBR3', 'ENGI11',
       'ENEV3', 'EGIE3', 'EQTL3', 'EZTC3', 'FLRY3', 'GGBR4', 'GOAU4', 'NTCO3',
       'SOMA3', 'HAPV3', 'HYPE3', 'IGTI11', 'IRBR3', 'ITSA4', 'ITUB4', 'JBSS3',
       'KLBN11', 'RENT3', 'LREN3', 'LWSA3', 'MGLU3', 'MRFG3', 'BEEF3', 'MRVE3',
       'MULT3', 'PCAR3', 'PETR3', 'PETR4', 'RECV3', 'PRIO3', 'PETZ3', 'RADL3',
       'RAIZ4', 'RDOR3', 'RAIL3', 'SBSP3', 'SANB11', 'SMTO3', 'CSNA3', 'SLCE3',
       'SUZB3', 'TAEE11', 'VIVT3', 'TIMS3', 'TOTS3', 'TRPL4', 'UGPA3', 'USIM5',
       'VALE3', 'VAMO3', 'VBBR3', 'WEGE3', 'YDUQ3']