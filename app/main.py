from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from typing import Dict, Any, Union

import json

from utils.config import setup_logging
from scraping.category_data import fetch_category_data
# from source.funcoes.funcao_extracao_cte import configurar_logging
# from source.funcoes.geral import extracao
# from source.funcoes.certificado import instalando_certificado

app = FastAPI(
    title="API - Extração de Dados de Maquinário",
    version="1.0.0",
    docs_url="/",
    description=(
        "Esta API tem como objetivo centralizar o processo de coleta automatizada de dados "
        "relacionados a maquinário. A estrutura foi projetada para permitir futuras atualizações "
        "automatizadas, assumindo que os sites mantenham a estrutura atual."
    )
)

@app.post("/coleta", response_model=None, tags=["BALDOR"])
async def processo_de_coleta(consulta: str) -> Union[FileResponse, Dict[str, Any]]:
    """
    Realiza a coleta automatizada de dados de maquinário a partir do site especificado.
    ### Sites atualmente disponíveis:
    - **BALDOR** — [Baldor Electric Company](https://www.baldor.com/).
    ### Parâmetros:
    - **Consulta** (str): Nome do site a ser consultado.
    - **Exemplo:** _BALDOR_.
    ### Retorno:
    - Um arquivo JSON contendo os dados extraídos do site selecionado.
    ### Tempo estimado de execução:
    - **Mínimo**: 1 minuto.
    - **Médio**: 3 minutos.
    - **Máximo**: 5 minutos.
        - Obs: A execução depende da estabilidade do site e da quantidade de dados retornados.
    """

    # configurar_logging("history_log")
    setup_logging("history_log")

    # coletando dados da categoria e salvando em um arquivo JSON
    category_data = fetch_category_data()
    with open("category_data.json", "w") as f:
        json.dump(category_data, f, indent=2)
    