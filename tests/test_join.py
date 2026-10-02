import csv
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SAIDA = ROOT / "vendas_lojas.csv"


@pytest.fixture(scope="module")
def linhas():
    import sys

    sys.path.insert(0, str(ROOT))
    import join

    join.main()
    with open(SAIDA, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_420_linhas(linhas):
    assert len(linhas) == 420


def test_soma_receita(linhas):
    assert sum(float(l["receita_brl"]) for l in linhas) == pytest.approx(931274.06, abs=0.5)


def test_sem_vendas_orfas(linhas):
    assert all(l["id_loja"] != "999" for l in linhas)
    assert "receita_brl" in linhas[0]
