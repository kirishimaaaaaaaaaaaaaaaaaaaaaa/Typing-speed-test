from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# List of pre-made sentences
sentences = [
    "Programming is not just about solving problems but about thinking logically and building systems.",
    "In the age of technology, consistent practice can significantly improve typing skills.",
    "The journey of a thousand miles begins with a single step, but persistence keeps you moving forward.",
    "The ability to stay focused and consistent over time is what differentiates masters from amateurs in any field.",
]

test_duration = 15  # Duration of the test in seconds


@app.route('/')
def home():
    # Serve the typing test HTML
    return render_template('index.html')


@app.route('/get_sentence', methods=['GET'])
def get_sentence():
    # Return a random sentence for the typing test
    sentence = random.choice(sentences)
    return jsonify({"sentence": sentence})


@app.route('/calculate_results', methods=['POST'])
def calculate_results():
    # Calculate typing test results
    data = request.json
    typed_text = data.get('typed_text', '')
    sample_text = data.get('sample_text', '')
    elapsed_time = float(data.get('elapsed_time', test_duration))

    # Calculate WPM and accuracy
    correct_chars = sum(1 for i, c in enumerate(typed_text) if i < len(sample_text) and c == sample_text[i])
    accuracy = (correct_chars / len(sample_text)) * 100 if sample_text else 0
    wpm = len(typed_text.split()) * (60 / elapsed_time)

    # Return results
    return jsonify({
        "wpm": round(wpm, 2),
        "accuracy": round(accuracy, 2),
        "typed_text": typed_text,
        "sample_text": sample_text
    })


if __name__ == '__main__':
    app.run(debug=True, port=5002)
