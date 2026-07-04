import pandas as pd
import zipfile
import json
import os

print("Extraindo microdados de 2022 direto do ZIP...")
taxas_2022 = {}
zip_path = 'data/microdados_enem_2022.zip'

if not os.path.exists(zip_path):
    print("Erro: ZIP de 2022 não encontrado.")
    exit(1)

with zipfile.ZipFile(zip_path, 'r') as z:
    csv_name = [n for n in z.namelist() if n.endswith('.csv') and 'MICRODADOS' in n.upper()][0]
    print(f"Lendo {csv_name} em blocos...")
    with z.open(csv_name) as f:
        # Lendo em chunks
        db_raw_2022 = {'BR': {'inscritos': 0, 'ausentes': 0}}
        cols = ['SG_UF_PROVA', 'TP_PRESENCA_CH'] # Usando CH (dia 1) como base de abstenção
        
        for chunk in pd.read_csv(f, sep=';', encoding='latin1', usecols=cols, chunksize=200000):
            chunk['ausente'] = (chunk['TP_PRESENCA_CH'] == 0).astype(int)
            
            # BR
            db_raw_2022['BR']['inscritos'] += len(chunk)
            db_raw_2022['BR']['ausentes'] += chunk['ausente'].sum()
            
            # UF
            grp = chunk.groupby('SG_UF_PROVA')['ausente'].agg(['count', 'sum']).reset_index()
            for _, row in grp.iterrows():
                uf = row['SG_UF_PROVA']
                if uf not in db_raw_2022:
                    db_raw_2022[uf] = {'inscritos': 0, 'ausentes': 0}
                db_raw_2022[uf]['inscritos'] += row['count']
                db_raw_2022[uf]['ausentes'] += row['sum']
                
        for uf, data in db_raw_2022.items():
            insc = int(data['inscritos'])
            aus = int(data['ausentes'])
            taxas_2022[uf] = {
                'inscritos': insc,
                'ausentes': aus,
                'taxa': round((aus / insc * 100), 1) if insc > 0 else None
            }

with open('data/taxas_2022.json', 'w') as f:
    json.dump(taxas_2022, f)
    
print("Taxas de 2022 reais extraídas com sucesso!")
print(taxas_2022)
