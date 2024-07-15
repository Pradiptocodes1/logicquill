from flask import Flask, request, jsonify, render_template_string
from llama_index.llms.llama_api import LlamaAPI
from llama_index.core.llms import ChatMessage

app = Flask(__name__)

# Initialize the LlamaAPI with the given API key
llm = LlamaAPI(api_key="LL-2F3X6yxwbPb7AWSFSYnrIOMc6aE1fkTXm2DVgpdqT2O2iWf416UD7yq3kN2dWRuQ", temperature=0)

def process_input(input_text):
    messages = [
        ChatMessage(
            model="llama3-70b",
            role="system", 
            content='''
            Write the pseudocode where 
            Always capitalize the initial word (often one of the main six constructs).
            Make only one statement per line.
            Indent to show hierarchy, improve readability and show nested constructs.
            Always end multi-line sections using any of the END keywords (ENDIF, ENDWHILE, etc.).
            Keep your statements programming language independent.
            Use the naming domain of the problem, not that of the implementation. For instance: “Append the last name to the first name” instead of “name = first+last.”
            Keep it simple, concise and readable
          '''
          
            
        ),
        ChatMessage(role="user", content=input_text),
    ]
    resp = llm.chat(messages)
    print(resp)
    # Return the response object as a string
    return str(resp)  # Convert the response object to its string representation

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
            font-family: Courier New; /* Ensuring response text is in Calibri font */
            text-align" left;
            padding-right: 100px;
        }
        .textarea-wrapper {
            display: inline-block;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
        }
        .responsePane{
            display: flex;
            justify-content: center;
            border: 1px solid black;
            background-color: #f5f5f5; 
            box-shadow: 4px 4px 8px rgba(0, 0, 0, 0.1);
            border-radius: 5px;
            resize: none;
            width: 50%; 
            margin: 0 auto;
        }
        .button{
            background-color: #373A40;
            color: white;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s, transform 0.2s box-shadow 0.2s;
            padding: 10px 10px;
            border-radius: 5px;
            border: 1px solid black;
            &:hover {
                background-color: #686D76; 
            }
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            &:active {
                background-color: #DC5F00;
                transform: scale(0.95);
                box-shadow: none; 
            }
            
        }
        textarea {
            width: 300px;
            height: 150px;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
            resize: none;
        label {
            color: #006989;
            font-family: 'Archivo Black', sans-serif;
        }
        h1{
          text-align: left;
        }
        
    </style>
</head>
<body>
    <center><h1 style="font-family: 'Archivo Black', sans-serif; font-size: 40px; color: #373A40;">logicquill.</h1></center>
    <br><br>
    <center>
    <form id="llamaForm">
        <label for="inputText">Enter your Code/ Concept</label><br>
        <br>
         <div class="textarea-wrapper">
        <textarea id="inputText" name="inputText" cols="50" rows="7" required></textarea>
    </div><br><br>
        <button class="button" type="submit">Generate</button>
    </form>
    </center><br>
    <div class="responsePane">
    <p id="response">Results will be displayed here. Simply copy it. <br> <br>Also, It’s Impossible to Hum While Holding Your Nose </p>
    </div>
    <script>
        document.getElementById('llamaForm').addEventListener('submit', function(event) {
            event.preventDefault();
            const inputText = document.getElementById('inputText').value;
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
            })
            .catch(error => {
                console.error('Error:', error);
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
