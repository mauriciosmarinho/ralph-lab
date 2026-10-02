"""US-001: inner join de vendas.csv com lojas.csv por id_loja -> vendas_lojas.csv."""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VENDAS = ROOT / "vendas.csv"
LOJAS = ROOT / "lojas.csv"
SAIDA = ROOT / "vendas_lojas.csv"


def ler_csv(caminho):
    with open(caminho, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def inner_join(vendas, lojas):
    lojas_por_id = {loja["id_loja"]: loja for loja in lojas}
    resultado = []
    for venda in vendas:
        loja = lojas_por_id.get(venda["id_loja"])
        if loja is None:  # venda orfa (ex.: id_loja=999) fica de fora
            continue
        linha = {**venda, **loja}
        linha["receita_brl"] = float(venda["receita_brl"])
        resultado.append(linha)
    return resultado


def main():
    vendas = ler_csv(VENDAS)
    lojas = ler_csv(LOJAS)
    linhas = inner_join(vendas, lojas)
    colunas = list(vendas[0].keys()) + [c for c in lojas[0].keys() if c != "id_loja"]
    with open(SAIDA, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=colunas)
        writer.writeheader()
        for linha in linhas:
            writer.writerow({**linha, "receita_brl": f"{linha['receita_brl']:.2f}"})
    return linhas


if __name__ == "__main__":
    linhas = main()
    print(f"{len(linhas)} linhas gravadas em {SAIDA.name}")
