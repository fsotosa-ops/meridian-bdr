"""
Investigador de empresas usando Serper.dev API
Busca información de importaciones y datos comerciales
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()


class CompanyResearcherAPI:
    
    def __init__(self):
        self.api_key = os.getenv("SERPER_API_KEY")
        self.base_url = "https://google.serper.dev/search"
        
        if not self.api_key:
            print("⚠️ ADVERTENCIA: No se encontró SERPER_API_KEY en .env")
    
    def search_import_data(self, company_name, query_templates):
        """
        Busca información de una empresa usando Serper.dev
        
        Args:
            company_name: Nombre de la empresa a investigar
            query_templates: String con queries separadas por coma
                            Usa {company} como placeholder
        
        Returns:
            String con resultados concatenados
        """
        
        if not self.api_key:
            return "Error: API key no configurada"
        
        # Parsear queries del template
        queries = [
            q.strip().replace("{company}", company_name) 
            for q in query_templates.split(",")
            if q.strip()
        ]
        
        all_results = []
        
        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }
        
        for query in queries:
            print(f"      🔎 {query}")
            
            try:
                response = requests.post(
                    self.base_url,
                    headers=headers,
                    json={
                        "q": query,
                        "gl": "mx",      # México
                        "hl": "es",      # Español
                        "num": 5         # Top 5 resultados
                    },
                    timeout=10
                )
                
                if response.status_code != 200:
                    print(f"      ⚠️ Error HTTP: {response.status_code}")
                    continue
                
                data = response.json()
                
                # Extraer resultados orgánicos
                organic = data.get("organic", [])
                
                for r in organic[:3]:  # Top 3 por query
                    title = r.get("title", "")
                    snippet = r.get("snippet", "")
                    
                    if title and snippet:
                        # Limpiar y concatenar
                        result = f"{title}: {snippet}"
                        all_results.append(result)
                
                # También extraer Knowledge Graph si existe
                knowledge = data.get("knowledgeGraph", {})
                if knowledge:
                    kg_title = knowledge.get("title", "")
                    kg_desc = knowledge.get("description", "")
                    if kg_title and kg_desc:
                        all_results.append(f"[Info] {kg_title}: {kg_desc}")
                        
            except requests.exceptions.Timeout:
                print(f"      ⚠️ Timeout en búsqueda")
            except Exception as e:
                print(f"      ❌ Error: {e}")
        
        # Concatenar resultados
        if all_results:
            return " | ".join(all_results)
        else:
            return "Sin información encontrada en búsquedas"
    
    def search_company_details(self, company_name):
        """
        Búsqueda rápida de detalles básicos de la empresa
        """
        return self.search_import_data(
            company_name,
            "{company} México empresa, {company} sitio web oficial"
        )
