
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return """
    <h1>College Regulations Chatbot</h1>
    <p>Project setup successful.</p>
    <p>Data Engineering module is ready for integration.</p>
    """


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "application": "College Policy Chatbot"
    })


if __name__ == "__main__":
    app.run(debug=True)
