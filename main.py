import os
import random
import pygame
import time
import keyboard
import sys

AUDIO_FOLDER = "audio"

# Optional: allow multiple acceptable answers
ACCEPTABLE_ANSWERS = {
    "mandarin": ["chinese", "mandarin"],
    "hindi": ["hindi", "urdu"],
    "korean": ["korean"],
    "japanese": ["japanese"],
    "spanish": ["spanish"],
    "french": ["french"],
    "german": ["german"],
    "arabic": ["arabic"],
    "russian": ["russian"],
    "portuguese": ["portuguese"],
    "italian": ["italian"],
    "dutch": ["dutch"],
    "greek": ["greek"],
    "turkish": ["turkish"],
    "hebrew": ["hebrew"],
    "bengali": ["bengali"],
    "vietnamese": ["vietnamese"]
}

def clear_input_buffer():
    try:
        # Windows
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    except ImportError:
        # Mac/Linux
        import termios
        termios.tcflush(sys.stdin, termios.TCIFLUSH)

def wait_for_key(valid_keys):
    while True:
        for key in valid_keys:
            if keyboard.is_pressed(key):
                clear_input_buffer()
                time.sleep(0.15)
                return key
        time.sleep(0.05)

def init_audio():
    pygame.mixer.init()

def get_audio_files():
    supported = (".wav", ".mp3")
    return [f for f in os.listdir(AUDIO_FOLDER) if f.endswith(supported)]

def extract_language(filename):
    return filename.split("_")[0].lower()

def play_audio_with_skip(filepath):
    pygame.mixer.music.load(filepath)
    pygame.mixer.music.play()

    print("▶ Playing audio... (press 's' to skip)")

    skipped = False

    while pygame.mixer.music.get_busy():
        if not skipped and keyboard.is_pressed("s"):
            pygame.mixer.music.stop()
            clear_input_buffer()
            time.sleep(.15)
            print("⏭ Skipped!\n")
            skipped = True
            break
        time.sleep(0.1)

def ask_ready(index, total):
    input(f"\n[{index}/{total}] Press ENTER when you're ready...")

def ask_replay(filepath):
    print("Replay audio? (y/n): ", end="", flush=True)

    while True:
        key = wait_for_key(["y", "n"])
        print(key)

        if key == "y":
            play_audio_with_skip(filepath)
            print("Replay audio? (y/n): ", end="", flush=True)
        else:
            break

def check_answer(user_guess, correct_language):
    user_guess = user_guess.lower()

    if correct_language in ACCEPTABLE_ANSWERS:
        return user_guess in ACCEPTABLE_ANSWERS[correct_language]

    return user_guess == correct_language

def main():
    init_audio()

    files = get_audio_files()

    if not files:
        print("No audio files found in /audio folder.")
        return

    random.shuffle(files)

    score = 0
    total = len(files)

    print("\n=== Language Recognition Trainer ===")
    print(f"Loaded {total} audio samples.\n")

    for i, file in enumerate(files, 1):
        correct_language = extract_language(file)
        filepath = os.path.join(AUDIO_FOLDER, file)

        ask_ready(i, total)

        play_audio_with_skip(filepath)

        ask_replay(filepath)

        start_time = time.time()
        guess = input("Your guess: ").strip()
        end_time = time.time()

        time_taken = round(end_time - start_time, 2)

        if check_answer(guess, correct_language):
            print(f"✅ Correct! ({time_taken}s)\n")
            score += 1
        else:
            print(f"❌ Wrong! Correct answer: {correct_language} ({time_taken}s)\n")

    print("=== SESSION COMPLETE ===")
    print(f"Final Score: {score}/{total}")
    print(f"Accuracy: {round((score/total)*100, 2)}%")

if __name__ == "__main__":
    main()
