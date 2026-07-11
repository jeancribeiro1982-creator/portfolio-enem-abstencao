# 📊 Portfólio: O Mistério da Abstenção no ENEM (2023)

Dashboard analítico interativo que investiga os fatores socioeconômicos por trás da evasão de candidatos no Exame Nacional do Ensino Médio.

> Este projeto é a primeira parte de uma análise de dados em dois atos. Enquanto aqui nós respondemos ***o quê*** e ***onde***, o projeto irmão de [Machine Learning](https://github.com/jeancribeiro1982-creator/portfolio-enem-ml) vai fundo no ***por quê*** e no ***quanto custa*** financeiramente.

## 🔗 Acesse o Dashboard Online

👉 **[Clique aqui para acessar o painel interativo](https://jeancribeiro1982-creator.github.io/portfolio-enem-abstencao/dashboard/)**

## 💡 Motivação

Os números do ENEM chegam todo ano em forma de notícia: "taxa de abstenção bate recorde". Mas essa manchete raramente mostra a desigualdade que existe embaixo desse número único.

A pergunta que motivou esse projeto foi simples: **a taxa de abstenção é uniforme entre os diferentes grupos sociais, ou ela diz mais sobre as condições de vida de quem falta do que sobre "falta de interesse"?**

A resposta, como os dados confirmam, é a segunda opção — e ela é devastadora.

## 🧠 Visão Geral do Projeto

Este projeto é uma análise de dados End-to-End que cobre todo o pipeline:

1. **ETL (Extract, Transform, Load):** Extração e tratamento dos microdados do INEP via Python/Pandas, processando 3,9 milhões de linhas em blocos (`chunksize`) para não estourar a memória RAM.
2. **Análise Exploratória:** Investigação de 7 dimensões socioeconômicas que influenciam a abstenção.
3. **Dashboard Interativo:** Painel web georreferenciado com mapa coroplético do Brasil e 6 gráficos dinâmicos, construído com Apache ECharts.

## 📈 Dimensões Analisadas

| Dimensão | Insight Principal |
|:---|:---|
| **Renda Familiar** | Famílias sem renda têm taxa de abstenção 3x maior que famílias acima de 5 SM |
| **Cor/Raça** | Candidatos Indígenas e Pretos apresentam as maiores taxas |
| **Tipo de Escola** | Escola Pública tem abstenção ~3x maior que Privada |
| **Gênero** | Homens faltam levemente mais que mulheres |
| **Faixa Etária** | Abstenção cresce progressivamente com a idade |
| **Geografia (UF)** | Estados do Norte e Nordeste lideram a evasão |

## 🛠️ Stack Tecnológica

| Camada | Tecnologia |
|:---|:---|
| ETL & Big Data | Python, Pandas (`chunksize` streaming) |
| Visualização | ECharts (Apache), HTML5, CSS3, JavaScript |
| Design | Glassmorphism, Paleta Oficial ENEM (WCAG AA) |
| Deploy | GitHub Pages |

## ✨ Funcionalidades do Dashboard

- **Mapa Coroplético Interativo:** Clique em qualquer estado do Brasil para filtrar todos os gráficos simultaneamente.
- **Filtro por Dropdown:** Selecione um estado pela caixa de seleção no topo.
- **Extremos Automáticos:** O painel identifica automaticamente o estado com maior e menor abstenção.
- **Tooltips Detalhados:** Passe o mouse sobre qualquer barra ou região para ver o valor exato.
- **Variação Interanual:** KPIs mostram a diferença absoluta de inscritos e ausentes entre 2022 e 2023.

## 📂 Estrutura do Projeto

```
portfolio-enem-abstencao/
├── src/
│   ├── process_real_enem.py    # Script ETL Pandas (processa 3.9M de linhas em chunks)
│   └── extract_2022.py         # Script de extração e cálculo de variação 2022 vs 2023
├── notebooks/
│   └── etl_enem.ipynb          # Jupyter Notebook de Análise Exploratória (EDA)
├── data/
│   └── enem_metrics_final.json # Dados processados (saída do ETL para o dashboard)
├── dashboard/
│   ├── index.html              # Página principal do painel
│   ├── style.css               # Estilos (Glassmorphism + Paleta ENEM)
│   └── app.js                  # Lógica dos gráficos e interatividade (ECharts)
└── README.md
```

## ▶️ Como Executar Localmente

1. Clone este repositório.
2. Baixe os microdados do ENEM 2023 e 2022 do INEP (links na seção abaixo) e coloque-os em `data/`.
3. Instale as dependências Python:
```bash
pip install pandas numpy
```
4. Rode os scripts ETL para gerar o JSON de saída:
```bash
python src/extract_2022.py
python src/process_real_enem.py
```
5. Abra o dashboard no navegador com um servidor local:
```bash
cd dashboard
python -m http.server 8080
# Acesse http://localhost:8080
```

## 📋 Fonte dos Dados

- **Microdados Oficiais:** INEP — Microdados do ENEM 2022 e 2023. Disponíveis em [inep.gov.br](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem).

## 👤 Autor

**Jean Ribeiro** — Analista de Dados

---

*Parte de um portfólio de projetos de Ciência de Dados aplicada a dados públicos brasileiros.*
