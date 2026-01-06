# Dashboard – Obesidade (Power BI)

Este diretório contém o painel analítico do Tech Challenge – Fase 04 (Data Analytics – Pos Tech), com foco em **insights sobre níveis de obesidade** e fatores associados (hábitos e perfil).

O dashboard foi desenvolvido no **Power BI** e utiliza como base o dataset tratado no projeto. (obesity.csv==>Knime==POstgres==>PowerBI)

---

## Acesso ao Dashboard (Online)

O painel está publicado e pode ser acessado por este link:

https://app.powerbi.com/view?r=eyJrIjoiMzQ4NjU1MjAtY2YwNi00NGZhLWI3NjEtYjQ1NjYxMzE2ZjNkIiwidCI6IjhhZjNmN2Y1LTUzYTQtNDcxYS1hMWI1LWI2N2E5YzQ4YTI1NCJ9

---

## Estrutura do Dashboard

O dashboard está organizado em páginas, com filtros para segmentação do perfil dos entrevistados.

### Página 1 — Visão Geral (Panorama)

Objetivo: apresentar um resumo rápido da base e da distribuição dos perfis por estado nutricional.

Principais elementos:
- **Total de pessoas entrevistadas**
- **Percentual de pessoas obesas**
- **Percentual de pessoas com sobrepeso**
- **Percentual com peso normal**
- **Percentual abaixo do peso**

Gráficos:
- **Distribuição por Estado Nutricional** (quantidade por categoria)
- **Detalhamento da Obesidade por Grau** (Grau I, II, III)

Filtros disponíveis (lado direito):
- Faixa etária
- Sexo
- Atividade física (frequência)
- Monitoramento de calorias

---

### Página 2 — Proporção de consumo de alimentos calóricos por nível de obesidade

Objetivo: mostrar a proporção (em %) de pessoas que consomem alimentos calóricos, segmentado por nível de obesidade.

Gráfico principal:
- Barras empilhadas 100% comparando **“Sim” vs “Não”** para consumo de alimentos calóricos em cada nível.

Uso típico:
- Identificar se o consumo de alimentos calóricos está associado a níveis mais altos de obesidade.

---

### Página 3 — Distribuição da obesidade por faixa etária

Objetivo: comparar a distribuição do nível de obesidade em diferentes faixas etárias.

Gráfico principal:
- Gráfico de colunas por **faixa etária** com a **quantidade de pessoas** em cada classe de obesidade (inclui peso insuficiente, peso normal, sobrepeso e obesidade por grau).

Uso típico:
- Identificar faixas etárias com maior concentração de sobrepeso/obesidade.

---

## Arquivos deste diretório

- `Obesidade.pbix` (arquivo do Power BI Desktop)
- `README.md` (este documento)
