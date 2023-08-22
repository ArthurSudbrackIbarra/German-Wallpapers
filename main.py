from ctypes import windll
from PIL import Image, ImageDraw, ImageFont
from googletrans import Translator
from transformers import pipeline
from textwrap import wrap
from datetime import datetime

# Constants, change them to your liking.
FONT = ImageFont.truetype("arial.ttf", 30)
FIRST_SENTENCE_COORDINATES = (1100, 120)
SECOND_SENTENCE_COORDINATES = (1100, 420)
DEFAULT_SENTENCE_COORDINATES = (1100, 720)

# Set the paths according to your system.
PROMPT_FILE = r"C:\Users\ibarrart\Desktop\german-wallpapers-prompt.txt"
SOURCE_IMAGE_PATH = r"C:\Users\ibarrart\PycharmProjects\GermanWallpapers\black.jpg"
RESULT_IMAGE_PATH = r"C:\Users\ibarrart\PycharmProjects\GermanWallpapers\result.jpg"


def main():
    # Read the prompt from a file, if it exists.
    prompt = ""
    try:
        with open(PROMPT_FILE, "r") as file:
            prompt = file.read()
    except FileNotFoundError:
        print("Prompt file not found. No prompt will be used.")

    # Generate a random sentence in english.
    model = pipeline("text-generation", model="gpt2")
    sentence_english = model(
        prompt,
        do_sample=True,
        max_length=40,
        top_k=50,
        temperature=0.9,
        num_return_sequences=1,
    )[0]["generated_text"]

    # Wrap the sentence to fit in the image.
    sentence_english = "\n".join(wrap(sentence_english, 40))

    # Translate the sentence to german.
    translator = Translator()
    sentence_german = translator.translate(sentence_english, dest="de", src="en").text

    # Wrap the sentence to fit in the image.
    sentence_german = "\n".join(wrap(sentence_german, 40))

    # Default sentence, always in the image.
    sentence_default = f"Last execution: {datetime.now().strftime('%H:%M:%S')}.\nThis is a random-generated sentence!"

    # Create an image with the sentences.
    image = Image.open(SOURCE_IMAGE_PATH)
    editable = ImageDraw.Draw(image)
    editable.text(FIRST_SENTENCE_COORDINATES, sentence_english, fill="white", font=FONT, align="center")
    editable.text(SECOND_SENTENCE_COORDINATES, sentence_german, fill="white", font=FONT, align="center")
    editable.text(DEFAULT_SENTENCE_COORDINATES, sentence_default, fill="red", font=FONT, align="center")
    image.save(RESULT_IMAGE_PATH)

    # Make the image the Windows wallpaper.
    windll.user32.SystemParametersInfoW(20, 0, RESULT_IMAGE_PATH, 0)


if __name__ == "__main__":
    main()
