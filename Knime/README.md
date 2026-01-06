# KNIME — Workflow de Tratamento da Base (Obesidade)

Este diretório contém o workflow do **KNIME** usado para tratar a base `Obesity.csv` e gravar o resultado no **PostgreSQL** (tabela `public.obesidade`), que foi consumida no Power BI e nos notebooks.

Arquivos:
- `Obesidade.knwf` (workflow)
- `Obesidade.zip` (workflow exportado/arquivado)

---

## Objetivo do workflow
1) Ler o CSV original
2) Selecionar colunas de interesse
3) Padronizar tipos/valores (numéricos e categóricos)
4) Padronizar rótulos em PT-BR (Rule Engine)
5) Gravar no PostgreSQL (`public.obesidade`)

---

## Entrada
- CSV original (no workflow estava apontando para um caminho local do Windows).
- Recomendação no repositório: usar `data/raw/Obesity.csv`.

---

## Saída
- PostgreSQL:
  - Schema: `public`
  - Tabela: `obesidade`
- Essa base foi usada para:
  - Dashboard Power BI
  - Pipeline de ML (notebooks)

---

## Pipeline (resumo por etapas)

### 1) Leitura e seleção de colunas
- **CSV Reader (#1)**: leitura do dataset.
- **Column Filter (#4)**: mantém estas colunas (17):
  - sexo
  - idade
  - altura
  - peso
  - historico_familiar
  - ingere_alim_calorico
  - ingere_vegetais
  - qtd_refeicao_principal
  - come_entre_refeicao
  - fumante
  - consumo_agua_litro
  - monitora_calorias
  - freq_atividade_fisica
  - tempo_uso_eletronico
  - frequencia_consumo_alcool
  - meio_de_transporte
  - nivel_obsesidade (nome conforme estava na base do KNIME)


---

### 2) Tratamento de valores ausentes
- **Missing Value (#5)**: configurado como **Do Nothing** para String e Double (ou seja, não faz imputação automática).

---

### 3) Padronização numérica (Math Formula)
As fórmulas abaixo foram aplicadas para “arredondar/normalizar” valores:

- **Ajuste Idade (Math Formula #20)**
  - `idade = floor($idade$)`

- **Ajuste Atividade Física (Math Formula #21)**
  - `freq_atividade_fisica = round($freq_atividade_fisica$)`

- **Consumo vegetais (Math Formula #23)**
  - `ingere_vegetais = round($ingere_vegetais$)`

- **Número de Refeições Principais (Math Formula #24)**
  - `qtd_refeicao_principal = round($qtd_refeicao_principal$)`

- **Consumo de água (Math Formula #25)**  *(no fluxo aparece com o mesmo título “Número de Refeições Principais”, mas atua em água)*
  - `consumo_agua_litro = round($consumo_agua_litro$)`

- **Uso de eletrônicos (Math Formula #26)**
  - `tempo_uso_eletronico = round($tempo_uso_eletronico$)`

---

### 4) Padronização de categorias (Rule Engine)
Os nós abaixo traduzem/padronizam os rótulos:

- **Sexo (Rule Engine #10)** — substitui a coluna `sexo`
  - `$sexo$ = "Female" => "Feminino"`
  - `$sexo$ = "Male"   => "Masculino"`
  - `TRUE => $sexo$`

- **Histórico Familiar (Rule Engine #11)** — `historico_familiar`
  - `$historico_familiar$ = "yes" => "Sim"`
  - `$historico_familiar$ = "no"  => "Não"`
  - `TRUE => $historico_familiar$`

- **Ingere alimentos calóricos (Rule Engine #12)** — `ingere_alim_calorico`
  - `$ingere_alim_calorico$ = "yes" => "Sim"`
  - `$ingere_alim_calorico$ = "no"  => "Não"`
  - `TRUE => $ingere_alim_calorico$`

- **Come entre refeições (Rule Engine #13)** — `come_entre_refeicao`
  - `$come_entre_refeicao$ = "no"          => "Não"`
  - `$come_entre_refeicao$ = "Frequently"  => "Frequentemente"`
  - `$come_entre_refeicao$ = "Always"      => "Sempre"`
  - `$come_entre_refeicao$ = "Sometimes"   => "Às Vezes"`
  - `TRUE => $come_entre_refeicao$`

- **Monitora Calorias (Rule Engine #14)** — `monitora_calorias`
  - `$monitora_calorias$ = "yes" => "Sim"`
  - `$monitora_calorias$ = "no"  => "Não"`
  - `TRUE => $monitora_calorias$`

- **Consumo Álcool (Rule Engine #15)** — `frequencia_consumo_alcool`
  - `$frequencia_consumo_alcool$ = "no"         => "Não"`
  - `$frequencia_consumo_alcool$ = "Frequently" => "Frequentemente"`
  - `$frequencia_consumo_alcool$ = "Always"     => "Sempre"`
  - `$frequencia_consumo_alcool$ = "Sometimes"  => "Às Vezes"`
  - `TRUE => $frequencia_consumo_alcool$`

- **Fumante (Rule Engine #16)** — `fumante`
  - `$fumante$ = "yes" => "Sim"`
  - `$fumante$ = "no"  => "Não"`
  - `TRUE => $fumante$`

- **Meio de Transporte (Rule Engine #17)** — `meio_de_transporte`
  - `"Motorbike"             => "Moto"`
  - `"Public_Transportation" => "Transporte Público"`
  - `"Automobile"            => "Carro"`
  - `"Bike"                  => "Bicicleta"`
  - `"Walking"               => "A Pé"`
  - `TRUE => $meio_de_transporte$`

- **Nível de Obesidade (Rule Engine #18)** — `nivel_obesidade`
  - `"Normal_Weight"       => "Peso Normal"`
  - `"Insufficient_Weight" => "Peso Insuficiente"`
  - `"Overweight_Level_I"  => "Sobrepeso Nível I"`
  - `"Overweight_Level_II" => "Sobrepeso Nível II"`
  - `"Obesity_Type_I"      => "Obesidade Grau I"`
  - `"Obesity_Type_II"     => "Obesidade Grau II"`
  - `"Obesity_Type_III"    => "Obesidade Grau III"`
  - `TRUE => $nivel_obesidade$`

- **At. Física Texto (Rule Engine #22)** — substitui `freq_atividade_fisica` por texto
  - `$freq_atividade_fisica$ = 0 => "Nenhuma atividade"`
  - `$freq_atividade_fisica$ = 1 => "1–2x por semana"`
  - `$freq_atividade_fisica$ = 2 => "3–4x por semana"`
  - `$freq_atividade_fisica$ = 3 => "5x ou mais"`
  - `TRUE => "Indefinido"`

---

### 5) Gravação no PostgreSQL
- **PostgreSQL Connector (#8)**: conexão com banco (credenciais configuradas localmente no KNIME).
- **DB Writer (#9)**: grava o dataset na tabela:
  - `public.obesidade`

---

## Como executar (resumo)
1) Abrir/importar o workflow no KNIME
2) Ajustar o caminho do CSV no **CSV Reader**
3) Ajustar a conexão no **PostgreSQL Connector**
4) Conferir destino no **DB Writer** (`public.obesidade`)
5) Executar o workflow do início ao fim
