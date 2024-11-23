from flask import Flask, render_template, request
import random
from time import time

app = Flask(__name__)

# Typing test paragraphs
test_paragraphs = [
    "Success is not achieved overnight. It is the result of consistent effort, unwavering dedication, and a refusal to give up in the face of adversity. Those who persevere through challenges, adapt to changes, and maintain focus on their goals are the ones who ultimately achieve greatness. It is not the absence of failure but the ability to rise each time we fall that defines true success.",
    "The rapid advancement of technology has transformed nearly every aspect of human life. From smartphones and artificial intelligence to renewable energy and space exploration, innovations are reshaping the way we communicate, work, and live. While these advancements bring convenience and opportunities, they also raise ethical questions about privacy, security, and the potential consequences of automation on the workforce.",
    "The beauty of nature lies in its diversity and intricacy. Towering mountains, vast oceans, and dense forests remind us of the Earth's grandeur. Every leaf, every ripple, and every bird's song is a testament to the intricate balance that sustains life. It is our responsibility to protect this fragile ecosystem, ensuring that future generations can marvel at the wonders of the natural world.",
    "Education is the cornerstone of personal growth and societal progress. It empowers individuals to think critically, solve problems, and contribute meaningfully to their communities. A well-rounded education not only imparts knowledge but also fosters creativity, empathy, and a lifelong love for learning. In a rapidly changing world, the ability to learn, unlearn, and relearn is more important than ever.",
    "Time is the most valuable resource we have, yet it is often taken for granted. Effective time management requires setting priorities, avoiding distractions, and maintaining a clear focus on goals. By planning our days wisely and making conscious choices about how we spend our time, we can achieve a balance between work, leisure, and personal growth. Remember, time wasted cannot be regained."
]

# Helper functions
def calculate_errors(reference_text, user_input):
    errors_count = 0
    for char_index in range(len(reference_text)):
        try:
            if reference_text[char_index] != user_input[char_index]:
                errors_count += 1
        except IndexError:
            errors_count += 1
    return errors_count

def calculate_typing_speed(start_time, end_time, typed_text):
    time_elapsed = end_time - start_time
    if time_elapsed == 0:  # Prevent division by zero
        return 0
    typing_speed = len(typed_text) / time_elapsed  # Characters per second
    return round(typing_speed, 2)

# Routes
@app.route("/")
def index():
    # Randomly select a paragraph
    paragraph = random.choice(test_paragraphs)
    return render_template("index.html", paragraph=paragraph, start_time=time())

@app.route("/result", methods=["POST"])
def result():
    reference_text = request.form["reference_text"]
    typed_text = request.form["typed_text"]
    start_time = float(request.form["start_time"])
    end_time = time()

    # Calculate results
    errors = calculate_errors(reference_text, typed_text)
    typing_speed = calculate_typing_speed(start_time, end_time, typed_text)

    return render_template("result.html", errors=errors, typing_speed=typing_speed)

if __name__ == "__main__":
    app.run(debug=True)
