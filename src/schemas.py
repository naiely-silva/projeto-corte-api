from pydantic import BaseModel, Field, model_validator
from typing import List

class Item(BaseModel):
    id: str = Field(..., description="Identificador do item")
    comprimento: int = Field(..., gt=0, description="Comprimento do item")
    quantidade: int = Field(..., gt=0, description="Quantidade solicitada")


class OtimizacaoRequest(BaseModel):
    comprimento_padrao: int = Field(
        ..., gt=0, description="Comprimento da barra padrão"
    )
    itens: List[Item]
    time_limit: int = Field(
        default=60,
        ge=1,
        le=120,
        description="Tempo máximo de execução em segundos"
    )

    @model_validator(mode="after")
    def validar_itens(self):
        for item in self.itens:
            if item.comprimento > self.comprimento_padrao:
                raise ValueError(
                    f"O item '{item.id}' possui comprimento maior que a barra padrão."
                )
        return self


class ItemCortado(BaseModel):
    item_id: str
    quantidade: int


class BarraResposta(BaseModel):
    barra_id: int
    itens_cortados: List[ItemCortado]
    comprimento_utilizado: int
    sobra: int


class OtimizacaoResponse(BaseModel):
    status_solver: str
    tempo_execucao_segundos: float
    barras_utilizadas: int
    desperdicio_total_mm: int
    plano_corte: List[BarraResposta]


class HealthResponse(BaseModel):
    status: str