from flask import Flask, request, jsonify, render_template_string
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

app = Flask(__name__)

# Initialize the MistralClient with the given API key
mistral_client = MistralClient(api_key="YhQawUzc9ymDAjC1cjXJqBpaIXz4jjPu")

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
            Express each statement or action on its own line. 
            • Include programming constructs that are common in most (imperative) programming languages whenever applicable (for, while, repeat/until, switch/case, return, if/then/else, etc.). 
            • Use indentation of the inner parts of loops, if statements, and methods/function bodies (this is preferred over begin/end for conciseness). 
            • Let keywords and commands stand out clearly (e.g. using bold face). • Use comments, indicated using a clear symbol and layout (e.g. ‘//‘ and position to the right of the code). 
            • For assignments (e.g., of 42 to x) you may use either x ← 42 or x := 42. These are preferred over x = 42, because this can then be reserved for the logical statement of whether x is equal to 42.
            • Refrain from using language-specific constructs such as using a dot for a method call to an object (as in this.example()).
            • When methods are using parameters, assume they are passed on by value (i.e., a copy is assumed to be made).
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
        .button-container {
            display: flex;
            justify-content: center;
            gap: 10px;
        }
        
        .back-button {
            background-color: #686D76;
            color: white;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s, transform 0.2s, box-shadow 0.2s;
            padding: 10px 10px;
            border-radius: 5px;
            border: 1px solid black;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .back-button:hover {
            background-color: #373A40;
        }
        
        .back-button:active {
            background-color: #DC5F00;
            transform: scale(0.95);
            box-shadow: none;
        }
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
        <div class="button-container">
            <button class="button" type="submit">Generate</button>
            <a href="https://www.citewise.tech/toolkitspage.html"><button class="back-button" type="button" id="backButton">Back</button></a>
        </div>
    </form>
    <div class="loader"></div>
    </center><br>
    <center>
    <div class="responsePane">
    <p id="response">Results will be displayed here. Simply copy it. <br> <br>Also, It's Impossible to Hum While Holding Your Nose </p>
    </div>
    </center>
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
