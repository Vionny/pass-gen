from algorithm.algo3 import read_dict_file
from flask import Flask, render_template, request, jsonify, Response
from logic import fill_password, generate_passwords  # import the functions you need

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    result = generate_passwords(data)
    return jsonify(result)




if __name__ == "__main__":
    app.run(debug=True, threaded=True, use_reloader=False)
