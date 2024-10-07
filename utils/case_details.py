# # Python modules
import requests
import json


# Internal modules
from .details_headers import caseDetailsHeaders
from .extract_tables_data import extract_tables


# # Main fuction to get case details
def get_case_details(payload):
    headers = caseDetailsHeaders

    response = requests.post('https://allahabadhighcourt.in/apps/status_ccms/index.php/get_CaseDetails', headers=headers, data=payload)
    if response.status_code == 200:
        html= response.text
        tables_data = extract_tables(html)
        return json.dumps(tables_data)  #returns all the data as a json array
    else:
        raise ValueError("Could not retrieve data from URL")



# import httpx
# import json

# # Main function to get case details
# async def get_case_details(payload):
#     headers = caseDetailsHeaders

#     async with httpx.AsyncClient() as client:
#         response = await client.post('https://allahabadhighcourt.in/apps/status_ccms/index.php/get_CaseDetails', headers=headers, data=payload)
        
#         if response.status_code == 200:
#             html = response.text
#             tables_data = extract_tables(html)
#             return json.dumps(tables_data)  # Returns all the data as a JSON array
#         else:
#             raise ValueError("Could not retrieve data from URL")
