import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SAIDA = ROOT / "index.html"


@pytest.fixture(scope="module")
def html():
    import sys

    sys.path.insert(0, str(ROOT))
    import join
    import pivot
    import web

    join.main()
    pivot.main()
    web.main()
    return SAIDA.read_text(encoding="utf-8")


def test_elemento_grafico(html):
    assert "<canvas" in html
    assert "new Chart(" in html


def test_dados_do_pivot(html):
    for mes in ["2026-01", "2026-06"]:
        assert mes in html
    for regiao in ["Centro-Oeste", "Nordeste", "Sudeste", "Sul"]:
        assert regiao in html


def test_paragrafo_conclusao(html):
    paragrafos = [re.sub(r"<[^>]+>", "", p) for p in re.findall(r"<p[^>]*>(.*?)</p>", html, re.S)]
    conclusao = max(paragrafos, key=len)
    assert len(conclusao) >= 300
    assert "Sudeste" in conclusao
    assert "orfas" in conclusao
    assert "108/Batel" in conclusao
