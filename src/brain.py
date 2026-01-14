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
        # Usamos el modelo Flash por su baja latencia y costo
        prompt = f"""
        Actúa como un BDR Senior. Evalúa este prospecto frente al ICP: {icp_prompt}.
        PERFIL: {profile_text}
        Responde exclusivamente en JSON con: fit (bool), score (int), reason (str), name (str), role (str), company (str).
        """
        
        try:
            response = self.client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt,
                config={
                    'response_mime_type': 'application/json'
                }
            )
            return json.loads(response.text)
        except Exception as e:
            print(f"Error en el cerebro de Gemini: {e}")
            return None