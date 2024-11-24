import curses
import time
import random

# Test duration in seconds
test_duration = 15

# List of pre-made sentences
sentences = [
    "Programming is not just about solving problems but about thinking logically and building systems.",
    "In the age of technology, consistent practice can significantly improve typing skills.",
    "The journey of a thousand miles begins with a single step, but persistence keeps you moving forward.",
    "The ability to stay focused and consistent over time is what differentiates masters from amateurs in any field.",
]

def typing_test(stdscr):
    # Curses initialization
    curses.curs_set(0)  # Hide cursor
    stdscr.clear()

    # Select a random sentence
    sample_text = random.choice(sentences)
    stdscr.addstr(0, 0, "Typing Test")
    stdscr.addstr(2, 0, "Type the following sentence as quickly and accurately as possible:")
    stdscr.addstr(4, 0, f"\"{sample_text}\"")
    stdscr.addstr(6, 0, f"You have {test_duration} seconds. Press Enter to start...")

    stdscr.refresh()
    stdscr.getch()  # Wait for Enter

    # Initialize variables
    user_input = []
    start_time = time.time()
    last_timer_update = -1

    while True:
        elapsed_time = time.time() - start_time
        remaining_time = max(0, test_duration - int(elapsed_time))

        # Update timer display
        if remaining_time != last_timer_update:
            stdscr.addstr(8, 0, f"Time left: {remaining_time} seconds   ")
            last_timer_update = remaining_time

        # Handle user input
        stdscr.nodelay(True)  # Non-blocking input
        try:
            key = stdscr.getch()
            if key != -1:  # A key was pressed
                if key in (10, 13):  # Enter key
                    break
                elif key in (8, 127, curses.KEY_BACKSPACE):  # Backspace
                    if user_input:
                        user_input.pop()  # Remove the last character
                elif 32 <= key <= 126:  # Printable characters
                    user_input.append(chr(key))
        except:
            pass

        # Display user input
        typed_text = ''.join(user_input)
        stdscr.addstr(10, 0, " " * (len(sample_text) + 20))  # Clear the line
        stdscr.addstr(10, 0, f"Typing: {typed_text}")  # Display updated text
        stdscr.refresh()

        # Exit if time is up
        if remaining_time == 0:
            break

        time.sleep(0.05)

    # Calculate results
    elapsed_time = time.time() - start_time
    typed_text = ''.join(user_input)
    correct_chars = sum(1 for i, c in enumerate(typed_text) if i < len(sample_text) and c == sample_text[i])
    accuracy = (correct_chars / len(typed_text)) * 100 if typed_text else 0
    wpm = len(typed_text.split()) * (60 / elapsed_time)

    # Prepare results
    results = [
        "\nResults:",
        f"Words per minute (WPM): {wpm:.2f}",
        f"Accuracy: {accuracy:.2f}%",
        f"\nYour typed text: {typed_text}",
        f"\nOriginal text: {sample_text}",
    ]

    # Return results to display after exiting curses
    return results

# Main wrapper
try:
        # Run curses application and get results
    results = curses.wrapper(typing_test)
except KeyboardInterrupt:
        # Handle abrupt exit
    print("\nTyping test interrupted.")
    exit()

    # Print results after curses ends
print("\n".join(results))
