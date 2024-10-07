from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed

# Internal modules imports
from utils.case_details import get_case_details  # Make sure this is synchronous

app = APIRouter()

class DataPayloadBulkCase(BaseModel):
    cinos: List[str]

@app.post('/case_details_bulk')
async def case_details(data: DataPayloadBulkCase):
    results = []
    
    with ThreadPoolExecutor() as executor:
        futures = {}

        for cino in data.cinos:
            data_payload = {
                'cino': cino,
                'source': 'undefined'
            }
            # Schedule the get_case_details function to be run with the executor
            future = executor.submit(get_case_details, data_payload)
            futures[future] = cino  # Map future to cino

        for future in as_completed(futures):
            cino = futures[future]  # Get the cino from the mapping
            try:
                table_data = future.result()  # Get the result of the future
                results.append({
                    'cino': cino,
                    'data': table_data
                })
            except Exception as e:
                results.append({
                    'cino': cino,
                    'error': str(e)
                })

    return {"results": results}
