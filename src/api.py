from fastapi import FastAPI, Depends

from src.config import get_settings
from src.schemas import (
    OtimizacaoRequest,
    OtimizacaoResponse,
    HealthResponse
)

from src.solver import resolver_corte
from src.auth import verificar_api_key

app = FastAPI(
    title="API de Otimização para Corte Unidimensional",
    description="""
API REST desenvolvida para resolver o Problema de Corte Unidimensional utilizando Programação  Linear Inteira com Google OR-Tools.

Projeto Final da disciplina Laboratório de Otimização - UFC.
""",
    version="1.0.0"
)

settings = get_settings()

@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["Health"]
)
def health():
    return HealthResponse(
        status="ok",
        versao=settings.app_version
    )


@app.post(
    "/otimizar",
    response_model=OtimizacaoResponse,
    tags=["Otimização"],
    dependencies=[Depends(verificar_api_key)]
)
def otimizar(dados: OtimizacaoRequest):

    resultado = resolver_corte(
        comprimento_padrao=dados.comprimento_padrao,
        itens=dados.itens,
        time_limit=dados.time_limit
    )

    return resultado