import tkinter as tk

class DisappearingTextApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Disappearing Text Writing App")
        self.root.geometry("800x600")


        self.text_area = tk.Text(root, wrap="word", font=("Arial", 14))
        self.text_area.pack(expand=True, fill="both")


        self.status_label = tk.Label(root, text="", font=("Arial", 15))
        self.status_label.pack(side="bottom", fill="x")


        self.time_limit = 5  # seconds
        self.remaining_time = self.time_limit
        self.timer_id = None


        self.text_area.bind("<Key>", self.reset_timer)

        
        self.update_timer()

    def update_timer(self):
        """Update countdown and clear text if time runs out."""
        self.status_label.config(text=f"Time remaining: {self.remaining_time}")
        if self.remaining_time <= 0:
            self.clear_text()
        else:
            self.remaining_time -= 1
        self.timer_id = self.root.after(1000, self.update_timer)

    def reset_timer(self, event=None):
        """Reset timer when user types."""
        self.remaining_time = self.time_limit

    def clear_text(self):
        """Clear the text when timer reaches 0 and reset countdown."""
        self.text_area.delete("1.0", tk.END)
        self.remaining_time = self.time_limit



if __name__ == "__main__":
    root = tk.Tk()
    app = DisappearingTextApp(root)
    root.mainloop()