document.addEventListener("DOMContentLoaded", async () => {
    const chartMap = echarts.init(document.getElementById('chart-map'), 'dark');
    const chartEscola = echarts.init(document.getElementById('chart-escola'), 'dark');
    const chartGenero = echarts.init(document.getElementById('chart-genero'), 'dark');
    const chartRenda = echarts.init(document.getElementById('chart-renda'), 'dark');
    const chartRaca = echarts.init(document.getElementById('chart-raca'), 'dark');
    const chartIdade = echarts.init(document.getElementById('chart-idade'), 'dark');

    window.addEventListener('resize', () => {
        chartMap.resize(); chartEscola.resize(); chartGenero.resize();
        chartRenda.resize(); chartRaca.resize(); chartIdade.resize();
    });

    try {
        const geoResponse = await fetch('https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson');
        const brazilGeoJson = await geoResponse.json();
        echarts.registerMap('brazil', brazilGeoJson);

        // Ler do JSON final (v2 force cache clear)
        const dataResponse = await fetch('../data/enem_metrics_final.json?v=2');
        const appData = await dataResponse.json();

        // Calcular min/max para a escala do mapa dinamicamente
        let maxUf = '', minUf = '', maxTaxa = 0, minTaxa = 100;
        for (const [key, value] of Object.entries(appData)) {
            if (key !== 'BR') {
                if (value.kpis.taxa_abstencao > maxTaxa) { maxTaxa = value.kpis.taxa_abstencao; maxUf = key; }
                if (value.kpis.taxa_abstencao < minTaxa) { minTaxa = value.kpis.taxa_abstencao; minUf = key; }
            }
        }
        document.getElementById('kpi-maior').innerText = `${maxUf} (${maxTaxa}%)`;
        document.getElementById('kpi-menor').innerText = `${minUf} (${minTaxa}%)`;

        const ufMapping = {
            "Acre": "AC", "Alagoas": "AL", "Amapá": "AP", "Amazonas": "AM", "Bahia": "BA",
            "Ceará": "CE", "Distrito Federal": "DF", "Espírito Santo": "ES", "Goiás": "GO",
            "Maranhão": "MA", "Mato Grosso": "MT", "Mato Grosso do Sul": "MS", "Minas Gerais": "MG",
            "Pará": "PA", "Paraíba": "PB", "Paraná": "PR", "Pernambuco": "PE", "Piauí": "PI",
            "Rio de Janeiro": "RJ", "Rio Grande do Norte": "RN", "Rio Grande do Sul": "RS",
            "Rondônia": "RO", "Roraima": "RR", "Santa Catarina": "SC", "São Paulo": "SP",
            "Sergipe": "SE", "Tocantins": "TO"
        };

        const mapData = brazilGeoJson.features.map(f => {
            const stateName = f.properties.name;
            const uf = ufMapping[stateName];
            return {
                name: stateName,
                value: appData[uf] ? appData[uf].kpis.taxa_abstencao : 0,
                uf: uf
            };
        });

        const colorPrimaria = '#FFD100'; // Amarelo
        const colorSecundaria = '#60A5FA'; // Azul claro
        const colorBg = 'transparent';
        const colorText = '#93c5fd';

        const ufSelect = document.getElementById('uf-select');
        const btnReset = document.getElementById('btn-reset');
        const lblLocal = document.getElementById('lbl-local');
        const kpiInscritos = document.getElementById('kpi-inscritos');
        const kpiAusentes = document.getElementById('kpi-ausentes');
        const kpiTaxa = document.getElementById('kpi-taxa');
        const varTaxa = document.getElementById('var-taxa');

        const updateView = (regionKey, regionName) => {
            const data = appData[regionKey];
            
            lblLocal.innerText = regionName;
            ufSelect.value = regionKey;
            
            kpiInscritos.innerText = data.kpis.inscritos.toLocaleString('pt-BR');
            kpiAusentes.innerText = data.kpis.ausentes.toLocaleString('pt-BR');
            kpiTaxa.innerText = `${data.kpis.taxa_abstencao}%`;
            
            // Variance Logic
            const diff = data.kpis.diff_taxa;
            if (diff === null || diff === undefined) {
                varTaxa.innerHTML = `- Dados de 2022 indisponíveis`;
                varTaxa.className = "variance var-neutral";
            } else if (diff > 0) {
                varTaxa.innerHTML = `▲ +${diff.toFixed(1)}% vs Ano Anterior`;
                varTaxa.className = "variance var-up";
            } else if (diff < 0) {
                varTaxa.innerHTML = `▼ ${diff.toFixed(1)}% vs Ano Anterior`;
                varTaxa.className = "variance var-down";
            } else {
                varTaxa.innerHTML = `- Estável`;
                varTaxa.className = "variance var-neutral";
            }

            btnReset.style.display = regionKey === 'BR' ? 'none' : 'block';

            // 1. Escola (Bar Horizontal) - Amarelo
            chartEscola.setOption({
                backgroundColor: colorBg,
                tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' }, formatter: '{b}<br/>Abstenção: {c}%' },
                grid: { left: '3%', right: '8%', bottom: '3%', top: '5%', containLabel: true },
                xAxis: { type: 'value', axisLabel: { formatter: '{value}%', color: colorText }, splitLine: { show: false } },
                yAxis: { type: 'category', data: data.escola.map(d => d.tipo), axisLabel: { color: '#e0f2fe' } },
                series: [{
                    type: 'bar',
                    data: data.escola.map(d => d.taxa),
                    itemStyle: { color: colorPrimaria, borderRadius: [0, 4, 4, 0] },
                    animationDurationUpdate: 800
                }]
            });

            // 2. Genero (Barras Horizontais — tipo correto para comparar taxas independentes)
            chartGenero.setOption({
                backgroundColor: colorBg,
                tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' }, formatter: '{b}<br/>Abstenção: {c}%' },
                grid: { left: '3%', right: '8%', bottom: '3%', top: '5%', containLabel: true },
                xAxis: { type: 'value', axisLabel: { formatter: '{value}%', color: colorText }, splitLine: { show: false } },
                yAxis: { type: 'category', data: data.genero.map(d => d.sexo), axisLabel: { color: '#e0f2fe' } },
                series: [{
                    type: 'bar',
                    data: data.genero.map(d => d.taxa),
                    itemStyle: { color: colorSecundaria, borderRadius: [0, 4, 4, 0] },
                    label: { show: true, position: 'right', formatter: '{c}%', color: '#fff', fontWeight: 'bold' },
                    animationDurationUpdate: 800
                }]
            });

            // 3. Renda (Bar Vertical)
            chartRenda.setOption({
                backgroundColor: colorBg,
                tooltip: { trigger: 'axis', formatter: '{b}<br/>Abstenção: {c}%' },
                grid: { left: '3%', right: '4%', bottom: '3%', top: '10%', containLabel: true },
                xAxis: { type: 'category', data: data.renda.map(d => d.faixa), axisLabel: { color: colorText, fontSize: 10, interval: 0 } },
                yAxis: { type: 'value', axisLabel: { formatter: '{value}%', color: colorText }, splitLine: { lineStyle: { color: 'rgba(255,255,255,0.05)' } } },
                series: [{
                    type: 'bar',
                    data: data.renda.map(d => d.taxa),
                    itemStyle: { color: colorSecundaria, borderRadius: [4, 4, 0, 0] },
                    animationDurationUpdate: 800
                }]
            });

            // 4. Raca (Bar Vertical)
            chartRaca.setOption({
                backgroundColor: colorBg,
                tooltip: { trigger: 'axis', formatter: '{b}<br/>Abstenção: {c}%' },
                grid: { left: '3%', right: '4%', bottom: '3%', top: '10%', containLabel: true },
                xAxis: { type: 'category', data: data.raca.map(d => d.cor), axisLabel: { color: colorText, fontSize: 10, interval: 0 } },
                yAxis: { type: 'value', axisLabel: { formatter: '{value}%', color: colorText }, splitLine: { lineStyle: { color: 'rgba(255,255,255,0.05)' } } },
                series: [{
                    type: 'bar',
                    data: data.raca.map(d => d.taxa),
                    itemStyle: { color: colorPrimaria, borderRadius: [4, 4, 0, 0] },
                    animationDurationUpdate: 800
                }]
            });

            // 5. Idade (Barra ao invés de linha perfeita para ser mais analitico)
            chartIdade.setOption({
                backgroundColor: colorBg,
                tooltip: { trigger: 'axis', formatter: '{b}<br/>Abstenção: {c}%' },
                grid: { left: '3%', right: '4%', bottom: '5%', top: '15%', containLabel: true },
                xAxis: { type: 'category', data: data.idade.map(d => d.faixa), axisLabel: { color: colorText, interval: 0 } },
                yAxis: { type: 'value', axisLabel: { formatter: '{value}%', color: colorText }, splitLine: { lineStyle: { color: 'rgba(255,255,255,0.05)' } } },
                series: [{
                    type: 'bar',
                    data: data.idade.map(d => d.taxa),
                    itemStyle: { color: colorSecundaria, borderRadius: [4, 4, 0, 0] },
                    animationDurationUpdate: 800
                }]
            });
        };

        // Render Map com Escala Dinamica Sequencial Sênior (Single Hue Luminosity)
        chartMap.setOption({
            backgroundColor: colorBg,
            tooltip: { trigger: 'item', formatter: '{b}<br/>Taxa de Abstenção: {c}%' },
            visualMap: {
                min: Math.floor(minTaxa), 
                max: Math.ceil(maxTaxa),
                text: ['Maior %', 'Menor %'],
                realtime: false,
                calculable: true,
                inRange: { color: ['#93c5fd', '#3b82f6', '#1e40af', '#001A33'] }, // Sequencial Azul Claro -> Azul Escuro
                textStyle: { color: colorText },
                bottom: 10, left: 10
            },
            series: [{
                name: 'Abstenção',
                type: 'map',
                map: 'brazil',
                roam: true,
                label: { show: true, color: 'rgba(255,255,255,0.7)', fontSize: 9 },
                emphasis: { label: { show: true, color: '#00254D', fontWeight: 'bold' }, itemStyle: { areaColor: '#fff' } },
                itemStyle: { borderColor: '#001A33', borderWidth: 1 },
                data: mapData
            }]
        });

        chartMap.on('click', function (params) {
            if(params.data && params.data.uf) {
                updateView(params.data.uf, params.data.name);
            }
        });

        ufSelect.addEventListener('change', (e) => {
            const uf = e.target.value;
            if (uf === 'BR') {
                updateView('BR', 'Brasil (Visão Nacional)');
            } else {
                const stateName = ufSelect.options[ufSelect.selectedIndex].text.replace(/ \(.+\)/, '');
                updateView(uf, stateName);
            }
        });

        btnReset.addEventListener('click', () => {
            updateView('BR', 'Brasil (Visão Nacional)');
        });

        updateView('BR', 'Brasil (Visão Nacional)');

    } catch(err) {
        console.error("Erro ao carregar dados", err);
    }
});
