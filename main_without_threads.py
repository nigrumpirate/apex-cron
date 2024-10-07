from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

# Internal modules imports
from utils.case_details import get_case_details

app = APIRouter()

class DataPayloadBulkCase(BaseModel):
    cinos: List[str]

@app.post('/case_details_bulk')
async def case_details(data: DataPayloadBulkCase):
    results = []

    for cino in data.cinos:
        data_payload = {
            'cino': cino,
            'source': 'undefined'
        }

        try:
            # Await the call to get_case_details directly
            table_data = await get_case_details(data_payload)
            results.append({
                'cino': cino,
                'data': table_data
            })
        except Exception as e:
            # Handle the exception for this specific case
            results.append({
                'cino': cino,
                'error': str(e)
            })

    return {"results": results}
