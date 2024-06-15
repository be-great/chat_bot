from flask import Flask, request, render_template_string
import requests
import json

app = Flask(__name__)

# HTML template for the form
form_template = '''
<!doctype html>
<html lang="en">
  <head>
    <title>Add Training Data</title>
  </head>
  <body>
    <h1>Add Training Data to Rasa Model</h1>
    <form action="/add_data" method="post">
      <label for="question">Question:</label><br>
      <input type="text" id="question" name="question"><br>
      <label for="intent">Intent:</label><br>
      <input type="text" id="intent" name="intent"><br>
      <label for="answers">Answers (comma-separated):</label><br>
      <input type="text" id="answers" name="answers"><br><br>
      <input type="submit" value="Submit">
    </form>
  </body>
</html>
'''

@app.route('/')
def form():
    return render_template_string(form_template)

@app.route('/add_data', methods=['POST'])
def add_data():
    question = request.form['question']
    intent = request.form['intent']
    answers = request.form['answers'].split(',')

    # Update training data
    nlu_entry = {
        "intent": intent,
        "examples": [
            f"- {question}"
        ]
    }

    responses_entry = {
        intent: [
            {"text": answer.strip()} for answer in answers
        ]
    }

    # Send the updated data to Rasa server
    update_nlu(nlu_entry)
    update_responses(responses_entry)

    # Train the model
    train_model()

    return f"Data added and model retrained."

def update_nlu(nlu_entry):
    # Load existing NLU data
    with open('data/nlu.yml', 'r') as file:
        nlu_data = file.read()

    # Add new entry to NLU data
    nlu_data += f"\n- intent: {nlu_entry['intent']}\n  examples: |\n"
    for example in nlu_entry['examples']:
        nlu_data += f"    {example}\n"

    # Save updated NLU data
    with open('data/nlu.yml', 'w') as file:
        file.write(nlu_data)

def update_responses(responses_entry):
    # Load existing domain data
    with open('domain.yml', 'r') as file:
        domain_data = file.read()

    # Add new responses to domain data
    for intent, responses in responses_entry.items():
        domain_data += f"\n  utter_{intent}:\n"
        for response in responses:
            domain_data += f"  - text: \"{response['text']}\"\n"

    # Save updated domain data
    with open('domain.yml', 'w') as file:
        file.write(domain_data)

def train_model():
    url = "http://localhost:5005/model/train"
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers)
    return response.json()

if __name__ == '__main__':
    app.run(debug=True)
