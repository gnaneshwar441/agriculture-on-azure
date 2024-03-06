# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 10:39:15 2024

@author: Gnaneshwar
"""

def genai_text_api(input_value=""):
    if input_value == "":
        return "Enter a crop name only"
    
    # import os
    import requests
    # import base64
    
    # Configuration
    GPT4V_KEY = # "YOUR_API_KEY"
    # IMAGE_PATH = "YOUR_IMAGE_PATH"
    # encoded_image = base64.b64encode(open(IMAGE_PATH, 'rb').read()).decode('ascii')
    headers = {
        "Content-Type": "application/json",
        "api-key": GPT4V_KEY,
    }
    
    # Payload for the request
    payload = {
      "messages": [
        {
          "role": "system",
          "content": [
            {
              "type": "text",
              "text": "You are an AI assistant that helps people find information."
            }
          ]
        },
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "How many Kg paddy seeds per acre?"
            }
          ]
        },
        {
          "role": "assistant",
          "content": [
            {
              "type": "text",
              "text": "For direct seeding, farmers may use around 60-80 kg of paddy seeds per acre. For transplanting method, the seed rate could be around 20-30 kg per acre since the seeds are first grown into seedlings before being transplanted to the field."
            }
          ]
        },
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": f"{input_value}"
            }
          ]
        }
      ],
      "temperature": 0.7,
      "top_p": 0.95,
      "max_tokens": 800
    }
    
    GPT4V_ENDPOINT = "https://oai-agriculture1.openai.azure.com/openai/deployments/gpt-4-vision/chat/completions?api-version=2024-02-15-preview"
    
    # Send request
    try:
        response = requests.post(GPT4V_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.RequestException as e:
        raise SystemExit(f"Failed to make the request. Error: {e}")
    
    # Handle the response as needed (e.g., print or process)
    print(response.json())
    return response.json()['choices'][0]['message']['content']
