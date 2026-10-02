"""US-003: pagina estatica com grafico (Chart.js) e conclusao (pivot_receita.csv -> index.html)."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ENTRADA = ROOT / "pivot_receita.csv"
SAIDA = ROOT / "index.html"

CORES = ["#2a78d6", "#e8862f", "#2e9e6a", "#c4448f"]


def brl(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def ler_pivot():
    with open(ENTRADA, newline="", encoding="utf-8") as f:
        linhas = list(csv.reader(f))
    meses = linhas[0][1:]
    regioes = {linha[0]: [float(v) for v in linha[1:]] for linha in linhas[1:]}
    return meses, regioes


def conclusao(regioes):
    totais = {regiao: sum(valores) for regiao, valores in regioes.items()}
    lider = max(totais, key=totais.get)
    total = sum(totais.values())
    return (
        f"Entre janeiro e junho de 2026 a receita total do relatorio foi de {brl(total)}, "
        f"e o {lider} foi a regiao lider, com {brl(totais[lider])}, seguido de perto por "
        f"Nordeste e Centro-Oeste; o Sul fica bem abaixo, com {brl(totais['Sul'])}. "
        "Dois cuidados com os dados afetam esse retrato. Primeiro, as 3 vendas orfas "
        "(id_loja=999, somando R$ 8.120,00) nao tem loja cadastrada e por isso somem do "
        "relatorio no inner join: a receita real da empresa e maior do que a mostrada aqui. "
        "Segundo, a loja 108/Batel (Sul, PR) existe no cadastro mas nao teve nenhuma venda, "
        "entao nao aparece no pivot; a receita do Sul vem so da loja 107/Moinhos, o que "
        "explica boa parte da distancia para as outras regioes."
    )


def gerar_html(meses, regioes):
    datasets = [
        {"label": regiao, "data": valores, "borderColor": cor, "backgroundColor": cor, "tension": 0.2}
        for (regiao, valores), cor in zip(regioes.items(), CORES)
    ]
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <title>Receita mensal por regiao - 1o semestre 2026</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>
  <style>
    body {{ font-family: system-ui, sans-serif; max-width: 860px; margin: 2rem auto; padding: 0 1rem; color: #222; }}
    p.conclusao {{ line-height: 1.5; }}
  </style>
</head>
<body>
  <h1>Receita mensal por regiao (jan-jun 2026)</h1>
  <canvas id="grafico" aria-label="Receita mensal por regiao" role="img"></canvas>
  <h2>Conclusao</h2>
  <p class="conclusao" id="conclusao">{conclusao(regioes)}</p>
  <script>
    new Chart(document.getElementById("grafico"), {{
      type: "line",
      data: {{ labels: {json.dumps(meses)}, datasets: {json.dumps(datasets, ensure_ascii=False)} }},
      options: {{
        plugins: {{ title: {{ display: true, text: "Receita (R$) por regiao e mes - fonte: pivot_receita.csv" }} }},
        scales: {{ y: {{ beginAtZero: true, title: {{ display: true, text: "Receita (R$)" }} }} }}
      }}
    }});
  </script>
</body>
</html>
"""


def main():
    meses, regioes = ler_pivot()
    html = gerar_html(meses, regioes)
    SAIDA.write_text(html, encoding="utf-8")
    return html


if __name__ == "__main__":
    main()
    print(f"pagina gravada em {SAIDA.name}")
