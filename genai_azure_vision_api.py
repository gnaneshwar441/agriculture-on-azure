# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 12:48:01 2024

@author: Gnaneshwar
"""

import os
import requests
import base64

def genai_vision_api(image_path=""):
    print("image_path:",image_path)
    # Configuration
    GPT4V_KEY = #"YOUR_API_KEY"
    IMAGE_PATH = image_path #"YOUR_IMAGE_PATH"
    encoded_image = base64.b64encode(open(IMAGE_PATH, 'rb').read()).decode('ascii')
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
              "type": "image_url",
              "image_url": {
                "url": f"data:image/jpeg;base64,{encoded_image}"
              }
            },
            {
              "type": "text",
              "text": "Output must follow the below format."
            },
            {
              "type": "text",
              "text": "Name of crop: <name of the crop in image>"
            },
            {
              "type": "text",
              "text": "States grown in India:<search in which parts of India is the crop in image grown in bullet points>"
            },
            {
              "type": "text",
              "text": "Season of the Crop:<search in which season is this crop in image grown in India in bullet points>"
            },
            {
              "type": "text",
              "text": "Cultivation methods:<cultivation methods of the crop in image in bullet points>"
            },
            {
              "type": "text",
              "text": "Seeds:<name of seeds related to the crop in image in India only>"
            },
            {
              "type": "text",
              "text": "Fertilizers:<name of fertilizers related to the crop in image in India only>"
            },
            {
              "type": "text",
              "text": "Pesticides:<name of pesticides related to the crop in image in India only>"
            },
            {
              "type": "text",
              "text": "Profit:<search profit percentage of the crop in image in India depending on yield, market demand and input costs>"
            },
            {
              "type": "text",
              "text": "Cost per Acre:<output the cost of the crop in image per acre in India only>"
            }
          ]
        }
        # {
        #   "role": "assistant",
        #   "content": [
        #     {
        #       "type": "text",
        #       "text": "Name of crop: Rice\n\nStates grown in India:\n- West Bengal\n- Uttar Pradesh\n- Punjab\n- Andhra Pradesh\n- Bihar\n- Tamil Nadu\n- Odisha\n- Assam\n- Chhattisgarh\n- Haryana\n\nSeason of the Crop:\n- Kharif season (June to November)\n- Summer season (March to June in irrigated areas)\n\nCultivation methods:\n- Wet or lowland cultivation (majority)\n- Dry or upland cultivation\n- Deep water or floating rice cultivation\n\nSeeds:\n- IR64\n- Sambha Mahsuri (BPT 5204)\n- Swarna (MTU 7029)\n- Pusa Basmati 1121\n\nFertilizers:\n- Urea\n- Di-ammonium phosphate (DAP)\n- Muriate of potash (MOP)\n- Zinc sulphate\n- Green manure\n\nPesticides:\n- Pretilachlor\n- Butachlor\n- Tricyclazole\n- Isoprothiolane\n- Buprofezin\n\nProfit:\n- The profit percentage of rice in India can vary widely depending on the variety grown, yield, market demand, and input costs. Generally, the profit margin can range from 20% to 50%.\n\nCost per Acre:\n- On average, the cost of cultivating rice per acre in India can range from INR 25,000 to INR 50,000, depending on the state, cultivation practices, and the variety of rice grown."
        #     }
        #   ]
        # }
        
        
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
