import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

def generate_explanation(transaction_data, risk_score, rules_triggered):
    """
    Generates a human-readable explanation for a fraudulent transaction using Gemini API.
    """
    if not API_KEY:
        return "Explanation unavailable (API Key missing)."

    try:
        # Construct prompt
        prompt = f"""
        Explain why this transaction is flagged as FRAUD.
        
        Transaction Data:
        - Amount: ${transaction_data.get('transaction_amount')}
        - Channel: {transaction_data.get('channel')}
        - Hour: '{transaction_data.get('hour')}:00'
        - Risk Score: {risk_score:.2f}
        - Triggered Rules: {', '.join(rules_triggered) if rules_triggered else 'None'}
        
        Provide a concise 1-sentence explanation for a compliance officer. Focus on the most suspicious factors.
        """
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        headers = {'Content-Type': 'application/json'}
        response = requests.post(URL, headers=headers, json=payload, timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            # Extract text
            try:
                explanation = result['candidates'][0]['content']['parts'][0]['text']
                return explanation.strip()
            except (KeyError, IndexError):
                return "Explanation generation failed (Invalid response format)."
        else:
            return f"Explanation generation failed (Status {response.status_code})."
            
    except Exception as e:
        return f"Explanation generation failed (Error: {str(e)})."
