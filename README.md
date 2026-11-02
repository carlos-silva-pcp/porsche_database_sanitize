# Porsche Sales Intelligence

### Data Analytics | Python | Data Cleaning | Business Intelligence | HTML, CSS & JavaScript

Projeto de tratamento, transformação e análise de dados de vendas de veículos Porsche, desenvolvido para transformar uma base comercial em informações estruturadas, indicadores de desempenho e insights estratégicos.

A solução contempla duas etapas principais:

1. **Data Cleaning & Transformation:** padronização e validação dos dados utilizando Python e regras documentadas em um arquivo `schema.md`.
2. **Business Intelligence & Data Visualization:** construção de uma dashboard interativa para análise de faturamento, vendedores, modelos, cidades e comportamento histórico dos clientes.

O projeto foi desenvolvido para fins de estudo e portfólio, simulando um cenário de análise comercial no segmento automotivo de luxo.

---

## 1. Objetivo do projeto

Transformar dados de vendas em informações confiáveis e acessíveis para responder a perguntas relevantes ao negócio.

O projeto busca compreender:

- Quais modelos Porsche apresentam maior volume de vendas?
- Quais modelos lideram as vendas em cada cidade?
- Quais vendedores apresentam maior faturamento?
- Como o desempenho comercial varia entre vendedores e regiões?
- Qual é o ticket médio das vendas?
- Quais clientes apresentam histórico de compras recorrentes?
- Quais clientes podem ser priorizados em futuras ações de relacionamento?

A proposta é utilizar dados históricos para apoiar análises de desempenho, identificação de padrões e oportunidades comerciais.

## 2. Fonte e estrutura dos dados

A base analisada contém **100 registros de vendas**, com informações sobre veículos, clientes, vendedores, preços e localização.

Os principais campos utilizados são:

| Campo | Descrição |
|---|---|
| `sale_id` | Identificador da venda |
| `SaleDateSanitized` | Data da venda padronizada |
| `CustomerNameSanitized` | Nome do cliente padronizado |
| `PorscheModelSanitized` | Modelo Porsche padronizado |
| `ModelYearSanitized` | Ano do modelo |
| `SalePriceSanitized` | Valor da venda em USD |
| `VehicleMileageSanitized` | Quilometragem em milhas |
| `PaymentMethodSanitized` | Método de pagamento |
| `CitySanitized` | Cidade da venda |
| `StateSanitized` | Estado americano |
| `SalesPersonSanitized` | Vendedor responsável |
| `DeliveryStatusSanitized` | Situação da entrega |

A base possui informações comerciais de cidades dos Estados Unidos, com valores monetários expressos em dólares americanos (USD).

## 3. Tratamento e qualidade dos dados

Antes da construção da dashboard, foi implementado um processo de sanitização utilizando Python.

As regras de tratamento foram documentadas no arquivo `schema.md`, permitindo definir padrões consistentes para cada atributo.

### Principais transformações

| Campo | Regra aplicada |
|---|---|
| Datas | Conversão para `YYYY-MM-DD` |
| Clientes | Padronização dos nomes próprios |
| Vendedores | Normalização de espaços, maiúsculas e minúsculas |
| Modelos Porsche | Padronização de modelos e versões |
| Ano do modelo | Conversão para ano com quatro dígitos |
| Preço | Conversão para valor numérico em USD |
| Quilometragem | Conversão para milhas inteiras |
| Pagamento | Padronização dos métodos de pagamento |
| Cidade | Normalização para Title Case |
| Estado | Conversão para siglas USPS |
| Entrega | Padronização das situações de entrega |

### Tratamento de valores inválidos

Quando um valor não pode ser convertido com segurança, a regra de sanitização determina a utilização de `INVALID`.

Essa abordagem evita correções arbitrárias e facilita a identificação de problemas de qualidade.

A lógica também busca preservar as informações originais, permitindo comparar os valores de origem com os valores tratados.

### Por que padronizar nomes?

Um mesmo vendedor pode aparecer na base com diferentes formatações:

- `WILLIAM CLARK`
- `william  clark`
- `William Clark`

Sem padronização, esses registros poderiam ser interpretados como vendedores diferentes, comprometendo os resultados de faturamento e volume de vendas.

A normalização reduz esse problema, embora não substitua a necessidade de identificadores únicos para distinguir pessoas com nomes semelhantes.

---

## 4. Lógica dos indicadores (KPIs)

A dashboard utiliza os registros filtrados para calcular os indicadores de desempenho comercial.

### Faturamento total

Soma dos valores de todas as vendas consideradas no recorte.

`Faturamento Total = SUM(SalePriceSanitized)`

**Objetivo:** mensurar o volume financeiro movimentado.

### Veículos vendidos

Quantidade de registros de vendas.

`Veículos Vendidos = COUNT(sale_id)`

**Objetivo:** acompanhar o volume comercial.

### Ticket médio

Relação entre o faturamento total e a quantidade de vendas.

`Ticket Médio = Faturamento Total / Quantidade de Vendas`

**Objetivo:** compreender o valor médio das transações.

### Cidades atendidas

Quantidade de cidades distintas com registros de vendas.

`Cidades Atendidas = COUNT DISTINCT(CitySanitized)`

**Objetivo:** identificar a abrangência geográfica das operações.

Todos esses indicadores são recalculados dinamicamente conforme os filtros selecionados.

---

## 5. Perguntas de negócio

### Pergunta 1 — Quais são os modelos Porsche mais vendidos?

**Lógica de análise:**

Agrupar as vendas por `PorscheModelSanitized`, contar os registros e ordenar os modelos pela quantidade vendida.

**Indicador utilizado:** volume de veículos por modelo.

**Aplicação no negócio:**

- Identificar modelos de maior demanda histórica.
- Apoiar análises de composição do portfólio.
- Subsidiar decisões sobre estoque e planejamento comercial.

### Pergunta 2 — Quais modelos lideram as vendas em cada cidade?

**Lógica de análise:**

Agrupar os registros por cidade e modelo, calcular a quantidade de vendas de cada combinação e identificar o modelo com maior volume em cada cidade.

A participação local é calculada por:

`Participação Local (%) = Vendas do Modelo / Total de Vendas da Cidade × 100`

**Aplicação no negócio:**

- Identificar preferências regionais observadas na base.
- Comparar o desempenho dos modelos entre mercados.
- Apoiar estratégias comerciais regionalizadas.

**Limitação:** em cidades com poucos registros, a liderança de um modelo pode não representar uma tendência consolidada.

### Pergunta 3 — Quais vendedores apresentam maior faturamento?

**Lógica de análise:**

Agrupar os registros por `SalesPersonSanitized` e somar os valores de `SalePriceSanitized`.

`Faturamento por Vendedor = SUM(Vendas do Vendedor)`

A dashboard apresenta um ranking dos vendedores com maior faturamento.

**Aplicação no negócio:**

- Identificar os maiores volumes financeiros por vendedor.
- Comparar resultados comerciais.
- Apoiar análises de produtividade e distribuição das vendas.

O faturamento isolado não representa necessariamente a eficiência individual, pois a base não informa metas, carteira de clientes ou oportunidades disponíveis para cada vendedor.

### Pergunta 4 — Quais insights podem ser extraídos por cidade?

**Lógica de análise:**

Combinar informações de cidade, modelo, quantidade de vendas e faturamento.

A dashboard identifica o mercado com maior volume de vendas no recorte e o modelo mais vendido nesse mercado.

**Aplicação no negócio:**

- Identificar mercados com maior concentração de vendas.
- Observar diferenças de preferência entre cidades.
- Direcionar investigações comerciais para regiões específicas.

### Pergunta 5 — Quais clientes podem ser considerados potenciais para novas ações comerciais?

**Lógica de análise:**

Agrupar as vendas por `CustomerNameSanitized` e calcular:

- Quantidade de compras registradas por cliente.
- Valor financeiro acumulado.
- Modelos presentes no histórico.

Clientes com mais de uma compra são identificados como recorrentes. Clientes com maior valor acumulado podem ser priorizados para análise de relacionamento.

**Aplicação no negócio:**

- Identificar clientes de alto valor histórico.
- Reconhecer padrões de recorrência.
- Apoiar ações de fidelização e relacionamento.
- Criar uma base inicial para futuras análises de CRM.

**Importante:** a base contém vendas realizadas, e não informações sobre leads, interesse declarado ou intenção futura de compra. Portanto, a classificação de clientes em potencial é exploratória, não um modelo preditivo.

---

## 6. Dashboard interativa

A dashboard foi desenvolvida utilizando HTML5, CSS3 e JavaScript.

A interface possui identidade visual inspirada na estética da Porsche, com foco em minimalismo, elegância e leitura clara dos indicadores.

### Filtros disponíveis

- Vendedor
- Modelo Porsche
- Cidade
- Método de pagamento

Os filtros são combinados, permitindo análises específicas de diferentes segmentos da base.

### Visualizações

A dashboard apresenta:

- Cards com indicadores comerciais.
- Ranking de faturamento por vendedor.
- Ranking dos modelos mais vendidos.
- Tabela dos modelos líderes por cidade.
- Insights comerciais calculados dinamicamente.
- Ranking de clientes por valor histórico e recorrência.

A aplicação funciona diretamente no navegador, sem necessidade de backend ou conexão com banco de dados, pois os registros estão incorporados ao HTML.

## 7. Tecnologias utilizadas

| Tecnologia | Aplicação |
|---|---|
| Python | Tratamento e transformação dos dados |
| Pandas | Manipulação de tabelas |
| OpenPyXL | Leitura e geração de arquivos Excel |
| Markdown | Documentação das regras de sanitização |
| HTML5 | Estrutura da dashboard |
| CSS3 | Estilização e responsividade |
| JavaScript | Filtros, cálculos e visualizações interativas |
| Excel | Fonte e armazenamento dos dados |

## 8. Fluxo de processamento

```text
Porsche Database (Excel)
          |
          v
     schema.md
  Regras de qualidade
          |
          v
    Python + Pandas
 Limpeza e padronização
          |
          v
   Base sanitizada
          |
          v
    Dashboard HTML
          |
          v
 KPIs e análises comerciais
          |
          v
    Insights de negócio
```

## 9. Resultados e observações

Na base utilizada para a versão atual da dashboard foram identificados:

- **100 registros de vendas.**
- **94 nomes de clientes distintos.**
- **6 clientes com mais de uma compra registrada.**

Esses números descrevem a base analisada e não devem ser interpretados como indicadores do desempenho real da Porsche.

A análise também demonstra a importância de utilizar nomes padronizados e de definir regras claras de agregação para evitar inconsistências nos indicadores.

## 10. Limitações e melhorias futuras

O projeto pode ser expandido com:

- Identificadores únicos para clientes e vendedores.
- Validações adicionais de valores monetários e categorias.
- Integração com banco de dados.
- Atualização automática da dashboard.
- Análise temporal das vendas.
- Comparativos de desempenho por período.
- Segmentação de clientes por recência, frequência e valor monetário (RFM).
- Modelos de previsão de vendas, mediante disponibilidade de dados adequados.

## 11. Considerações finais

O Porsche Sales Intelligence demonstra um fluxo de trabalho que parte de dados comerciais brutos, aplica regras de qualidade e transforma os registros em visualizações voltadas à análise de negócio.

Mais do que construir uma interface, o projeto busca demonstrar a importância de conectar **qualidade de dados, regras de negócio e visualização de informações** para produzir análises mais consistentes.

---

**Disclaimer:** Projeto do bootcamp da @digitalinnovationone, desenvolvido exclusivamente para fins educacionais e de portfólio. Não possui vínculo, patrocínio ou associação oficial com a Porsche AG.








