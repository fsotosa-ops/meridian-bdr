from google import genai
import os
import json
from dotenv import load_dotenv

load_dotenv()

class MeridianBrain:
    def __init__(self):
        # Cliente oficial unificado para 2026
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    def evaluate_candidate(self, profile_text, icp_prompt):
        prompt = f"""
        Actúa como un BDR Senior. Evalúa este prospecto frente al ICP: {icp_prompt}.
        PERFIL: {profile_text}
        Responde exclusivamente en JSON (un solo objeto, NO una lista) con: fit (bool), score (int), reason (str), name (str), role (str), company (str).
        """
        
        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
                config={
                    'response_mime_type': 'application/json'
                }
            )
            result = json.loads(response.text)
            
            # Si devuelve una lista, tomamos el primer elemento
            if isinstance(result, list):
                result = result[0] if result else None
                
            return result
        except Exception as e:
            print(f"Error en el cerebro de Gemini: {e}")
            return None
    
    def extract_profile_info(self, profile_text):
        """Extrae solo nombre, cargo y empresa (sin evaluar fit)"""
        prompt = f"""
        Extrae la información de este perfil de LinkedIn.
        PERFIL: {profile_text}
        Responde exclusivamente en JSON con: name (str), role (str), company (str).
        """
        
        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
                config={
                    'response_mime_type': 'application/json'
                }
            )
            result = json.loads(response.text)
            
            if isinstance(result, list):
                result = result[0] if result else None
                
            return result
        except Exception as e:
            print(f"Error extrayendo info: {e}")
            return None