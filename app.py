
from flask import Flask, jsonify, request, render_template_string
from retrieval import search_policy

app = Flask(__name__)


# Step 1: Generate an answer from the retrieved policy
def generate_answer(policy):
    if policy is None:
        return (
            "Sorry, I couldn't find a relevant policy "
            "in the available documents. Please try asking "
            "about attendance, examinations, or leave."
        )

    text = policy["text"]
    source = policy["source"]

    return (
        "Based on the available college policy:\n\n"
        + text
        + "\n\nPlease refer to the source document: "
        + source
    )


# Step 2: HTML page and styling
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>CampusPolicy AI</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f2f4f8;
            color: #263247;
            margin: 0;
        }

        header {
            background: #263b5b;
            color: white;
            padding: 24px;
            text-align: center;
        }

        header p {
            color: #dce5f2;
        }

        main {
            max-width: 700px;
            margin: 35px auto;
            padding: 16px;
        }

        .card {
            background: white;
            padding: 24px;
            border-radius: 12px;
            margin-bottom: 18px;
            box-shadow: 0 3px 12px #00000010;
        }

        form {
            display: flex;
            gap: 10px;
        }

        input {
            flex: 1;
            min-width: 0;
            padding: 13px;
            border: 1px solid #ccd2dc;
            border-radius: 7px;
            font-size: 15px;
        }

        button {
            padding: 12px 20px;
            background: #263b5b;
            color: white;
            border: none;
            border-radius: 7px;
            cursor: pointer;
        }

        button:hover {
            background: #38547c;
        }

        .answer {
            line-height: 1.7;
            white-space: pre-wrap;
            overflow-wrap: anywhere;
        }

        .source {
            color: #496b54;
            margin-top: 16px;
            font-size: 14px;
        }

        .examples {
            color: #647084;
            line-height: 1.8;
        }

        .score {
            color: #647084;
            font-size: 12px;
        }

        @media (max-width: 500px) {
            form {
                flex-direction: column;
            }

            main {
                margin: 15px auto;
            }
        }
    </style>
</head>

<body>
    <header>
        <h1>CampusPolicy AI</h1>
        <p>College Regulations and Academic Policy Chatbot</p>
    </header>

    <main>
        <div class="card">
            <h2>Ask a Policy Question</h2>

            <form method="POST" action="/">
                <input
                    type="text"
                    name="question"
                    placeholder="Ask about attendance, exams or leave..."
                    value="{{ question }}"
                    required
                >
                <button type="submit">Ask</button>
            </form>

            <p class="examples">
                Try asking:
                <br>• What is the attendance requirement?
                <br>• Can I carry a mobile phone into the exam hall?
                <br>• What should I do if I am absent due to illness?
            </p>
        </div>

        {% if answer %}
        <div class="card">
            <h2>Policy Answer</h2>

            <div class="answer">{{ answer }}</div>

            {% if policy_source %}
            <div class="source">
                Source: {{ policy_source }}
                <br>
                Policy ID: {{ policy_id }}
            </div>
            {% endif %}

            {% if score is not none %}
            <p class="score">
                Retrieval similarity:
                {{ "%.3f"|format(score) }}
            </p>
            {% endif %}
        </div>
        {% endif %}
    </main>
</body>
</html>
"""


# Step 3: Home page and policy question handling
@app.route("/", methods=["GET", "POST"])
def home():
    question = ""
    answer = ""
    source = ""
    policy_id = ""
    score = None

    if request.method == "POST":
        question = request.form.get("question", "").strip()

        if question:
            # Retrieve the most relevant policy
            result, score = search_policy(question)

            if result is None:
                answer = generate_answer(None)
                score = None

            else:
                # Generate a response using retrieved policy text
                answer = generate_answer(result)

                source = result["source"]
                policy_id = result["chunk_id"]

    return render_template_string(
        HTML_PAGE,
        question=question,
        answer=answer,
        policy_source=source,
        policy_id=policy_id,
        score=score
    )


# Step 4: Health-check endpoint
@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "application": "College Policy Chatbot"
    })


# Step 5: Start Flask application
if __name__ == "__main__":
    app.run(debug=True)
