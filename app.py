from flask import Flask, render_template
import requests

app = Flask(__name__)


API = "Your API"
NASA_URL = f"https://api.nasa.gov/planetary/apod?api_key={API}"

@app.route("/")
def home():
    response = requests.get(NASA_URL)
    data = response.json()

    return render_template("index.html",
                           title=data.get("title", "NASA APOD"),
                           image_url=data.get("url"),
                           explanation=data.get("explanation", "No description available."))

if __name__ == "__main__":
    app.run(debug=True)
