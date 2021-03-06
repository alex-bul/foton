import requests
import base64
import json

headless = False

def detect_face(file_name):
    url_detect = "https://detect-face-fnk37ur3qq-an.a.run.app/api/v1/detect/"

    with open(file_name, 'rb') as f:
        image_64_encode = base64.standard_b64encode(f.read())

    payload = json.dumps({'image': image_64_encode.decode('utf-8')})
    headers = {
        'Content-Type': 'application/json'
    }

    return requests.request("POST", url_detect, headers=headers, data=payload).json()


def photo_to_comics(photo_array):
    file_name = photo_array[0]
    if 'data' not in detect_face(file_name):
        raise Exception("На фото не обнаружено лиц!")
    file = open(file_name, "rb")
    files = {'image': file}
    r = requests.post("https://face.bubble.ru/_api/face", files=files)
    file.close()
    return r.content


def photo_to_portrait(photo_array):
    url_convert = "https://convert-to-art-fnk37ur3qq-an.a.run.app/api/v1/convert/"

    file_name = photo_array[0]
    headers = {
        'Content-Type': 'application/json'
    }

    response = detect_face(file_name)
    if 'data' not in response:
        raise Exception("На фото не обнаружено лиц!")
    payload = json.dumps({
        'anno_img': response["data"]["anno_img"],
        'style': response["data"]["style"]
    })
    response = requests.request("POST", url_convert, headers=headers, data=payload).json()
    img_data = response['data']['image']
    return base64.decodebytes(str.encode(img_data))


conventers = [photo_to_portrait, photo_to_comics]
