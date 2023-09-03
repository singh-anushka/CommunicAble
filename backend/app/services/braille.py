from ..utils.ocr import getOcrText
import requests
import pdf2image
import io
import requests
from pybraille import convertText
from dotenv import load_dotenv
load_dotenv()

def testing():
    return {"message": "This is the Braille endpoint."}

def url_to_braille(url):
    text = url_to_text(url)
    return text, text_to_braille(text)

def text_to_braille(in_text):
    braille_text = convertText(in_text)
    return braille_text

def url_to_text(url):
    global i
    filename = "temporary.pdf"
    r = requests.get(url, allow_redirects=True, stream=True)
    with open(filename, 'wb') as f:
            for chunk in r.iter_content():
                f.write(chunk)

    images = pdf2image.convert_from_path(filename)
    print(len(images))

    all_text = ""
    new_page = ""
    for image in images:
        image_data = imageToArray(image)
        new_page += text_from_image(image_data) or ""

        all_text += new_page

    i = 0
    return all_text

def imageToArray(pil_image):
	image_byte_array = io.BytesIO()
	pil_image.save(image_byte_array, format='PNG')
	image_data = image_byte_array.getvalue()
	return image_data


def text_from_image(image_data: bytes):
	result = getOcrText(image_data)
	if result is not None and result['status'] == 'Succeeded':
		return showResultinFile(result)

def showResultinFile(result):
	lines = result['recognitionResult']['lines']
	texty = ""
	for i in range(len(lines)-1):
		words = lines[i]['words']
		s = ""
		for word in words:
			s += word['text'] + " "
		texty += s
	return texty
