import os
from dotenv import load_dotenv
from src.researcher_api import CompanyResearcherAPI

load_dotenv()

researcher = CompanyResearcherAPI()
result = researcher.search_import_data(
    "Grupo Bimbo", 
    "{company} importador México, {company} importaciones volumen USD"
)
print(result)