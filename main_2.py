from ctypes import windll
from PIL import Image, ImageDraw, ImageFont
from googletrans import Translator
from wonderwords import RandomWord

# Constants, change them to your liking.
NUMBER_OF_SENTENCES = 5
FONT = ImageFont.truetype("arial.ttf", 30)
SENTENCES_COORDINATES = (1100, 120)
COLOR_BLUE = (117, 163, 209)
COLOR_PINK = "pink"
COLOR_GRAY = (178, 175, 179)

# Set the paths according to your system.
SOURCE_IMAGE_PATH = r"C:\Users\ibarrart\PycharmProjects\GermanWallpapers\black.jpg"
RESULT_IMAGE_PATH = r"C:\Users\ibarrart\PycharmProjects\GermanWallpapers\result.jpg"


def main():
    # Generate a sentence with 'NUMBER_OF_SENTENCES' english nouns, adjectives and verbs.
    generator = RandomWord()
    english_sentences = ""
    for _ in range(NUMBER_OF_SENTENCES):
        noun = generator.word(include_parts_of_speech=["nouns"])
        adjective = generator.word(include_parts_of_speech=["adjectives"])
        verb = generator.word(include_parts_of_speech=["verbs"])
        if verb.endswith("s"):
            english_sentences += f"The {adjective} {noun} {verb}es.\n"
        else:
            english_sentences += f"The {adjective} {noun} {verb}s.\n"

    # Translate the sentence to german.
    translator = Translator()
    german_sentences = translator.translate(english_sentences, dest="de", src="en").text

    # Create an image with the sentences.
    image = Image.open(SOURCE_IMAGE_PATH)
    editable = ImageDraw.Draw(image)

    # Write the sentences in the image.
    # German sentences change color depending on the article.
    # Masculine -> blue, Feminine -> pink, Neutral -> gray.
    zipped = zip(english_sentences.split("\n"), german_sentences.split("\n"))
    index = 0
    for english_sentence, german_sentence in zipped:
        editable.text(
            (SENTENCES_COORDINATES[0], SENTENCES_COORDINATES[1] + index * 50),
            english_sentence,
            fill="white",
            font=FONT,
            align="center"
        )
        fill = "white"
        if str.lower(german_sentence).startswith("der"):
            fill = COLOR_BLUE
        elif str.lower(german_sentence).startswith("die"):
            fill = COLOR_PINK
        elif str.lower(german_sentence).startswith("das"):
            fill = COLOR_GRAY
        editable.text(
            (SENTENCES_COORDINATES[0], SENTENCES_COORDINATES[1] + (index + 1) * 50),
            german_sentence,
            fill=fill,
            font=FONT,
            align="center"
        )
        index += 3

    # Save the image.
    image.save(RESULT_IMAGE_PATH)

    # Make the image the Windows wallpaper.
    windll.user32.SystemParametersInfoW(20, 0, RESULT_IMAGE_PATH, 0)


if __name__ == "__main__":
    main()
