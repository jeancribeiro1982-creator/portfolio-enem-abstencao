# 📊 Portfólio: O Mistério da Abstenção no ENEM (2023)

Dashboard analítico interativo que investiga os fatores socioeconômicos por trás da evasão de candidatos no Exame Nacional do Ensino Médio.

## 🔗 Acesse o Dashboard Online

👉 **[Clique aqui para acessar o painel interativo](https://jeancribeiro1982-creator.github.io/portfolio-enem-abstencao/dashboard/)**

## 🧠 Visão Geral do Projeto

Este projeto é uma análise de dados End-to-End que cobre todo o pipeline:

1. **ETL (Extract, Transform, Load):** Extração e tratamento dos microdados do INEP via Python/Pandas (Jupyter Notebook).
2. **Análise Exploratória:** Investigação de 7 dimensões socioeconômicas que influenciam a abstenção.
3. **Dashboard Interativo:** Painel web georreferenciado com mapa coroplético do Brasil e 6 gráficos dinâmicos.

## 📈 Dimensões Analisadas

| Dimensão | Insight Principal |
|---|---|
| **Renda Familiar** | Famílias sem renda têm taxa de abstenção 3x maior que famílias acima de 5 SM |
| **Cor/Raça** | Candidatos Indígenas e Pretos apresentam as maiores taxas |
| **Tipo de Escola** | Escola Pública tem abstenção ~3x maior que Privada |
| **Gênero** | Homens faltam levemente mais que mulheres |
| **Faixa Etária** | Abstenção cresce progressivamente com a idade |
| **Geografia (UF)** | Estados do Norte e Nordeste lideram a evasão |

## 🛠️ Stack Tecnológica

| Camada | Tecnologia |
|---|---|
| ETL & Big Data | Python, Pandas (`chunksize` streaming) |
| Visualização | ECharts (Apache), HTML5, CSS3, JavaScript |
| Design | Glassmorphism, Paleta Oficial ENEM (WCAG AA) |
| Deploy | GitHub Pages |

## 📂 Estrutura do Projeto

```
portfolio-enem-abstencao/
├── src/
│   └── process_real_enem.py    # Script ETL Pandas (processa 3.9M de linhas em chunks)
├── notebooks/
│   └── etl_enem.ipynb          # Jupyter Notebook de Análise Exploratória (EDA)
├── data/
│   └── enem_metrics_final.json # Dados processados (saída do ETL para o JS)
├── dashboard/
│   ├── index.html              # Página principal do painel
│   ├── style.css               # Estilos (Glassmorphism + Paleta ENEM)
│   ├── app.js                  # Lógica dos gráficos e interatividade
│   └── logo.svg                # Logotipo vetorial local
└── README.md
```

## ✨ Funcionalidades do Dashboard

- **Mapa Coroplético Interativo:** Clique em qualquer estado do Brasil para filtrar todos os gráficos simultaneamente.
- **Filtro por Dropdown:** Selecione um estado pela caixa de seleção no topo.
- **Extremos Automáticos:** O painel identifica automaticamente o estado com maior e menor abstenção.
- **Tooltips Detalhados:** Passe o mouse sobre qualquer barra ou região para ver o valor exato.

## 📋 Fonte dos Dados

- **Microdados Oficiais:** INEP — Microdados do ENEM 2023 (1.7 GB, ~3.9 milhões de registros processados autenticamente via script).

## 👤 Autor

**Jean Ribeiro** — Analista de Dados

---

*Projeto desenvolvido como portfólio de Data Science e Análise de Dados.*
