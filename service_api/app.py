from flask import Flask, request, send_file, send_from_directory
from flask_cors import CORS
from modules import collect_data, trainer, utils
import os
import shutil

app = Flask(__name__)
CORS(app)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/result", methods=["GET"])
def give():
    file_path = f"./result/result.png"
    return send_file(file_path)


@app.route("/download_model")
def download_model():
    utils.makezip("example_classifier")
    return send_from_directory(directory=".", path="react_classifier.zip")


@app.route("/run", methods=["POST"])
def run():
    post_data = request.get_json()
    keywords = post_data["classes"]
    image_count = post_data["imageCount"]
    print(keywords, image_count)
    # Collect Data
    collect_data.download_data(keywords, amount=image_count)

    # Training
    trainer.train(epochs=10)

    # Clear Images
    shutil.rmtree("downloads")

    return {"success": True}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
