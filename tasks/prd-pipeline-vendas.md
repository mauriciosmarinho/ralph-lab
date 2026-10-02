# PRD: Pipeline CSV → Gráfico (vendas por loja)

## Introdução/Visão Geral

Construir um pipeline de dados que transforma dois CSVs brutos (`vendas.csv`,
`lojas.csv`, já presentes na raiz do repo) numa página web com gráfico de
receita mensal por região. O pipeline tem três saídas obrigatórias na raiz do
repositório: `vendas_lojas.csv` (inner join), `pivot_receita.csv` (pivot
região × mês) e `index.html` (gráfico + conclusão).

Os dados têm duas armadilhas propositais que o pipeline precisa tratar sem
apagar nem inventar nada:

1. Três vendas em `vendas.csv` têm `id_loja = 999`, que não existe em
   `lojas.csv` (linhas `V00421`, `V00422`, `V00423`, somando R$ 8.120,00).
2. A loja `108` (Batel/PR) existe em `lojas.csv` mas não tem nenhuma venda em
   `vendas.csv`.

## Metas

- Produzir o inner join dos dois arquivos por `id_loja`, descartando apenas as
  3 vendas órfãs (não a loja 108, que simplesmente não aparece no resultado de
  um inner join — isso é esperado, não um bug a corrigir).
- Produzir o pivot de receita por região × mês a partir do join.
- Produzir uma página HTML estática com gráfico da receita mensal por região e
  um parágrafo de conclusão (≥ 300 caracteres) que mencione as duas armadilhas
  e seu efeito no relatório.
- Cada etapa prova que está correta com testes automatizados (`pytest`).

## Valores de conferência (não negociáveis)

| Métrica | Valor esperado |
|---|---|
| Linhas de dados em `vendas_lojas.csv` | 420 |
| Soma de `receita_brl` no join | 931274.06 (±0.5) |
| Forma do pivot | 4 linhas × 7 colunas |
| Soma de todas as células numéricas do pivot | 931274.06 (±0.5) |
| Cabeçalho do pivot (exato) | `regiao,2026-01,2026-02,2026-03,2026-04,2026-05,2026-06` |
| Região líder | Sudeste, R$ 265.077,49 |

## User Stories

### US-001: Inner join de vendas e lojas
**Descrição:** Como analista, preciso juntar `vendas.csv` e `lojas.csv` por
`id_loja` para ter cada venda associada à sua região, mantendo só vendas com
loja válida.

**Critérios de aceitação:**
- [ ] Script lê `vendas.csv` e `lojas.csv` da raiz do repo
- [ ] `receita_brl` é lido como número (ponto decimal), nunca como texto
- [ ] Inner join por `id_loja`: as 3 vendas com `id_loja=999` NÃO entram no resultado
- [ ] Resultado salvo em `vendas_lojas.csv` na raiz do repo, mantendo a coluna `receita_brl` com esse nome exato
- [ ] `vendas.csv` e `lojas.csv` originais não são alterados
- [ ] `tests/test_join.py` com pelo menos 2 testes: (1) `vendas_lojas.csv` tem exatamente 420 linhas de dados, (2) soma de `receita_brl` é 931274.06 com tolerância de 0.5
- [ ] `pytest tests/test_join.py` passa

### US-002: Pivot de receita por região × mês
**Descrição:** Como analista, preciso agregar a receita do join por região e
mês para visualizar a evolução temporal por região.

**Critérios de aceitação:**
- [ ] Script lê `vendas_lojas.csv` (saída da US-001)
- [ ] Extrai `YYYY-MM` da coluna `data` para agrupar por mês
- [ ] Gera pivot com linhas = região (`Centro-Oeste`, `Nordeste`, `Sudeste`, `Sul`) e colunas = meses `2026-01` a `2026-06`
- [ ] Salva em `pivot_receita.csv` na raiz, cabeçalho EXATO: `regiao,2026-01,2026-02,2026-03,2026-04,2026-05,2026-06`
- [ ] Valores com ponto decimal, 2 casas, sem `R$` e sem separador de milhar
- [ ] Forma final: 4 linhas de dados + 1 cabeçalho, 7 colunas
- [ ] `tests/test_pivot.py` com pelo menos 2 testes: (1) cabeçalho exato, (2) soma de todas as células numéricas é 931274.06 com tolerância de 0.5
- [ ] `pytest tests/test_pivot.py` passa

### US-003: Página web com gráfico e conclusão
**Descrição:** Como leitor do relatório, preciso ver a receita mensal por
região num gráfico e entender, em texto, o que os números significam —
incluindo o efeito das duas armadilhas dos dados no relatório.

**Critérios de aceitação:**
- [ ] `index.html` na raiz do repo, página estática (pode usar Chart.js via CDN ou SVG/canvas gerado localmente)
- [ ] Contém elemento de gráfico reconhecível (`<canvas>`, `<svg>`, `Chart(`, `plotly`, `echarts`, `d3.` ou `vega`) mostrando receita mensal por região, usando os dados de `pivot_receita.csv`
- [ ] Contém um `<p>` de conclusão com no mínimo 300 caracteres, mencionando: a região líder (Sudeste), e o efeito de cada armadilha no relatório (as 3 vendas órfãs — R$ 8.120,00 — somem do relatório; a loja 108/Batel não aparece no pivot porque não teve vendas)
- [ ] `tests/test_web.py` com pelo menos 1 teste verificando a presença do elemento de gráfico e do parágrafo de conclusão com 300+ caracteres
- [ ] `pytest tests/test_web.py` passa

## Não-objetivos (fora de escopo)

- Não editar `vendas.csv` ou `lojas.csv` originais.
- Não usar left join nem reportar a loja 108 ou as vendas órfãs como se tivessem dados — a omissão delas é o ponto pedagógico do exercício, não um bug.
- Sem framework de frontend, sem build step — HTML estático simples.
- Sem necessidade de typecheck (projeto é Python puro); o gate de qualidade de cada story é `pytest` verde para o arquivo de teste daquela story.

## Considerações Técnicas

- Linguagem: Python (pandas ou csv/stdlib — escolha do agente).
- `pytest` deve ser executável com `python -m pytest` a partir da raiz do repo.
- Cada story deve terminar com um commit próprio.

## Métricas de Sucesso

- `pytest -q` na raiz do repo roda ≥ 4 testes, todos passando.
- Os 3 arquivos de saída existem na raiz com os valores de conferência exatos.

## Questões Abertas

- Nenhuma — todos os valores de conferência já são conhecidos (ver tabela acima).
