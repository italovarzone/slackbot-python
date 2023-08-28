from json import load
import pathlib

with open(f"{pathlib.Path().absolute()}/config/security.json", "r", encoding='utf-8', errors='ignore') as jsonini:
    iniAuth = load(jsonini)

with open(f"{pathlib.Path().absolute()}/config/queue.json", "r", encoding='utf-8', errors='ignore') as jsonini:
    iniQueue = load(jsonini)

tokenBot = iniAuth['tokenBot']
SigningSecret = iniAuth['SigningSecret']
queue = iniQueue['technical']
