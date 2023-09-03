import os
import requests
import pdf2image
import PyPDF2
import wave
import time
import cv2
import io
import requests
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from xml.etree import ElementTree

from dotenv import load_dotenv
load_dotenv()

from ..utils.ocr import getOcrText
from ..utils.constants import ttsTokenURL, ttsURL, ttsVoiceListURL


all_audio = []
i = 0


def testing():
    return {"message": "This is the Book endpoint."}


def narrateBook(url, sound = False):
	global i
	filename = "temporary.pdf"
	r = requests.get(url, allow_redirects=True, stream=True)
	with open(filename, 'wb') as f:
		for chunk in r.iter_content():
			f.write(chunk)

	images = pdf2image.convert_from_path(filename)
	print(len(images))

	all_text = ""
	new_page = "Chapter 1 \n"
	for image in images:
		image_data = imageToArray(image)
		new_page += text_from_image(image_data) or ""

		all_text += new_page
		if sound:
			i += 1
			app = TextToSpeech(new_page, os.getenv('SpeechKey') or "")
			app.get_token()
			app.save_audio()

	i = 0
	if sound:
		return slow_down_audio(combine_all_audio(), 0.95)
	return all_text


def imageToArray(pil_image):
	image_byte_array = io.BytesIO()
	pil_image.save(image_byte_array, format='PNG')
	image_data = image_byte_array.getvalue()
	return image_data


class TextToSpeech(object):
	def __init__(self, to_be_spoken, subscription_key):
		self.subscription_key = subscription_key
		self.tts = to_be_spoken
		self.timestr = time.strftime("%Y%m%d-%H%M")
		self.access_token = None

	def get_token(self):
		response = requests.post(ttsTokenURL, headers={'Ocp-Apim-Subscription-Key': self.subscription_key})
		self.access_token = str(response.text)

	def save_audio(self):
		global i
		headers = {
			'Authorization': 'Bearer ' + (self.access_token or ''),
			'Content-Type': 'application/ssml+xml',
			'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
			'User-Agent': 'YOUR_RESOURCE_NAME'
		}
		xml_body = ElementTree.Element('speak', version='1.0')
		xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-us')
		voice = ElementTree.SubElement(xml_body, 'voice')
		voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
		voice.set('name', 'en-IN-NeerjaNeural') # Short name for 'Microsoft Server Speech Text to Speech Voice (en-US, Guy24KRUS)'
		voice.text = self.tts
		body = ElementTree.tostring(xml_body)
		response = requests.post(ttsURL, headers=headers, data=body)
		if response.status_code == 200:
			with open('sample-' + str(i) + '.wav', 'wb') as audio:
				audio.write(response.content)
				all_audio.append('sample-' + str(i) + '.wav')
				print("\nStatus code: " + str(response.status_code) + "\nYour TTS is ready for playback.\n" + 'sample-' + str(i) + '.wav')
		else:
			print("\nStatus code: " + str(response.status_code) + "\nSomething went wrong. Check your subscription key and headers.\n")
			print("Reason: " + str(response.reason) + "\n")

	def get_voices_list(self):
		headers = {}
		headers['Ocp-Apim-Subscription-Key'] = os.getenv('CVKey') or ""
		response = requests.get(ttsVoiceListURL, headers=headers)
		if response.status_code == 200:
			print("\nAvailable voices: \n" + response.text)
		else:
			print("\nStatus code: " + str(response.status_code) + "\nSomething went wrong. Check your subscription key and headers.\n")


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


def showResultOnImage( result, img ):
	img = img[:, :, (2, 1, 0)]
	fig, ax = plt.subplots(figsize=(12, 12))
	ax.imshow(img, aspect='equal')

	lines = result['recognitionResult']['lines']

	for i in range(len(lines)):
		words = lines[i]['words']
		for j in range(len(words)):
			tl = (words[j]['boundingBox'][0], words[j]['boundingBox'][1])
			tr = (words[j]['boundingBox'][2], words[j]['boundingBox'][3])
			br = (words[j]['boundingBox'][4], words[j]['boundingBox'][5])
			bl = (words[j]['boundingBox'][6], words[j]['boundingBox'][7])
			text = words[j]['text']
			x = [tl[0], tr[0], tr[0], br[0], br[0], bl[0], bl[0], tl[0]]
			y = [tl[1], tr[1], tr[1], br[1], br[1], bl[1], bl[1], tl[1]]
			line = Line2D(x, y, linewidth=3.5, color='red')
			ax.add_line(line)
			ax.text(tl[0], tl[1] - 2, '{:s}'.format(text),
			bbox=dict(facecolor='blue', alpha=0.5),
			fontsize=14, color='white')

	plt.axis('off')
	plt.tight_layout()
	plt.draw()
	plt.show()


def text_from_image(image_data: bytes):
	result = getOcrText(image_data)
	if result is not None and result['status'] == 'Succeeded':
		# data8uint = np.fromstring(image_data, dtype=int, sep=' ')
		# img = cv2.cvtColor(cv2.imdecode(data8uint, cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
		# showResultOnImage(result, img)
		return showResultinFile(result)


def extractPdfText(filePath=''):
    fileObject = open(filePath, 'rb')
    pdfFileReader = PyPDF2.PdfFileReader(fileObject)
    totalPageNumber = pdfFileReader.numPages
    print('This pdf file contains totally ' + str(totalPageNumber) + ' pages.')

    currentPageNumber = 0
    text = []
    while(currentPageNumber < totalPageNumber ):
        pdfPage = pdfFileReader.getPage(currentPageNumber)

        text.append(pdfPage.extractText())
        currentPageNumber += 1

    return text


def narrate_book_parse(url, sound=False):     #This function returns text from the book.
	global i
	dir_path = os.path.dirname(os.path.realpath(__file__))
	filename = "temporary.pdf"
	filePath = os.path.join(dir_path, filename)
	r = requests.get(url, allow_redirects=True, stream=True)
	with open(filename, 'wb') as f:
		for chunk in r.iter_content():
			f.write(chunk)

	all_pages = extractPdfText(filePath)
	all_text = ""
	for page in all_pages:
		i += 1
		all_text += page
		app = TextToSpeech(page, os.getenv('SpeechKey') or "")
		app.get_token()
		app.save_audio()
	i = 0
	if sound:
		return combine_all_audio()
	return all_text


def slow_down_audio(audio_file, Change_RATE):
	dir_path = os.path.dirname(os.path.realpath(__file__))
	outfile = os.path.join(dir_path, "narration.wav")
	CHANNELS = 1
	swidth = 2
	# Change_RATE = 2

	spf = wave.open(audio_file, 'rb')
	RATE = spf.getframerate()
	signal = spf.readframes(-1)

	wf = wave.open(outfile, 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(swidth)
	wf.setframerate(RATE*Change_RATE)
	wf.writeframes(signal)
	wf.close()
	return outfile


def combine_all_audio():
	global all_audio
	dir_path = os.path.dirname(os.path.realpath(__file__))
	data = []
	outfile = os.path.join(dir_path, "narration_1.wav")
	for infile in all_audio:
		w = wave.open(infile, 'rb')
		data.append([w.getparams(), w.readframes(w.getnframes())])
		w.close()

	print('audio elements = '+str(len(data)))

	output = wave.open(outfile, 'wb')
	output.setparams(data[0][0])
	for data_ele in data:
		output.writeframes(data_ele[1])
	output.close()
	all_audio = []
	return outfile
