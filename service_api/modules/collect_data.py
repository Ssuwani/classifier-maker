import os
import json


def remove_if_not_jpg():
    root_dir = "downloads"
    for (root, dirs, files) in os.walk(root_dir):
        for file in files:
            if not file.endswith("jpg"):
                os.remove(os.path.join(root, file))


def save_json_example_classifier(keywords):
    data = {str(i): label for i, label in enumerate(keywords.split(","))}
    with open("example_classifier/api/class_index.json", "w") as json_file:
        json.dump(data, json_file)


def download_data(keywords, amount):
    assert len(keywords.split(",")) == 2, f"Error keywords format: {keywords}"
    os.system(
        f"googleimagesdownload --keywords {keywords} --limit {amount} --format jpg"
    )

    remove_if_not_jpg()

    save_json_example_classifier(keywords)
