from ortools.linear_solver import pywraplp
import time
from src.schemas import Item


def resolver_corte(
    comprimento_padrao: int,
    itens: list[Item],
    time_limit: int = 60
) -> dict:
    inicio = time.time()

    solver = pywraplp.Solver.CreateSolver("SCIP")

    if solver is None:
        raise Exception("Não foi possível criar o solver.")

    solver.SetTimeLimit(time_limit * 1000)

    m = len(itens)

    # N = número máximo de barras (pior caso: 1 barra por item)
    N = sum(item.quantidade for item in itens)

    # Variáveis de decisão
    x = {}  # quantidade do item i na barra j
    y = {}  # indica se a barra j é usada (0 ou 1)

    for j in range(N):
        y[j] = solver.BoolVar(f"y_{j}")

        for i, item in enumerate(itens):
            # quantidade limitada pela demanda do item (mais eficiente)
            x[i, j] = solver.IntVar(0, item.quantidade, f"x_{i}_{j}")

    # ----------------------------
    # Restrição de demanda
    # ----------------------------
    for i, item in enumerate(itens):
        solver.Add(
            sum(x[i, j] for j in range(N)) >= item.quantidade
        )

    # ----------------------------
    # Restrição de capacidade
    # ----------------------------
    for j in range(N):
        solver.Add(
            sum(
                itens[i].comprimento * x[i, j]
                for i in range(m)
            ) <= comprimento_padrao * y[j]
        )

    # ----------------------------
    # Função objetivo
    # ----------------------------
    solver.Minimize(sum(y[j] for j in range(N)))

    status = solver.Solve()
    tempo = time.time() - inicio

    # ----------------------------
    # Status formatado
    # ----------------------------
    if status == pywraplp.Solver.OPTIMAL:
        status_str = "OPTIMAL"
    elif status == pywraplp.Solver.FEASIBLE:
        status_str = "FEASIBLE"
    elif status == pywraplp.Solver.INFEASIBLE:
        status_str = "INFEASIBLE"
    else:
        status_str = "UNKNOWN"

    # ----------------------------
    # Construção da solução
    # ----------------------------
    plano = []
    desperdicio_total = 0
    barras_utilizadas = 0

    for j in range(N):

        if y[j].solution_value() > 0.5:
            barras_utilizadas += 1

            itens_cortados = []
            utilizado = 0

            for i, item in enumerate(itens):
                qtd = int(round(x[i, j].solution_value()))

                if qtd > 0:
                    itens_cortados.append({
                        "item_id": item.id,
                        "quantidade": qtd
                    })

                    utilizado += qtd * item.comprimento

            sobra = comprimento_padrao - utilizado
            desperdicio_total += sobra

            plano.append({
                "barra_id": barras_utilizadas,
                "itens_cortados": itens_cortados,
                "comprimento_utilizado": utilizado,
                "sobra": sobra
            })

    return {
        "status_solver": status_str,
        "tempo_execucao_segundos": round(tempo, 4),
        "barras_utilizadas": barras_utilizadas,
        "desperdicio_total_mm": desperdicio_total,
        "plano_corte": plano
    }