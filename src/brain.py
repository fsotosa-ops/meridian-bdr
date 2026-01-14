"""
Cerebro de Meridian - Evaluación de leads con Gemini
"""

import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()


class MeridianBrain:
    
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            raise ValueError("❌ GEMINI_API_KEY no encontrada en .env")
        
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.0-flash"  # Rápido y barato
    
    def extract_profile_info(self, profile_text):
        """
        Extrae información estructurada de un perfil raw de LinkedIn.
        
        Args:
            profile_text: Texto crudo extraído del perfil
        
        Returns:
            Dict con name, role, company
        """
        
        prompt = f"""
Extrae la información de este perfil de LinkedIn Sales Navigator.
Responde SOLO en JSON válido, sin texto adicional.

PERFIL:
{profile_text}

Formato de respuesta (JSON):
{{"name": "Nombre Completo", "role": "Cargo", "company": "Empresa"}}

Si no encuentras algún campo, usa null.
"""
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config={
                    'response_mime_type': 'application/json'
                }
            )
            
            result = json.loads(response.text)
            
            # Manejar si devuelve lista
            if isinstance(result, list):
                result = result[0] if result else None
            
            return result
            
        except json.JSONDecodeError as e:
            print(f"      ⚠️ Error parseando JSON: {e}")
            return None
        except Exception as e:
            print(f"      ❌ Error en extracción: {e}")
            return None
    
    def evaluate_candidate(self, profile_with_research, icp_criteria):
        """
        Evalúa si un candidato cumple con el ICP.
        
        Args:
            profile_with_research: Perfil + información de investigación
            icp_criteria: Criterios del ICP definidos por el BDR
        
        Returns:
            Dict con fit, score, reason
        """
        
        prompt = f"""
Eres un BDR Senior experto en calificación de leads B2B.

CRITERIOS DEL ICP (Ideal Customer Profile):
{icp_criteria}

INFORMACIÓN DEL PROSPECTO:
{profile_with_research}

INSTRUCCIONES:
1. Analiza si el prospecto cumple con los criterios del ICP
2. Presta especial atención a:
   - Si la empresa es importadora
   - Volumen de importaciones (si hay datos)
   - Industria/productos que maneja
   - Cargo del contacto (¿es decisor de compras?)

3. Asigna un SCORE de 0-100:
   - 80-100: Match excelente, contactar prioritario
   - 60-79: Buen match, vale la pena explorar
   - 40-59: Match parcial, evaluar con cuidado
   - 0-39: No cumple criterios principales

Responde SOLO en JSON válido:
{{"fit": true/false, "score": 0-100, "reason": "Explicación breve de la evaluación"}}
"""
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config={
                    'response_mime_type': 'application/json'
                }
            )
            
            result = json.loads(response.text)
            
            # Manejar si devuelve lista
            if isinstance(result, list):
                result = result[0] if result else None
            
            # Validar campos requeridos
            if result:
                result['fit'] = bool(result.get('fit', False))
                result['score'] = int(result.get('score', 0))
                result['reason'] = str(result.get('reason', ''))[:300]
            
            return result
            
        except json.JSONDecodeError as e:
            print(f"      ⚠️ Error parseando JSON: {e}")
            return {"fit": False, "score": 0, "reason": "Error en evaluación"}
        except Exception as e:
            print(f"      ❌ Error en evaluación: {e}")
            return None
