import requests
import shutil, random, os

url = "https://southcentralus.api.cognitive.microsoft.com/customvision/v3.0/Prediction/98cfcb17-841d-4b72-a84b-84ec4151f5a2/classify/iterations/Iteration3/image"
prediction_key = "80baf3ea051a442ab0805892939a7591"
content_type = 'application/octet-stream'
headers = {'Prediction-Key': prediction_key, 'Content-Type': content_type}

# randomly select 10 documents in each category to test
filenames = random.sample(os.listdir(dirpath), 100)
categories = ['ADVE', 'Email', 'Form', 'Letter', 'Memo', 'News', 'Note', 'Report', 'Resume', 'Scientific']
for folder in categories:
    for fname in filenames:
        srcpath = os.path.join('./'+folder+'/testing', fname)
        # make request to vision
        files = {'media': open(srcpath, 'rb')}
        try:
            r = requests.post(url, headers=headers, files=files)
        except requests.exceptions.RequestException as e:
            print(e)
        input("press Enter to continue")
