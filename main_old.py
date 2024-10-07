# Fast API Imports

from fastapi import APIRouter, File, UploadFile, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi import FastAPI
from typing import List
from fastapi.middleware.cors import CORSMiddleware


from concurrent.futures import ThreadPoolExecutor
import asyncio


# Internal modules imports
from utils.case_details import get_case_details

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

class DataPayloadBulkCase(BaseModel):
    cinos: List[str]



# @app.post('/case_details_bulk')
# async def case_details(data: DataPayloadBulkCase):
#     try:
#         results = []
        
#         for cino in data.cinos:
#             data_payload = {
#                 'cino': cino,
#                 'source': 'undefined'
#             }
#             table_data = await get_case_details(data_payload['cino'])
#             results.append({
#                 'cino': cino,
#                 'data': table_data
#             })
        
#         return {"results": results}
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))



@app.post('/case_details_bulk')
async def case_details(data: DataPayloadBulkCase):
    loop = asyncio.get_event_loop()
    results = []

    with ThreadPoolExecutor() as pool:
        futures = []
        
        for cino in data.cinos:
            data_payload = {
                'cino': cino,
                'source': 'undefined'
            }
            futures.append(loop.run_in_executor(pool, get_case_details, data_payload))

        for future in asyncio.as_completed(futures):
            table_data = await future
            results.append({
                'cino': future.cino,  # You might want to handle this differently
                'data': table_data
            })

    return {"results": results}
