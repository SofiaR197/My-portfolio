import tkinter as tk
import time
import random


SAMPLE_TEXTS = [
    "The quick brown fox jumps over the lazy dog",
    "Typing fast is a skill that improves with practice",
    "Python is a versatile programming language for beginners",
    "Consistency is the key to becoming a fast typist",
    "Artificial intelligence is shaping the future of technology"
]


class TypingSpeedTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.geometry("800x500")
        self.root.config(bg="#f2f2f2")

        self.sample_text = random.choice(SAMPLE_TEXTS)
        self.start_time = None
        self.time_left = 60
        self.timer_running = False


        self.label_title = tk.Label(root, text="Typing Speed Test", font=("Arial", 20, "bold"), bg="#f2f2f2")
        self.label_title.pack(pady=10)

        self.label_instructions = tk.Label(root, text="Type the text below as fast and accurately as you can:",
                                           font=("Arial", 12), bg="#f2f2f2")
        self.label_instructions.pack(pady=5)

        self.text_display = tk.Label(root, text=self.sample_text, font=("Arial", 14), wraplength=700, bg="#A376A2",
                                     relief="solid", padx=10, pady=10)
        self.text_display.pack(pady=10)

        self.entry = tk.Text(root, height=5, width=80, font=("Arial", 12), state="disabled")
        self.entry.pack(pady=10)

        self.timer_label = tk.Label(root, text="Time: 60s", font=("Arial", 14, "bold"), bg="#CB0404", fg="white")
        self.timer_label.pack(pady=5)

        self.button_start = tk.Button(root, text="Start Test", command=self.start_test, font=("Arial", 12), bg="#BAD8B6",
                                      fg="white")
        self.button_start.pack(pady=5)

        self.result_label = tk.Label(root, text="", font=("Arial", 14, "bold"), bg="#f2f2f2")
        self.result_label.pack(pady=10)

    def start_test(self):
        self.entry.config(state="normal")
        self.entry.delete("1.0", tk.END)
        self.result_label.config(text="")
        self.sample_text = random.choice(SAMPLE_TEXTS)
        self.text_display.config(text=self.sample_text)

        self.start_time = time.time()
        self.time_left = 60
        self.timer_running = True
        self.update_timer()

    def update_timer(self):
        if self.time_left > 0 and self.timer_running:
            self.timer_label.config(text=f"Time: {self.time_left}s")
            self.time_left -= 1
            self.root.after(1000, self.update_timer)
        else:
            self.timer_running = False
            self.entry.config(state="disabled")
            self.check_speed()

    def check_speed(self):
        typed_text = self.entry.get("1.0", tk.END).strip()

        if not typed_text:
            self.result_label.config(text="You didn't type anything!", fg="red")
            return


        elapsed_time = time.time() - self.start_time
        elapsed_minutes = elapsed_time / 60
        word_count = len(typed_text.split())
        wpm = round(word_count / elapsed_minutes)


        correct_words = 0
        sample_words = self.sample_text.split()
        typed_words = typed_text.split()

        for i in range(min(len(sample_words), len(typed_words))):
            if sample_words[i] == typed_words[i]:
                correct_words += 1

        accuracy = round((correct_words / len(sample_words)) * 100)

        self.result_label.config(
            text=f"⏱ Test Finished!\nSpeed: {wpm} WPM | Accuracy: {accuracy}%",
            fg="black"
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedTest(root)
    root.mainloop()
