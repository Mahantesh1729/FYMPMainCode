from flask import Flask, request, make_response

app = Flask(__name__)

@app.route('/', methods=['POST'])
def home():
    response = make_response('Welcome to the home page!')
    return response

if __name__ == '__main__':
    app.run(debug=True)
