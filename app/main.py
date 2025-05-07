from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from typing import Dict, Any, Union
import requests
import json
import time
import os
from glob import glob

from utils.general_utils import setup_logging, CHECKPOINT, save_checkpoint, load_checkpoint
from utils.pre_process import clean_bom
from utils.download_files import download_product_files

from scraping.baldor_scraping import fetch_category_data, fetch_subcategory_data, fetch_subsubcategory_data, fetch_products_data
from scraping.baldor_output import output_formater
from scraping.final_output import build_final_output

session = requests.Session()  

app = FastAPI(
    title="API - Machinery Data Extraction",
    version="1.0.0",
    docs_url="/",
    description=(
        "This API centralizes the automated collection of machinery related data. "
        "The architecture is designed to allow seamless, future updates provided the target "
        "websites keep their current structure."
    )
)

logger = setup_logging("history_log")

@app.post("/coleta", response_model=None, tags=["BALDOR"])
async def processo_de_coleta(consulta: str) -> Union[FileResponse, Dict[str, Any]]:
    """
    Performs automated machinery‑data collection from the specified website.
    
    Currently supported websites
    - **BALDOR** - [Baldor Electric Company](https://www.baldor.com/)

    Parameters
    - **Consulta** (str) - Name of the website to query.  
    - **Example** - **BALDOR**

     Returns
    - A JSON file containing the data extracted from the selected site.

    Estimated runtime
    - **Minimum:** 30 minutes  
    - **Average:** 1 hour  
    - **Maximum:** 5 hours  
      *Note:* The actual time depends on site stability and the amount of data returned.
    """

    if consulta.upper() != "BALDOR":
        raise HTTPException(status_code=400, detail="Query not yet supported.")

    MAX_RETRIES = 5
    for attempt in range(MAX_RETRIES):
        try:
            data = load_checkpoint()
            if data is None:
                data = fetch_category_data()
                data = fetch_subcategory_data(data)
                data = fetch_subsubcategory_data(data)
                data = fetch_products_data(data)

            clean_bom(data)

            download_product_files(data)

            import pprint
            pprint.pprint(data, depth=4)

            output_formater(data)  

            final_output = build_final_output(data) 

            os.makedirs("data", exist_ok=True)
            with open("data/final_output.json", "w", encoding="utf-8") as f:
                json.dump(final_output, f, ensure_ascii=False, indent=2)

            if os.path.exists(CHECKPOINT):
                os.remove(CHECKPOINT)

            return JSONResponse(content=final_output)

        except Exception as exc:
            logger.warning(f"Attempt {attempt+1}/{MAX_RETRIES} failed: {exc}. Retrying in 5 minutes...")
            save_checkpoint(data)
            session.cookies.clear()
            time.sleep(5 * 60)

    raise HTTPException(status_code=500, detail="Maximum retries reached. Process aborted.")

@app.get("/ready", tags=["Status"], status_code=200)
async def status():
    return {"status": "API running correctly!"}

