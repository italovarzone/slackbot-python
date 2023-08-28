# README #

Esse README descreve a aplicação, formas de utilização, instalação e desenvolvimento.

## Descrição do Repositório ##

Aplicação utilizada para gerenciar filas de técnicos no Slack.

v0.0.1

### Instalação e Configuração Inicial ###

- Configuração Inicial
  - Criar .env copiando os conteúdos de .env-example para .env
  - Copiar security.json e queue.json para a pasta config

- Instalação Docker
  - Necessário docker ... e docker compose ...
  - executar `bash docker compose up --build`

- Instalação local
  - venv - Python 3.10.2 (`bash python3.10 -m venv .venv`)
  - Acessar a venv `bash source .venv/bin/activate`
  - Instalar os requisitos necessários `bash pip install -r requirements.txt`
  - Para executar a aplicação rodar: `bash python app.py`
