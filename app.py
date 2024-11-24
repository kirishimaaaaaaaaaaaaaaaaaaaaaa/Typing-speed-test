from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# List of paragraphs
paragraphs = [
    """
    Programming is not just about solving problems but about thinking logically and building systems. In the age of technology, consistent practice can significantly improve typing skills. 
    The journey of a thousand miles begins with a single step, but persistence keeps you moving forward. The ability to stay focused and consistent over time is what differentiates masters from amateurs in any field.
    """,
    """
    The key to becoming an expert in any field lies in the ability to stay focused, dedicate time, and improve upon what you know consistently. Mastery requires continuous learning, 
    whether it's through formal education or self-guided study. Overcoming challenges and failures on the journey to success teaches valuable lessons that cannot be learned from success alone.
    """,
    """
    In today's world, technology plays an essential role in nearly every aspect of our lives. Whether it’s the devices we use, the way we communicate, or how we work, technology shapes our experiences.
    Being adaptable to new technological advancements is crucial for thriving in a modern society. By fostering curiosity and embracing change, individuals can leverage technology to improve productivity and create innovative solutions.
    """,
    """
    Time management is a crucial skill that can dramatically impact the quality and efficiency of one's work. It involves organizing tasks, setting goals, and prioritizing responsibilities in a way that maximizes productivity.
    Effective time management is not just about working harder, but about working smarter. By learning to allocate time properly and avoid distractions, people can achieve more and reduce stress levels.
    """
]

test_duration = 15  # Duration of the test in seconds

@app.route('/')
def home():
    # Serve the typing test HTML
    return render_template('index.html')


@app.route('/get_paragraph', methods=['GET'])
def get_paragraph():
    # Return a random paragraph for the typing test
    paragraph = random.choice(paragraphs)
    return jsonify({"paragraph": paragraph})


@app.route('/calculate_results', methods=['POST'])
def calculate_results():
    # Calculate typing test results
    data = request.json
    typed_text = data.get('typed_text', '')
    sample_text = data.get('sample_text', '')
    elapsed_time = float(data.get('elapsed_time', test_duration))

    # Split typed text and sample text into words
    typed_words = typed_text.split()
    sample_words = sample_text.split()

    # Calculate correct words typed
    correct_words = 0
    for i in range(min(len(typed_words), len(sample_words))):
        if typed_words[i].lower() == sample_words[i].lower():  # case-insensitive comparison
            correct_words += 1

    # Calculate WPM based on the typed words
    wpm = len(typed_words) * (60 / elapsed_time)  # Words per minute

    # Calculate accuracy based on correctly typed words
    accuracy = (correct_words / len(typed_words)) * 100 if typed_words else 0

    # Return results
    return jsonify({
        "wpm": round(wpm, 2),
        "accuracy": round(accuracy, 2),
        "typed_text": typed_text,
        "sample_text": sample_text
    })


if __name__ == '__main__':
    app.run(debug=True, port=5002)
