from flask import Flask, request, jsonify, render_template_string
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

app = Flask(__name__)

# Initialize the MistralClient with the given API key
mistral_client = MistralClient(api_key="azyEN3ZYjcvg964D8U99slt0JzY5jG4F")

def process_input(input_text):
    messages = [
        ChatMessage(
            role="system", 
            content='''
            Write the pseudocode where 
            Always capitalize the initial word (often one of the main six constructs).
            Make only one statement per line.
            Indent to show hierarchy, improve readability and show nested constructs.
            Always end multi-line sections using any of the END keywords (ENDIF, ENDWHILE, etc.).
            Keep your statements programming language independent.
            Use the naming domain of the problem, not that of the implementation. For instance: "Append the last name to the first name" instead of "name = first+last."
            Keep it simple, concise and readable
            properly describe and use appropriate symbols if neccessary for sets, lists unions arrows etc. 
            '''
        ),
        ChatMessage(role="user", content=input_text),
    ]
    chat_response = mistral_client.chat(
        model="mistral-small",
        messages=messages,
    )
    return chat_response.choices[0].message.content

@app.route('/')
def index():
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>logicquill</title>
    <link href='https://fonts.googleapis.com/css?family=Archivo+Black' rel='stylesheet'>
    <style>
        body {
            background-color: #EEEEEE;
            font-family: Courier New;
        }
        #response {
            font-family: Courier New;
            text-align: left;
            padding-right: 100px;
        }
        .textarea-wrapper {
            display: inline-block;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
        }
        .responsePane{
            display: flex;
            justify-content: center;
            resize: none;
            width: auto; 
            margin: 0 auto;
        }
        .button{
            background-color: #373A40;
            color: white;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s, transform 0.2s, box-shadow 0.2s;
            padding: 10px 10px;
            border-radius: 5px;
            border: 1px solid black;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .button:hover {
            background-color: #686D76; 
        }
        .button:active {
            background-color: #DC5F00;
            transform: scale(0.95);
            box-shadow: none; 
        }
        textarea {
            width: 300px;
            height: 150px;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
            resize: none;
        }
        label {
            color: #006989;
            font-family: 'Archivo Black', sans-serif;
        }
        h1{
          text-align: center;
        }
        .loader {
          width: 50px;
          aspect-ratio: 1;
          border-radius: 50%;
          border: 8px solid;
          border-color: #000 #0000;
          animation: l1 1s infinite;
          display: none;
        }
        @keyframes l1 {to{transform: rotate(.5turn)}}
    </style>
</head>
<body>
    <h1 style="font-family: 'Archivo Black', sans-serif; font-size: 40px; color: #373A40;">logicquill.</h1>
    <br><br>
    <center>
    <form id="mistralForm">
        <label for="inputText">Enter your Code/ Concept</label><br>
        <br>
         <div class="textarea-wrapper">
        <textarea id="inputText" name="inputText" cols="50" rows="7" required></textarea>
    </div><br><br>
        <button class="button" type="submit">Generate</button>
    </form>
    <div class="loader"></div>
    </center><br>
    <div class="responsePane">
    <p id="response">Results will be displayed here. Simply copy it. <br> <br>Also, It's Impossible to Hum While Holding Your Nose </p>
    </div>
    <script>
        document.getElementById('mistralForm').addEventListener('submit', function(event) {
            event.preventDefault();
            const inputText = document.getElementById('inputText').value;
            const loader = document.querySelector('.loader');
            const generateButton = document.querySelector('.button');
            const responsePane = document.querySelector('.responsePane');

            // Show loader and hide generate button
            loader.style.display = 'inline-block';
            generateButton.style.display = 'none';
            responsePane.style.display = 'none';

            fetch('/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ input_text: inputText })
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('response').innerText = data.response;
                // Hide loader and show generate button
                loader.style.display = 'none';
                generateButton.style.display = 'inline-block';
                responsePane.style.display = 'flex';
            })
            .catch(error => {
                console.error('Error:', error);
                // Hide loader and show generate button in case of error
                loader.style.display = 'none';
                generateButton.style.display = 'inline-block';
                responsePane.style.display = 'flex';
            });
        });
    </script>
</body>
</html>
    ''')

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    input_text = data.get('input_text')
    if not input_text:
        return jsonify({'error': 'No input_text provided'}), 400

    response_text = process_input(input_text)
    return jsonify({'response': response_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)