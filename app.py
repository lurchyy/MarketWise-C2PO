from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def process_inputs():
    try:
        # Get the inputs from the request
        string_input = request.form.get('string_input', '')
        number_input = request.form.get('number_input', '0')
        bool_input = request.form.get('bool_input', 'False')

        # Convert the inputs safely
        number_input = int(number_input) if number_input.isdigit() else 0
        bool_input = bool_input.lower() in ['true', '1']

        # Process the inputs
        processed_input = 'Prefix: ' + string_input

        # Store the processed input in a variable
        result = {
            'string_input': processed_input,
            'number_input': number_input,
            'bool_input': bool_input
        }

        return result
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run()