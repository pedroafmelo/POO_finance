# -- coding: UTF-8 --
"""Import modules"""
from dataclasses import dataclass
from os import path

@dataclass
class Variables:
    """Variables dataclass"""

    project_name: str
    project_icon: str
    project_dir: str
    data_dir: str
    df_dir: str
    data_url: str
    encoding: str
    extension: str

class Config:
    """Iface Config"""

    def _init_(self) -> None:
        """Initialize instance"""
        variables = Variables(
            project_name = "Coin Purse",
            project_icon = "🪙",
            project_dir = path.abspath(path.dirname(__file__)),
            data_dir = path.join(self.vars.project_dir, "data"),
            extension= ".csv.gz",
            df_dir = path.join(self.vars.data_dir, f"b3_companies{self.vars.extension}"),
            data_url = "https://www.fundamentus.com.br/resultado.php"
        )

        self.vars = variables
        self.user_agent = [
            'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
        ]
        self.columns = ["Papel", "Cotação", "EV/EBIT", "ROIC", "Liq.2meses"]