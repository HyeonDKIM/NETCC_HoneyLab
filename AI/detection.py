import os, re, glob
import cv2
import numpy as np
from keras.models import model_from_json
from influxdb import InfluxDBClient
from datetime import datetime
from time import time

client = InfluxDBClient('172.17.0.1', 8086, 'root', 'root', 'NUC2')

categories = ["healthy", "leafminer","leafmold","leafspot","yellowleafcurl"]
json_file = open("//home//dnslab2//yolo//Weights//version_without_Canker.json", "r")
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights("//home//dnslab2//yolo//Weights//version_without_Canker.h5")
print("loaded model from disk")

def Dataization(img_path):
    image_w = 32
    image_h = 32
    img=cv2.imread(img_path)
    img=cv2.resize(img, None, fx=image_w/img.shape[1], fy=image_h/img.shape[0])
    return (img/256)

def MakeRealTime():
    now = datetime.now()
    time = [now.year, now.month, now.day, now.hour, now.minute, now.second]
    realTime = ""
    for i in range(0, 6):
        if time[i] < 10:
            time[i] = '0' + str(time[i])
        else:
            time[i] = str(time[i])
        realTime = realTime + '_' + time[i]
    realTime = realTime[1:len(realTime)]

    return realTime

def InsertSystemLog(_realTime, _region, _state, _timeStamp):
    json_body = [
        {
            "measurement":"systemLog",
            "tags": {
                "real_time": _realTime,
                "region": _region
            },
            "fields": {
                "state": _state,
                "timeStamp": _timeStamp
            }
        }
    }
    client.write_points(json_body)

def InsertDetectLog(_realTime, _region, _disease):
    detectTime = client.query('select \"timeStamp\" from systemLog where \"realTime\"=\'{}\''.format(_realTime))
    detectTime = str(detectTime)[len(str(detectTime)) - 23 : len(str(detectTime)) - 10]
    _fromTime = detectTime - 3600000
    _toTime = detectTime + 3600000
    json_body = [
        {
            "measurement":"detectLog",
            "tags": {
                "realTime": _realTime,
                "region": _region
            },
            "fields": {
                "disease": _disease,
                "fromTime": _fromTime,
                "toTime": _toTime
            }
        }
    ]
    client.write_points(json_body)

src=[]
name=[]
test=[]

image_dir= "//home//dnslab2//yolo//Yolo_detected//"
destination_dir = "//home//dnslab2//yolo//AI_detected//" #저장 목적지

for file in os.listdir(image_dir):
    if (file.find('.jpg') is not -1):
        src.append(image_dir+file)
        name.append(file)
        test.append(Dataization(image_dir+file))

test = np.array(test)
predict = loaded_model.predict_classes(test)
cnt = 0 #healthy라고 판단한 개수
cnt_leafminer = 0
cnt_leafmold = 0
cnt_leafspot = 0
cnt_yellowleafcurl = 0

# 숫자 안겹치게 이미지 저장하는 코드
def Save_file(src, disease, i):
    detect_disease = disease
    img_detected = cv2.imread(src)
    stop = False
    count = i
    destination_dir_classfication = "//home//dnslab2//yolo//AI_detected//" + disease + "//" # 이름 변경해서 그에 맞는 경로에 집어넣음
    while (stop == False):
        if (len(os.listdir(destination_dir_classfication))!=0): # 폴더 내에 파일이 있는지 없는지 -> 이거는 파일이 있을때
            if os.path.exists(destination_dir_classfication + str(count) + "_" + detect_disease + ".jpg"): # 파일명 있으면 count++하기
                count += 1
            else:
                cv2.imwrite(destination_dir_classfication + str(count) + "_" + detect_disease + ".jpg", img_detected) # 파일명 없으면 그대로 저장
                print("file saved!")
                stop=True
        else: # 폴더 내에 파일이 없을때
            cv2.imwrite(destination_dir_classfication + str(count) + "_" + detect_disease + ".jpg", img_detected) #그냥 저장
            print("file saved!")
            stop = True

        if (stop == True):
                break


for i in range(len(test)):
    state = None
    print(name[i] + " : , predict: "+str(categories[predict[i]]))
    if(str(categories[predict[i]]) == "healthy"):
        cnt += 1
        os.remove(src[i])
	state = "healthy"
    elif str(categories[predict[i]]) == "leafminer":
        Save_file(src[i],"leafminer",i)
        os.remove(src[i])
	cnt_leafminer += 1
	state = "leafminer"
    elif str(categories[predict[i]]) == "leafmold":
        Save_file(src[i],"leafmold",i)
        os.remove(src[i])
	cnt_leafmold += 1
	state = "leafmold"
    elif str(categories[predict[i]]) == "leafspot":
        Save_file(src[i],"leafspot",i);
        os.remove(src[i])
	cnt_leafspot += 1
	state = "leafspot"
    elif str(categories[predict[i]]) == "yellowleafcurl":
        Save_file(src[i],"yellowleafcurl",i);
        os.remove(src[i])
	cnt_yellowleafcurl += 1
	state = "yellowleafcurl"
    unixTime = str(time())
    unixTime = str(unixTime)[0:len(str(unixTime) - 8])
    presentTime = MakeRealTime()
    InsertSystemLog(presentTime, "FARM_1", state, unixTime)
    InsertDetectLog(presentTime, "FARM_1", state)

print("all: "+str(len(test)))
print("leafminer: "+str(cnt_leafminer))
print("leafmold: "+str(cnt_leafmold))
print("leafspot: "+str(cnt_leafspot))
print("yellowleafcurl: "+str(cnt_yellowleafcurl))
