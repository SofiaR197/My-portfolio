import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont


class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Watermarking App")
        self.root.geometry("800x600")
        self.root.config(bg="#2c2c2c")

        self.image = None
        self.tk_image = None
        self.displayed_label = None

        tk.Button(root, text="Upload Image", command=self.upload_image, bg="#59AC77", fg="white").pack(pady=10)
        self.watermark_text = tk.Entry(root, width=40)
        self.watermark_text.pack(pady=5)
        self.watermark_text.insert(0, "Enter your watermark text")

        tk.Button(root, text="Add Watermark", command=self.add_watermark, bg="#124170", fg="white").pack(pady=10)
        tk.Button(root, text="Save Image", command=self.save_image, bg="#A376A2", fg="white").pack(pady=10)


    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.image = Image.open(file_path).convert("RGBA")
            self.show_image(self.image)

    def show_image(self, img):
        img_resized = img.copy()
        img_resized.thumbnail((600, 400))
        self.tk_image = ImageTk.PhotoImage(img_resized)

        if self.displayed_label:
            self.displayed_label.destroy()

        self.displayed_label = tk.Label(self.root, image=self.tk_image, bg="#2c2c2c")
        self.displayed_label.pack(pady=10)

    def add_watermark(self):
        if self.image is None:
            messagebox.showerror("Error", "Please upload an image first!")
            return

        text = self.watermark_text.get()
        if not text:
            messagebox.showerror("Error", "Please enter watermark text!")
            return

        watermarked = self.image.copy()
        drawable = ImageDraw.Draw(watermarked)

        font = ImageFont.truetype("arial.ttf", 65)

        width, height = watermarked.size
        bbox = drawable.textbbox((0,0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x = (width - text_width) // 2
        y = (height - text_height) // 2

        drawable.text((x, y), text, font=font, fill=(255, 255, 255, 180))

        self.image = watermarked
        self.show_image(watermarked)

    def save_image(self):
        if self.image is None:
            messagebox.showerror("Error", "No image to save!")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"),
            ("JPEG files", "*.jpg"),
            ("ALL files", "*.*")]
        )
        if file_path:
            self.image.save(file_path)
            messagebox.showinfo("Success", "Image saved successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop()



