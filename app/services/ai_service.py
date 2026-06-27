
import json
import anthropic
from app.config import get_settings

settings = get_settings()

class AIService:
    def __init__(self):
        # Inicializamos el cliente de Claude
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

    def evaluate_answer(self, question: str, user_answer: str, official_context: str, current_stress: int) -> dict:
        """
        Evalúa la respuesta del usuario usando Claude, ajustando el tono según el estrés.
        """
        
        # Definimos cómo debe comportarse Claude según la barra de estrés (Gamificación)
        if current_stress <= 3:
            tone_instruction = "You are friendly and encouraging. Use a calm tone."
        elif current_stress <= 7:
            tone_instruction = "You are neutral and professional, like a standard government clerk."
        else:
            tone_instruction = "You are strictly formal, serious, and slightly impatient. Speak quickly and to the point."

        # EL PROMPT MAESTRO (Sistema RAG simulado)
        system_prompt = f"""
        You are an AI simulating a USCIS Citizenship Interview Officer for an app called Civix.
        {tone_instruction}
        
        Your STRICT RULE: You must ONLY evaluate the user's answer based on the 'Official Context' provided below. 
        Do NOT use any outside historical knowledge. If the answer is not in the context, it is wrong. This guarantees 0% hallucinations.
        
        You must respond strictly in JSON format with exactly these 3 keys:
        - "is_correct": boolean
        - "explanation": string (If correct, say 'Correct'. If wrong, briefly explain the right answer using the Official Context).
        - "stress_adjustment": integer (-1, 0, or 1. Add 1 if the user is doing poorly or the answer is completely wrong, 0 if neutral, -1 if they are highly confident and correct).
        """

        user_prompt = f"""
        Question asked to the applicant: {question}
        
        Applicant's spoken answer: "{user_answer}"
        
        Official Context (The absolute truth): {official_context}
        
        Respond ONLY with the JSON.
        """

        # Llamada a la API de Claude
        response = self.client.messages.create(
            model="claude-sonnet-4-5", # El modelo más inteligente y rápido
            max_tokens=300,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )

        # Extraer el texto de la respuesta de Claude
        raw_response = response.content[0].text
        
        # Limpiar y parsear el JSON (Claude a veces envía bloques ```json ```)
        cleaned_response = raw_response.replace("```json", "").replace("```", "").strip()
        
        try:
            return json.loads(cleaned_response)
        except json.JSONDecodeError:
            # Fallback por si la red falla o Claude tiene un día raro
            return {
                "is_correct": False,
                "explanation": "System error evaluating response.",
                "stress_adjustment": 0
            }

# Instancia global del servicio
ai_service = AIService()