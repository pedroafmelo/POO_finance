<p align="center">
  <a>
    <img src="img/logo.jpg" height="180" width="195" alt="CoinPurse" />
  </a>
</p>

<style>
    body {
        background-color: #151827; /* Substitua pela cor desejada */
    }
</style>

<p align="center">
  <a href="https://coinpurse.streamlit.app/">
    <img src="https://img.shields.io/static/v1?label=streamlit&message=app&color=7159c1&style=for-the-badge&logo=streamlit" alt="Badge">
  </a>
</p>

<br>
<p align="center">Practical and portable finance analyst 🪙</p>
<br>
<br>

Tabela de conteúdos
=================
<!--ts-->
   * [Sobre](#Sobre)
   * [Tabela de Conteudo](#tabela-de-conteudo)
   * [Instalação](#instalacao)
   * [Como usar](#como-usar)
      * [Pre Requisitos](#pre-requisitos)
      * [Local files](#local-files)
      * [Remote files](#remote-files)
      * [Multiple files](#multiple-files)
      * [Combo](#combo)
   * [Tests](#testes)
   * [Tecnologias](#tecnologias)
<!--te-->

<h4 align="center"> 
	🚧  CoinPurse 🪙 Em construção...  🚧
</h4>

### Features

- [x] Calculadora de Juros Compostos
- [x] Recomendação de Investimentos
- [x] Histórico de Ações

### Interface Inicial

<p align="center">
  <a>
    <img src="img/interface.png"  alt="Interface" />
  </a>
</p>
<br>

### Calculadora de Juros Compostos
<p align="center">
  <a>
     <video controls src="img/"></video>
  </a>
</p>
<br>

### Recomendador de Investimentos
<p align="center">
  <a>
    <img src="img/tabela.png"  alt="Interface" />
  </a>
</p>
<br>

### Histórico de Ações
<p align="center">
  <a>
    <video controls src="img/"></video>
  </a>
</p>
<br>

### Como rodar localmente

Caso queira rodar localmente, você irá inicialmente precisar dessas ferramentas instaladas:
[Git](https://git-scm.com), [Python](https://www.python.org/downloads/). 
Além disto é bom ter um editor para trabalhar com o código como [VSCode](https://code.visualstudio.com/)

### 🎲 Rodando Localmente (servidor)

Primeiramente clone o projeto
```bash
# Clone este repositório
$ git clone <https://github.com/pedroafmelo/POO_finance.git>

# Acesse a pasta do projeto no terminal/cmd
$ cd <caminho/até/POO_finance>
````

Para instalar as dependências, recomendo que primeiro crie um ambiente virtual.
````bash
# Crie o ambiente
python -m venv myenv

# Ative o ambiente
myenv\Scripts\activate
````

Agora pode instalar as dependências
````bash
# Instale as dependências
$ pip install -r requirements.txt
````

Por fim, pode rodar a aplicação
````bash
# Execute a aplicação em modo de desenvolvimento
$ python -m streamlit run app.py

# O servidor inciará na porta:8501 - acesse <http://localhost:8501>
````
<br>

### 🛠 Tecnologias e Ferramentas

As seguintes ferramentas foram usadas na construção do projeto:

- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [Beatiful Soup](https://beautiful-soup-4.readthedocs.io/en/latest/)
- [Yahoo Finances API](https://pypi.org/project/yfinance/)
- [Pandas](https://pandas.pydata.org/)
<br>
<br>


### Autores

<table>
  <tr>
    <td align="center">
  <a href="https://github.com/pedroafmelo">
    <img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/u/141172256?s=48&v=4" width="100px;" alt=""/>
    <br />
    <sub><b>Pedro Augusto</b></sub>
  </a>
  <br/>
  <b>
  <a href="https://www.linkedin.com/" target="_blank" >
    <img src="https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" style="padding-top: 10px;">
  </a>
    <td align="center">
  <a href="https://github.com/ricktherunner">
    <img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/u/139015105?v=4" width="100px;" alt=""/>
    <br />
    <sub><b>Pedro Henrique</b></sub>
  </a>
  <br />
  <a href="https://www.linkedin.com/" target="_blank">
    <img src="https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" style="padding-top: 10px;">
  </a>
</td>
    <td align="center">
  <a href="https://github.com/lucasrabay">
    <img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/u/140542061?v=4" width="100px;" alt=""/>
    <br />
    <sub><b>Lucas Rabay</b></sub>
  </a>
  <br />
  <a href="https://www.linkedin.com/" target="_blank">
    <img src="https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" style="padding-top: 10px;">
  </a>
</td>

</table>

