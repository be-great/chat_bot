import requests

def send_message(message):
    response = requests.post(
        'http://localhost:5005/webhooks/rest/webhook',
        json={"sender": "user", "message": message}
    )
    return response.json()

# Example usage
user_input = "Hello, how can you assist me today?"
response = send_message(user_input)
print("Chatbot:", response)
