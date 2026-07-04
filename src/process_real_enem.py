import pandas as pd
import json
import os

print("Iniciando processamento real dos microdados do ENEM 2023...")

# Mapeamentos para as variáveis categóricas
MAP_SEXO = {'M': 'Masculino', 'F': 'Feminino'}
MAP_RACA = {
    0: 'Não Declarado',
    1: 'Branca',
    2: 'Preta',
    3: 'Parda',
    4: 'Amarela',
    5: 'Indígena',
    6: 'Não Declarado'
}
MAP_ESCOLA = {
    1: 'Não Declarado',
    2: 'Pública',
    3: 'Privada',
    4: 'Não Declarado'
}

def map_idade(tp):
    # Baseado no dicionário padrão do ENEM
    if pd.isna(tp): return 'Não Declarado'
    if tp <= 2: return '< 18 anos'
    elif tp <= 5: return '18-20'
    elif tp <= 10: return '21-25'
    elif tp <= 11: return '26-30'
    else: return '> 30 anos'

def map_renda(q):
    if pd.isna(q): return 'Sem Resposta'
    if q == 'A': return 'Sem Renda'
    elif q in ['B', 'C']: return 'Até 1 SM' # B=1 SM, C=1.5 SM (aprox)
    elif q in ['D', 'E', 'F', 'G']: return '1 a 3 SM'
    elif q in ['H', 'I', 'J', 'K']: return '3 a 5 SM'
    else: return '+5 SM'

# Vamos acumular as contagens para depois calcular as taxas
# Estrutura: db[UF][DIMENSAO][CHAVE] = {'inscritos': 0, 'ausentes': 0}
# E um "BR" para Brasil
db_raw = {'BR': {'kpis': {'inscritos': 0, 'ausentes': 0}, 'renda': {}, 'raca': {}, 'escola': {}, 'idade': {}, 'genero': {}}}

chunk_size = 200000
file_path = "data/raw_inep/DADOS/MICRODADOS_ENEM_2023.csv"
cols = ['SG_UF_PROVA', 'TP_PRESENCA_CH', 'TP_SEXO', 'TP_COR_RACA', 'TP_ESCOLA', 'TP_FAIXA_ETARIA', 'Q006']

for chunk in pd.read_csv(file_path, sep=';', encoding='latin1', usecols=cols, chunksize=chunk_size):
    # Faltou se presença no dia 1 (CH/LC) for 0
    chunk['ausente'] = (chunk['TP_PRESENCA_CH'] == 0).astype(int)
    
    # Processar cada linha ou agrupar
    # Para ser eficiente, agrupamos por UF + Dimensões
    
    # Sexo
    grp_sexo = chunk.groupby(['SG_UF_PROVA', 'TP_SEXO'])['ausente'].agg(['count', 'sum']).reset_index()
    for _, row in grp_sexo.iterrows():
        uf = row['SG_UF_PROVA']
        sexo = MAP_SEXO.get(row['TP_SEXO'], 'Outro')
        
        if uf not in db_raw:
            db_raw[uf] = {'kpis': {'inscritos': 0, 'ausentes': 0}, 'renda': {}, 'raca': {}, 'escola': {}, 'idade': {}, 'genero': {}}
            
        # BR
        db_raw['BR']['kpis']['inscritos'] += row['count']
        db_raw['BR']['kpis']['ausentes'] += row['sum']
        db_raw['BR']['genero'].setdefault(sexo, {'inscritos': 0, 'ausentes': 0})
        db_raw['BR']['genero'][sexo]['inscritos'] += row['count']
        db_raw['BR']['genero'][sexo]['ausentes'] += row['sum']
        
        # UF
        db_raw[uf]['kpis']['inscritos'] += row['count']
        db_raw[uf]['kpis']['ausentes'] += row['sum']
        db_raw[uf]['genero'].setdefault(sexo, {'inscritos': 0, 'ausentes': 0})
        db_raw[uf]['genero'][sexo]['inscritos'] += row['count']
        db_raw[uf]['genero'][sexo]['ausentes'] += row['sum']

    # Raca
    grp = chunk.groupby(['SG_UF_PROVA', 'TP_COR_RACA'])['ausente'].agg(['count', 'sum']).reset_index()
    for _, row in grp.iterrows():
        uf = row['SG_UF_PROVA']
        val = MAP_RACA.get(row['TP_COR_RACA'], 'Não Declarado')
        db_raw['BR']['raca'].setdefault(val, {'inscritos': 0, 'ausentes': 0})
        db_raw['BR']['raca'][val]['inscritos'] += row['count']
        db_raw['BR']['raca'][val]['ausentes'] += row['sum']
        db_raw[uf]['raca'].setdefault(val, {'inscritos': 0, 'ausentes': 0})
        db_raw[uf]['raca'][val]['inscritos'] += row['count']
        db_raw[uf]['raca'][val]['ausentes'] += row['sum']

    # Escola
    grp = chunk.groupby(['SG_UF_PROVA', 'TP_ESCOLA'])['ausente'].agg(['count', 'sum']).reset_index()
    for _, row in grp.iterrows():
        uf = row['SG_UF_PROVA']
        val = MAP_ESCOLA.get(row['TP_ESCOLA'], 'Não Declarado')
        db_raw['BR']['escola'].setdefault(val, {'inscritos': 0, 'ausentes': 0})
        db_raw['BR']['escola'][val]['inscritos'] += row['count']
        db_raw['BR']['escola'][val]['ausentes'] += row['sum']
        db_raw[uf]['escola'].setdefault(val, {'inscritos': 0, 'ausentes': 0})
        db_raw[uf]['escola'][val]['inscritos'] += row['count']
        db_raw[uf]['escola'][val]['ausentes'] += row['sum']

    # Idade
    chunk['idade_cat'] = chunk['TP_FAIXA_ETARIA'].apply(map_idade)
    grp = chunk.groupby(['SG_UF_PROVA', 'idade_cat'])['ausente'].agg(['count', 'sum']).reset_index()
    for _, row in grp.iterrows():
        uf = row['SG_UF_PROVA']
        val = row['idade_cat']
        db_raw['BR']['idade'].setdefault(val, {'inscritos': 0, 'ausentes': 0})
        db_raw['BR']['idade'][val]['inscritos'] += row['count']
        db_raw['BR']['idade'][val]['ausentes'] += row['sum']
        db_raw[uf]['idade'].setdefault(val, {'inscritos': 0, 'ausentes': 0})
        db_raw[uf]['idade'][val]['inscritos'] += row['count']
        db_raw[uf]['idade'][val]['ausentes'] += row['sum']

    # Renda
    chunk['renda_cat'] = chunk['Q006'].apply(map_renda)
    grp = chunk.groupby(['SG_UF_PROVA', 'renda_cat'])['ausente'].agg(['count', 'sum']).reset_index()
    for _, row in grp.iterrows():
        uf = row['SG_UF_PROVA']
        val = row['renda_cat']
        db_raw['BR']['renda'].setdefault(val, {'inscritos': 0, 'ausentes': 0})
        db_raw['BR']['renda'][val]['inscritos'] += row['count']
        db_raw['BR']['renda'][val]['ausentes'] += row['sum']
        db_raw[uf]['renda'].setdefault(val, {'inscritos': 0, 'ausentes': 0})
        db_raw[uf]['renda'][val]['inscritos'] += row['count']
        db_raw[uf]['renda'][val]['ausentes'] += row['sum']

print("Calculando taxas finais...")
# Converter db_raw para db_final (JSON structure required by dashboard)
db_final = {}
for uf, data in db_raw.items():
    insc = data['kpis']['inscritos']
    aus = data['kpis']['ausentes']
    taxa = round((aus / insc * 100), 1) if insc > 0 else 0
    # Usando dados reais de 2022 extraídos
    taxa_anterior = None
    if os.path.exists('data/taxas_2022.json'):
        with open('data/taxas_2022.json', 'r') as f2:
            t_2022 = json.load(f2)
            taxa_anterior = t_2022.get(uf, None)

    diff_taxa = round(taxa - taxa_anterior, 1) if taxa_anterior is not None else None
    
    db_final[uf] = {
        "kpis": {
            "inscritos": int(insc),
            "ausentes": int(aus),
            "taxa_abstencao": taxa,
            "taxa_anterior": taxa_anterior,
            "diff_taxa": diff_taxa
        },
        "renda": [{"faixa": k, "taxa": round((v['ausentes']/v['inscritos']*100),1) if v['inscritos']>0 else 0} for k, v in data['renda'].items()],
        "raca": [{"cor": k, "taxa": round((v['ausentes']/v['inscritos']*100),1) if v['inscritos']>0 else 0} for k, v in data['raca'].items()],
        "escola": [{"tipo": k, "taxa": round((v['ausentes']/v['inscritos']*100),1) if v['inscritos']>0 else 0} for k, v in data['escola'].items()],
        "idade": [{"faixa": k, "taxa": round((v['ausentes']/v['inscritos']*100),1) if v['inscritos']>0 else 0} for k, v in data['idade'].items()],
        "genero": [{"sexo": k, "taxa": round((v['ausentes']/v['inscritos']*100),1) if v['inscritos']>0 else 0} for k, v in data['genero'].items()]
    }

with open("data/enem_metrics_final.json", "w", encoding="utf-8") as f:
    json.dump(db_final, f, ensure_ascii=False, indent=2)

print("Dados Finais reais gerados com sucesso!")
