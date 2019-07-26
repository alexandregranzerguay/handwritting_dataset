import requests, json
import shutil, random, os
from report import openReport

url = "https://southcentralus.api.cognitive.microsoft.com/customvision/v3.0/Prediction/98cfcb17-841d-4b72-a84b-84ec4151f5a2/classify/iterations/Iteration3/image"
prediction_key = "80baf3ea051a442ab0805892939a7591"
content_type = 'application/octet-stream'
headers = {'Prediction-Key': prediction_key, 'Content-Type': content_type}

def successEval(tagName, trueName, probability):
    desired_cat = ['Email', 'Form', 'Letter', 'Memo', 'News', 'Note', 'Report', 'Resume']
    evaluate = False
    for items in desired_cat:
        if not trueName in items.lower():
            continue
        else:
            evaluate = True
    if probability >= 0.5 and tagName == trueName and evaluate :
        return True, 'successfully classified document'
    elif probability >= 0.5 and tagName != trueName and evaluate:
        return False, 'unsuccessfully classified document'
    elif probability >= 0.5 and not evaluate:
        return False, 'classified when it should have been Negative'
    elif probability < 0.5 and not evaluate:
        return True, 'successfully identified as Negative'
    elif probability < 0.5 and evaluate:
        return False, 'Could not determine correct classification'
    else:
        return False, [tagName, trueName, probability, 'Unexpected error']

def main():
    # randomly select 10 documents in each category to test
    categories = ['ADVE', 'Email', 'Form', 'Letter', 'Memo', 'News', 'Note', 'Report', 'Resume', 'Scientific']
    api_res = []
    mov_ave = 0
    for folder in categories:
        filenames = random.sample(os.listdir('./'+folder+'/testing'), 20)
        for fname in filenames:
            srcpath = os.path.join('./'+folder+'/testing', fname)
            # make request to vision
            print(srcpath)
            data = open(srcpath, 'rb').read()
            try:
                r = requests.post(url, headers=headers, data=data)
            except requests.exceptions.RequestException as e:
                print(e)
            try:
                res = r.json()
                # l_res = json.loads(res)
                probability = res['predictions'][0]['probability']
                tagName = res['predictions'][0]['tagName'].lower()
                s,e = successEval(tagName, folder.lower(), probability)
                print(e)
                res_dict = {'tagName':tagName, 'probability': probability, 'success': s}
                api_res.append(res_dict.copy())
            except:
                api_res.append('Did not work on image: '+srcpath)
                continue
            # input("press Enter to continue")
    filepath='./report.json'
    writeReportToFile(api_res, filepath)
    openReport(filepath)

def writeReportToFile(report, filepath):
    with open(filepath, 'w+') as f:
        json.dump(report, f)

if __name__=="__main__":
    main()