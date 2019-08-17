#coding:utf-8
import requests
import json
import base64
import config
import random

def google_vision_api(output_path):
    KEY = config.API_KEY
    url = 'https://vision.googleapis.com/v1/images:annotate?key='
    api_url = url + KEY
    #画像読み込み
    img_file_path = output_path
    img = open(img_file_path, 'rb')
    img_byte = img.read()
    img_content = base64.b64encode(img_byte).decode("utf-8")
    #リクエストBody作成
    req_body = json.dumps({
            'requests': [{
                    'image': {
                        'content': img_content
                        },
                    'features': [{
                            'type': 'LABEL_DETECTION',
                            'maxResults': 5,
                            }]
                    }]
            })
    #リクエスト発行
    res = requests.post(api_url, data=req_body)
    #リクエストから画像情報取得
    res_json = res.json()
    labels = res_json['responses'][0]['labelAnnotations']
    label_list = []
    for value in labels:
        label_list.append(value['description'])
    print(random.choice(label_list))
    return random.choice(label_list)

if __name__ == '__main__':
    google_vision_api()

