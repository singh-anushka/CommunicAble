import speech_recognition as sr
import cv2
import os
import string
import os
import requests

def testing():
    return {"message": "This is the Note endpoint."}

dir_path = os.path.dirname(os.path.realpath(__file__))

def getSignVideo(url_to_audio):
    r = requests.get(url_to_audio, allow_redirects=True, stream=True)
    with open(os.path.join(dir_path, 'test.wav'), 'wb') as f:
        for chunk in r.iter_content():
            f.write(chunk)

    r = sr.Recognizer()

    arr=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r',
    's','t','u','v','w','x','y','z']

    with sr.AudioFile(os.path.join(dir_path, 'test.wav')) as source:
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 3
        audio = r.listen(source)

        # recognize speech using Sphinx
        a=r.recognize_sphinx(audio)

        print("you said " + a.lower())

        for c in string.punctuation:
            a= a.replace(c,"")

        images = []
        for i in range(len(a)):
            if a[i] in arr:
                ImageAddress = os.path.join(dir_path, '../utils/letters/'+a[i]+'.jpg')
                images.append(ImageAddress)
            else:
                continue

        frame = cv2.imread(images[0])
        height, width, layers = frame.shape

        video = cv2.VideoWriter(os.path.join(dir_path, 'output.webm'), cv2.VideoWriter_fourcc('v', 'p', '9', '0'), 30, (width, height))

        for image in images:
            for _ in range(20):
                video.write(cv2.imread(image))

        cv2.destroyAllWindows()
        video.release()
        print(os.path.join(dir_path, 'output.webm'))
        return os.path.join(dir_path, 'output.webm')