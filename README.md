# 📊 Portfólio: O Mistério da Abstenção no ENEM (2023)

<!-- CI/CD Badges -->
![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg?style=flat-square)
![License MIT](https://img.shields.io/badge/license-MIT-green.svg?style=flat-square)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg?style=flat-square)
![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)

![Dashboard Preview](docs/dashboard.png)

Dashboard analítico interativo que investiga os fatores socioeconômicos por trás da evasão de candidatos no Exame Nacional do Ensino Médio.

> Este projeto é a primeira parte de uma análise de dados em dois atos. Enquanto aqui nós respondemos ***o quê*** e ***onde***, o projeto irmão de [Machine Learning](https://github.com/jeanribeiro-dev/portfolio-enem-ml) vai fundo no ***por quê*** e no ***quanto custa*** financeiramente.

## 🎯 Key Insights (O que descobrimos?)
A análise de 3,9 milhões de registros revelou dados alarmantes que vão além da "falta de interesse":
- **Renda é o maior gargalo:** Candidatos de famílias sem nenhuma renda apresentam uma taxa de abstenção **3x maior** em comparação aos candidatos de famílias com renda superior a 5 Salários Mínimos.
- **Geografia da Evasão:** Norte e Nordeste lideram as taxas de evasão no país, sugerindo dificuldades logísticas e estruturais regionais.
- **Escola Pública x Privada:** Alunos oriundos de escolas públicas abandonam o exame em uma proporção quase 3 vezes superior aos de escolas privadas.

## 🔗 Acesse o Dashboard Online

👉 **[Clique aqui para acessar o painel interativo](https://jeanribeiro-dev.github.io/portfolio-enem-abstencao/dashboard/)**

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

## 🏗️ Arquitetura e Estrutura do Projeto

O fluxo de dados segue o pipeline: **Extract & Load (INEP) -> Transform (Pandas Out-of-Core) -> Dashboard (ECharts)**.

```mermaid
graph LR
    A[Microdados INEP (1.7GB)] -->|chunksize=200k| B(Pandas ETL)
    B --> C[Tratamento NAs & Encoding]
    C --> D[(enem_metrics_final.json)]
    D --> E[ECharts Dashboard]
    E --> F[GitHub Pages]
```

```text
portfolio-enem-abstencao/
├── data/
│   ├── raw_inep/               # Dados brutos (Git Ignored)
│   └── enem_metrics_final.json # Dados processados agregados
├── docs/
│   └── dashboard.png           # Assets para documentação
├── notebooks/
│   └── etl_enem.ipynb          # Exploração (EDA) e prototipação
├── src/
│   ├── process_real_enem.py    # Pipeline ETL em chunksize
│   └── extract_2022.py         # Scripts de comparação anual
├── dashboard/
│   ├── index.html              # Interface do Usuário
│   ├── style.css               # Design UI/UX
│   └── app.js                  # Engine do ECharts
├── requirements.txt            # Dependências rigorosas
└── README.md
```

## ▶️ Reprodutibilidade e Configuração Local (Setup)

Utilizamos um ambiente estrito para garantir a reprodutibilidade dos dados.

1. Clone este repositório.
2. Baixe os microdados do ENEM 2023 e 2022 do INEP (links na seção de Proveniência de Dados) e extraia na pasta `data/raw_inep/DADOS/`.
3. Instale as dependências rigorosas usando o `requirements.txt`:
```bash
pip install -r requirements.txt
```
4. Execute o pipeline de ETL para gerar os agregados finais:
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

## 📋 Proveniência e Integridade de Dados

- **Fonte Oficial:** Os dados brutos vêm do INEP (Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira). [Link de acesso público](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem).
- **Compliance e LGPD:** Todos os microdados são 100% anonimizados de origem. Nenhum PII (Personally Identifiable Information) é exposto ou trafegado neste sistema.
- **Volume:** A base de 2023 conta com mais de 3.9 milhões de registros, processados em memória restrita utilizando `chunksize`.

## 👤 Autor

**Jean Ribeiro** — Analista de Dados

---

*Parte de um portfólio de projetos de Ciência de Dados aplicada a dados públicos brasileiros.*
