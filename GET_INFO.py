import os
import json
import sqlite3
import pandas as pd

db_file = r'2026-01.db'

files = os.listdir('CSV_FILES')

conn = sqlite3.connect(db_file)
cursor = conn.cursor()

municipios = []
natureza_juridica = []
cnaes = []
motivos =  []
qualificacao = []

def extract_municipios(conn):
    data = {}
    municipios = json.loads(pd.read_sql_query("SELECT DISTINCT MUNICÍPIO, UF FROM DADOS_ESTABELECIMENTOS ORDER BY UF, MUNICÍPIO",conn).to_json(orient='records',force_ascii=False))
    for m in municipios:
        data[m['UF']] = []
    for m in municipios:
        data[m['UF']].append(m['MUNICÍPIO'])
    with open('municipios.json','w',encoding='utf-8') as f:
        json.dump(data,f)
    return data
    
def extract_cnaes(file):
    with open(file,'r',encoding='latin1') as f:
        dados = [x.replace('\n','').replace('"','').split(';')[1] for x in f.readlines()]
    with open('cnaes.txt','w',encoding='utf-8') as f:
        f.write(str(dados))
    return dados

def extract_motivos(file):
    with open(file,'r',encoding='latin1') as f:
        dados = [x.replace('\n','').replace('"','').split(';')[1] for x in f.readlines()]
    with open('motivos.txt','w',encoding='utf-8') as f:
        f.write(str(dados))
    return dados

def extract_qualificacao(file):
    with open(file,'r',encoding='latin1') as f:
        dados = [x.replace('\n','').replace('"','').split(';')[1] for x in f.readlines()]
    with open('qualificacao.txt','w',encoding='utf-8') as f:
        f.write(str(dados))
    return dados

def extract_natureza_juridica(file):
    with open(file,'r',encoding='latin1') as f:
        dados = [x.replace('\n','').replace('"','').split(';')[1] for x in f.readlines()]
    with open('natureza_juridica.txt','w',encoding='utf-8') as f:
        f.write(str(dados))
    return dados


municipios = extract_municipios(conn)

for file in files:
    if 'CNAE' in file:
        cnaes = extract_cnaes(os.path.join('CSV_FILES',file))
    if 'MOTI' in file:
        motivos = extract_motivos(os.path.join('CSV_FILES',file))
    if 'QUAL' in file:
        qualificacao = extract_qualificacao(os.path.join('CSV_FILES',file))
    if 'NATJU' in file:
        natureza_juridica = extract_natureza_juridica(os.path.join('CSV_FILES',file))