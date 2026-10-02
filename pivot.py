"""US-002: pivot de receita por regiao x mes (vendas_lojas.csv -> pivot_receita.csv)."""
import csv
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ENTRADA = ROOT / "vendas_lojas.csv"
SAIDA = ROOT / "pivot_receita.csv"

REGIOES = ["Centro-Oeste", "Nordeste", "Sudeste", "Sul"]
MESES = [f"2026-{m:02d}" for m in range(1, 7)]


def pivot(linhas):
    totais = defaultdict(float)
    for linha in linhas:
        totais[(linha["regiao"], linha["data"][:7])] += float(linha["receita_brl"])
    return {regiao: {mes: totais[(regiao, mes)] for mes in MESES} for regiao in REGIOES}


def main():
    with open(ENTRADA, newline="", encoding="utf-8") as f:
        tabela = pivot(csv.DictReader(f))
    with open(SAIDA, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["regiao"] + MESES)
        for regiao, valores in tabela.items():
            writer.writerow([regiao] + [f"{valores[mes]:.2f}" for mes in MESES])
    return tabela


if __name__ == "__main__":
    main()
    print(f"pivot gravado em {SAIDA.name}")
