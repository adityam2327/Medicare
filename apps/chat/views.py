# apps/chat/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from .models import Conversation
import re

GEMINI_API_KEY = "AIzaSyC_Q0X-YIc30_ob27ryCNuQNMexu6MhhQ0"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

LEGAL_SYSTEM_PROMPT = """You are HealthAI, a professional healthcare assistant designed to provide comprehensive medical guidance and support. You excel at helping users find hospitals,check symptoms ,  book appointments, and access personalized health tips—all in one place. Your responses are quick, accurate, empathetic, and user-friendly, ensuring a seamless healthcare experience."""


def clean_markdown(text):
    """Removes markdown symbols to prevent rendering issues."""
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)  # Remove **bold**
    text = re.sub(r"\*(.*?)\*", r"\1", text)  # Remove *italic*
    text = re.sub(r"\n\s*\*", "\n- ", text)  # Convert bullet points (* → -)
    return text


def get_chatbot_response(user_input):
    try:
        # Prepare the request payload according to Gemini's format
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {"text": f"{LEGAL_SYSTEM_PROMPT}\n\nUser Question: {user_input}"}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 800
            }
        }
        
        # Make request to Gemini API
        response = requests.post(
            f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        # Print response for debugging
        print("API Response:", response.text)
        
        # Parse the response
        if response.status_code == 200:
            response_data = response.json()
            # Extract text from the response according to Gemini's structure
            if 'candidates' in response_data and response_data['candidates']:

                candidate = response_data['candidates'][0]
                if 'content' in candidate and 'parts' in candidate['content']:
                    bot_response = candidate['content']['parts'][0].get('text', '')
                    return clean_markdown(bot_response)  # Apply cleaning function
            return "I'm sorry, I couldn't find the information you requested."
        else:
            print(f"API Error: Status {response.status_code}")
            return f"I apologize, but there was an error processing your request. Status code: {response.status_code}"
            
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return "I apologize, but I'm having trouble processing your request. Please try again in a moment."

def chatbot(request):
    return render(request, 'chatbot.html')

@csrf_exempt
def chat(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_input = data.get('message', '')
            
            if not user_input.strip():
                return JsonResponse({
                    'response': 'Please enter a message.'
                })
            
            # Get chatbot response
            bot_response = get_chatbot_response(user_input)
            
            # Save conversation
            Conversation.objects.create(
                user_input=user_input,
                bot_response=bot_response
            )
            
            return JsonResponse({
                'response': bot_response
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'response': 'Invalid request format.'
            })
        except Exception as e:
            print(f"View Exception: {str(e)}")
            return JsonResponse({
                'response': 'An error occurred while processing your request.'
            })
            
    return JsonResponse({'response': 'Invalid request method'})