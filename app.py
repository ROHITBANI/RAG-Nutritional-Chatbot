import json
import requests
import time

# Use an empty API key string. The canvas environment will handle the actual key.
API_KEY = "AIzaSyCXwUke-IOCoc_wa2rc0UT2L-wqWE_BANM"
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent"

def generate_response(prompt, history):
    """
    Generates a response from the Gemini API using RAG-like behavior via Google Search grounding.

    Args:
        prompt (str): The user's query.
        history (list): A list of previous messages in the conversation.

    Returns:
        str: The generated response from the chatbot, including sources.
    """
    try:
        # Construct the conversation history payload
        contents = history + [{"role": "user", "parts": [{"text": prompt}]}]
        
        # Define the system instruction for the chatbot's persona and rules
        system_instruction = {
            "parts": [{
                "text": "You are a friendly and professional nutritional expert named Nutri-Bot. Provide concise, clear, and easy-to-understand information based on reliable sources. If you are asked to provide medical advice, gently decline and recommend consulting a healthcare professional or a registered dietitian. You must cite your sources if Google Search is used."
            }]
        }

        payload = {
            "contents": contents,
            "tools": [{"google_search": {}}],  # Enable Google Search grounding for RAG
            "systemInstruction": system_instruction,
        }

        headers = {
            'Content-Type': 'application/json',
        }

        # Make the API call with exponential backoff
        max_retries = 3
        retry_delay = 1
        for i in range(max_retries):
            response = requests.post(f"{API_URL}?key={API_KEY}", headers=headers, data=json.dumps(payload))
            if response.status_code == 200:
                break
            elif response.status_code == 429: # Too many requests
                print(f"Rate limit exceeded. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2
            else:
                response.raise_for_status()
        
        response.raise_for_status() # Raise an exception for bad status codes

        result = response.json()
        candidate = result.get('candidates', [{}])[0]
        
        if not candidate:
            return "I'm sorry, I couldn't generate a response. Please try again."

        text = candidate.get('content', {}).get('parts', [{}])[0].get('text', '')
        
        # Extract grounding sources for citations
        sources = []
        grounding_metadata = candidate.get('groundingMetadata', {})
        if grounding_metadata and grounding_metadata.get('groundingAttributions'):
            for attribution in grounding_metadata['groundingAttributions']:
                web_uri = attribution.get('web', {}).get('uri')
                web_title = attribution.get('web', {}).get('title')
                if web_uri and web_title:
                    sources.append({'uri': web_uri, 'title': web_title})

        # Append citations to the response
        full_response = text
        if sources:
            full_response += "\n\nSources:"
            for source in sources:
                full_response += f"\n- [{source['title']}]({source['uri']})"
        
        return full_response

    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"
    except json.JSONDecodeError as e:
        return f"Failed to parse JSON response: {e}"

def main():
    print("Hello! I'm Nutri-Bot, your personal nutritional advisor.")
    print("I can provide information on a wide range of foods, diets, and health topics.")
    print("Type 'exit' or 'quit' to end the conversation.")
    print("-" * 50)
    
    chat_history = []
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ["exit", "quit"]:
            print("Nutri-Bot: Goodbye! Stay healthy.")
            break
        
        print("Nutri-Bot: Thinking...")
        response = generate_response(user_input, chat_history)
        print(f"Nutri-Bot: {response}")
        print("-" * 50)
        
        # Add the user's message and the bot's response to the history for context
        chat_history.append({"role": "user", "parts": [{"text": user_input}]})
        chat_history.append({"role": "model", "parts": [{"text": response}]})
        
if __name__ == "__main__":
    main()
