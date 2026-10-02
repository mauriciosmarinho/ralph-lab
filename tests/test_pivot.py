import csv
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SAIDA = ROOT / "pivot_receita.csv"


@pytest.fixture(scope="module")
def linhas():
    import sys

    sys.path.insert(0, str(ROOT))
    import join
    import pivot

    join.main()
    pivot.main()
    with open(SAIDA, newline="", encoding="utf-8") as f:
        return list(csv.reader(f))


def test_cabecalho_exato(linhas):
    assert linhas[0] == ["regiao", "2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "2026-06"]


def test_soma_total(linhas):
    total = sum(float(v) for linha in linhas[1:] for v in linha[1:])
    assert total == pytest.approx(931274.06, abs=0.5)


def test_forma_final(linhas):
    assert len(linhas) == 5
    assert all(len(linha) == 7 for linha in linhas)
    assert [linha[0] for linha in linhas[1:]] == ["Centro-Oeste", "Nordeste", "Sudeste", "Sul"]
