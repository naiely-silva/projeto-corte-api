# API de Otimização para o Problema de Corte Unidimensional

Projeto Final da disciplina **Laboratório de Otimização** – Universidade Federal do Ceará (UFC).

---

## Deploy

API: https://projeto-corte-api.onrender.com  
Swagger: https://projeto-corte-api.onrender.com/docs

# Descrição

Esta API resolve o **Problema de Corte Unidimensional (Cutting Stock Problem)** utilizando **Programação Inteira** com o **Google OR-Tools**.

O objetivo é minimizar a quantidade de barras utilizadas para atender toda a demanda de itens, gerando um plano de corte e informando o desperdício total.

---

# Cenário de Negócio

Uma empresa possui barras padrão de comprimento útil $L$ (ex: barras de aço de 6m) e deve
produzir itens menores com comprimentos $li$ em quantidades especificadas pela demanda
$di$. O objetivo é planejar os padrões de corte para satisfazer a demanda minimizando a
quantidade de barras padrão cortadas.

---

# Modelo Matemático

## Conjuntos e índices


$$i \in \{1, \dots, m\}: \quad \text{índice dos itens}$$

$$j \in \{1, \dots, N\}: \quad \text{índice das barras}$$


Onde $N$ é um limite superior do número de barras necessárias.

## Parâmetros

$$L : \text{comprimento da barra padrão}$$

$$l_i : \text{comprimento do item } i$$

$$d_i : \text{demanda do item } i$$

## Variáveis de decisão

$$y_j \in \{0,1\}, \quad \forall j$$

$$x_{ij} \in \mathbb{Z}_{\ge 0}, \quad \forall i,j$$

## Função objetivo

$$\min \sum_{j=1}^{N} y_j$$

## Restrições

Atendimento da demanda:

$\sum_{j=1}^{N} x_{ij} = d_i, \quad \forall i = 1, \dots, m$

Limite de comprimento:

$\sum_{i=1}^{m} l_i x_{ij} \leq L \cdot y_j, \quad \forall j = 1, \dots, N$

Domínio das variáveis:

$x_{ij} \in \mathbb{Z}_{\ge 0}, \quad y_j \in \{0,1\}$

---

# Tecnologias Utilizadas

- Python 3
- FastAPI
- Google OR-Tools
- Pydantic
- Uvicorn
- Pytest
- Python-dotenv

---

# Estrutura do Projeto

```
projeto_corte_api/
│
├── src/
│   ├── __init__.py
│   ├── api.py
│   ├── auth.py
│   ├── config.py
│   ├── schemas.py
│   └── solver.py
│
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   └── test_solver.py
│
├── .env
├── .gitignore
├── api_requests.http
├── README.md
└── requirements.txt
```

---

# Instalação

## 1. Criar o ambiente virtual

```bash
python -m venv .venv
```

## 2. Ativar o ambiente

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

## 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

---

# Executando a API

```bash
uvicorn src.api:app --reload
```

A API ficará disponível em:

```
http://127.0.0.1:8000
```

A documentação Swagger estará disponível em:

```
http://127.0.0.1:8000/docs
```

---

# Endpoints

## GET /health

Verifica se a API está em funcionamento.

Resposta:

```json
{
  "status": "ok"
}
```

---

## POST /otimizar

Resolve o problema de corte unidimensional.

Este endpoint requer autenticação por API Key.

---

# Autenticação

Configure a chave da API no arquivo `.env`:

```env
API_KEY=ufc2026_otimizacao
```

Envie a chave no cabeçalho da requisição:

```
X-API-Key: ufc2026_otimizacao
```

No Swagger, basta clicar em **Authorize**, informar a chave e executar as requisições protegidas.

---

# Exemplo de Entrada

```json
{
  "comprimento_padrao": 3000,
  "time_limit": 60,
  "itens": [
    {
      "id": "item_A",
      "comprimento": 1150,
      "quantidade": 3
    },
    {
      "id": "item_B",
      "comprimento": 800,
      "quantidade": 4
    }
  ]
}
```

---

# Exemplo de Saída

```json
{
  "status_solver": "OPTIMAL",
  "tempo_execucao_segundos": 0.015,
  "barras_utilizadas": 2,
  "desperdicio_total_mm": 450,
  "plano_corte": [
    {
      "barra_id": 1,
      "itens_cortados": [
        {
          "item_id": "item_A",
          "quantidade": 2
        }
      ],
      "comprimento_utilizado": 2300,
      "sobra": 700
    }
  ]
}
```

---

# Testes

Executar todos os testes:

```bash
python -m pytest
```

Ou executar com detalhes:

```bash
pytest -v
```

---