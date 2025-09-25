from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
import numpy as np
from collections import Counter
import os

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads"

def get_palette(image_path, top_colors=10):
    img = Image.open(image_path).convert("RGB")
    img = img.resize((150, 150))  # Reducir tamaño para hacerlo más rápido
    pixels = np.array(img).reshape(-1, 3)

    # Contar colores
    counts = Counter(map(tuple, pixels))
    most_common = counts.most_common(top_colors)

    # Convertir a HEX
    hex_colors = ['#%02x%02x%02x' % rgb for rgb, _ in most_common]
    return hex_colors

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "image" not in request.files:
            return redirect(request.url)

        file = request.files["image"]
        if file.filename == "":
            return redirect(request.url)

        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        colors = get_palette(filepath)

        return render_template("result.html", colors=colors, image=file.filename)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
