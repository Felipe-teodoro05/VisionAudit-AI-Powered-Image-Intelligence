# VisionAudit: AI-Powered Image Intelligence

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Computer Vision](https://img.shields.io/badge/AI-Florence--2-purple)](https://huggingface.co/microsoft/Florence-2-large)
[![Requests](https://img.shields.io/badge/Lib-Requests-green)]()

## Business Problem (O Desafio)
Empresas de proteção de marca (Brand Protection) precisam monitorar milhões de páginas na web para identificar uso indevido de imagens, logotipos ou conteúdo fraudulento. Fazer isso manualmente é impossível.
- **O Objetivo:** Criar um *bot* autônomo capaz de navegar em URLs suspeitas, extrair evidências visuais (imagens), mesmo que ofuscadas em Base64, e utilizar Inteligência Artificial Generativa para descrever o conteúdo da imagem e categorizar a ameaça.

---

## Solution Architecture

O **VisionAudit** é um pipeline de ingestão e inferência que conecta scraping tradicional com LLMs multimodais.



### Data Flow
1.  **Smart Scraper:** O agente acessa a URL alvo e localiza *assets* visuais. O sistema detecta automaticamente se a imagem é um link externo ou um *blob* Base64 embutido no HTML.
2.  **Payload Construction:** A imagem é processada e codificada para o padrão OpenAI Vision API.
3.  **AI Inference (Florence-2):** Utilizamos o modelo `microsoft-florence-2-large` para gerar uma legenda detalhada (`<DETAILED_CAPTION>`) do conteúdo visual.
4.  **Action:** O resultado estruturado é enviado para o sistema central de decisão.

---

## Tech Stack & Key Concepts

* **Python (OOP):** Código estruturado em classes para modularidade e reuso.
* **BeautifulSoup4:** Parsing de DOM para extração de atributos ocultos.
* **Computer Vision API:** Integração com modelos de Vision-Language (VLM) via requisições REST.
* **Base64 Handling:** Decodificação e re-codificação de streams de imagem para transporte via JSON.

---

## Code Snippet (Core Logic)

```python
# Exemplo da lógica de detecção de formato de imagem
if img_src.startswith("data:image"):
    # Decodifica imagem embutida no HTML (Base64)
    image_data = base64.b64decode(img_src.split(",")[1])
else:
    # Download tradicional de CDN
    image_data = requests.get(img_src).content
