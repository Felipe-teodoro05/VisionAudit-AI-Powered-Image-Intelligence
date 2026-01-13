import os
import base64
import requests
import json
from bs4 import BeautifulSoup
from typing import Dict, Any, Optional

# Simulação de variáveis de ambiente 
API_TOKEN = os.getenv("VISION_API_TOKEN", "INSERT_YOUR_TOKEN_HERE")
BASE_URL = "https://intern.aiaxuropenings.com"

class VisionScraper:
    def __init__(self, target_url: str):
        self.target_url = target_url
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {API_TOKEN}'
        }

    def fetch_image_from_url(self) -> bytes:
        """Faz o scrape da página e baixa a imagem (Base64 ou Binário)."""
        print(f"[*] Scraping target: {self.target_url}")
        response = requests.get(self.target_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        img_tag = soup.find("img")
        
        if not img_tag or not img_tag.get("src"):
            raise ValueError("Nenhuma imagem encontrada na tag <img>.")

        img_src = img_tag["src"]
        
        # Tratamento para Base64 vs URL Direta
        if img_src.startswith("data:image"):
            print("[*] Imagem detectada como Base64.")
            return base64.b64decode(img_src.split(",")[1])
        else:
            print("[*] Imagem detectada como URL externa.")
            return requests.get(img_src).content

    def analyze_image(self, image_bytes: bytes) -> Dict[str, Any]:
        """Envia imagem para inferência no modelo Florence-2."""
        print("[*] Enviando para análise de IA (Florence-2)...")
        
        img_base64 = base64.b64encode(image_bytes).decode('utf-8')
        payload = {
            "model": "microsoft-florence-2-large",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "<DETAILED_CAPTION>"},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}}
                    ]
                }
            ]
        }

        url = f"{BASE_URL}/v1/chat/completions"
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()

    def submit_results(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """Submete o resultado final."""
        print("[*] Submetendo resultados...")
        url = f"{BASE_URL}/api/submit-response"
        response = requests.post(url, headers=self.headers, json=analysis_result)
        response.raise_for_status()
        return response.json()

if __name__ == "__main__":
    # Exemplo de uso
    TARGET = "https://intern.aiaxuropenings.com/scrape/3d1b1b53-3a03-4a38-bffa-faf2bedcd72c"
    
    try:
        app = VisionScraper(TARGET)
        
        # 1. Get Image
        img_data = app.fetch_image_from_url()
        
        # 2. Analyze
        ai_response = app.analyze_image(img_data)
        print(f"[+] Análise completa: {json.dumps(ai_response, indent=2)}")
        
        # 3. Submit
        final_result = app.submit_results(ai_response)
        print(f"[+] Processo finalizado: {final_result}")
        
    except Exception as e:
        print(f"[!] Erro crítico: {e}")