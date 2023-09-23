import os
import random
from flask import Flask, request, render_template
import openai

app = Flask(__name__)

# Set your OpenAI API key here
openai.api_key = "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"

# Maintain conversation history
conversation_history = []

# Scripted responses
greetings = ["Hello!", "Hi there!", "Hey, how can I help you today?"]
empathy_responses = ["I understand how you feel.", "It must be tough for you.", "I'm here to listen."]
goodbye_responses = ["Goodbye!", "Take care!", "Feel free to come back anytime."]

def generate_response(user_message):
    # Generate a response from the AI model
    response = openai.Completion.create(
        engine="davinci",  # You can choose an appropriate engine
        prompt=user_message,
        max_tokens=50,
        temperature=0.7,  # Adjust this value for more variability
    )
    
    ai_response = response.choices[0].text
    
    # Apply NLP post-processing
    ai_response = post_process_response(ai_response)
    
    return ai_response

def post_process_response(response):
    # Add variability
    if random.random() < 0.3:
        response = random.choice(empathy_responses) + " " + response
    
    # Correct grammar and punctuation (you can use libraries like spaCy or NLTK)
    response = response.capitalize() + "." if not response.endswith((".", "!", "?")) else response
    
    return response

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_message = request.form["user_message"]
        conversation_history.append(f"User: {user_message}")
        
        # Generate a response from the AI model
        ai_response = generate_response(user_message)
        conversation_history.append(f"AI: {ai_response}")

    return render_template("index.html", conversation=conversation_history)

if __name__ == "__main__":
    app.run(debug=True)

if __name__ == "__main__":
    # Bind the Flask app to a specific IP address (e.g., '127.0.0.1') and port (e.g., 5000)
    app.run(debug=True, host='127.0.0.1', port=888)