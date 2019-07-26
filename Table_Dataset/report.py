import json

def openReport(filepath):
    with open(filepath, 'r') as f:
        report = json.load(f)
        counter = 0
        ave_proba = 0
        sum_proba = 0
        sum_success = 0
        for line in report:
            counter+=1
            sum_proba += line['probability']
            if line['success'] :
                sum_success += 1
        a,b = calculations(sum_proba, sum_success, counter)   
        # print('Avergae probability of correct answer: '+a+'\n')
        print('Success rate: '+str(int(b))+"%")

def calculations(sum_proba, sum_success, counter):
    ave_proba = sum_proba/counter
    success_rate = sum_success/counter * 100
    return ave_proba, success_rate
