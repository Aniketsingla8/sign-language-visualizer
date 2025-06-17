from flask import Flask, render_template, request, send_file
from PIL import Image
import os

app = Flask(__name__)

# Folder with your sign images (e.g., a.jpg, love.jpg, you.jpg)
SIGN_IMAGE_FOLDER = "sign_images"
OUTPUT_IMAGE_PATH = "static/output/combined.jpg"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        sentence = request.form["sentence"].lower()
        words = sentence.replace("?", "").replace("!", "").split()

        image_paths = []
        for word in words:
            img_path = os.path.join(SIGN_IMAGE_FOLDER, f"{word}.jpg")
            if os.path.exists(img_path):
                image_paths.append(img_path)
            else:
                # fallback to fingerspelling if word image doesn't exist
                for letter in word:
                    letter_img = os.path.join(SIGN_IMAGE_FOLDER, f"{letter}.jpg")
                    if os.path.exists(letter_img):
                        image_paths.append(letter_img)

        if image_paths:
            images = [Image.open(path) for path in image_paths]
            widths, heights = zip(*(i.size for i in images))
            total_width = sum(widths)
            max_height = max(heights)

            new_img = Image.new("RGB", (total_width, max_height), (255, 255, 255))
            x_offset = 0
            for img in images:
                new_img.paste(img, (x_offset, 0))
                x_offset += img.width

            os.makedirs(os.path.dirname(OUTPUT_IMAGE_PATH), exist_ok=True)
            new_img.save(OUTPUT_IMAGE_PATH)

            return render_template("index.html", image_generated=True, combined_image="combined.jpg")


    return render_template("index.html", image_generated=False)

if __name__ == "__main__":
    app.run(debug=True)
