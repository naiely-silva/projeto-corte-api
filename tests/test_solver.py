from src.solver import resolver_corte
from src.schemas import Item


def test_solver_basico():

    itens = [
        Item(
            id="A",
            comprimento=1000,
            quantidade=2
        )
    ]

    resultado = resolver_corte(
        comprimento_padrao=3000,
        itens=itens
    )

    assert resultado["barras_utilizadas"] >= 1


def test_status_solver():

    itens = [
        Item(
            id="A",
            comprimento=500,
            quantidade=2
        )
    ]

    resultado = resolver_corte(
        comprimento_padrao=3000,
        itens=itens
    )

    assert resultado["status_solver"] in [
        "OPTIMAL",
        "FEASIBLE"
    ]