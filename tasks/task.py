#TO CREATE A CRON TASK ON YOUR RASPBERRY PI FOLLOW THE STEPS BELOW
#!/usr/bin/python
# crontab -e
# INSERT THE FOLLOWING LINE:
# * * * * * python3 /home/pi/Desktop/MyProject/task.py > /home/pi/Desktop/MyProject/logs/log.txt


#EXAMPLE OF A CRON TASK THAT SENDS DATA TO AN EXTERNAL SERVER
from interfaces import urlrequest
import json, time, datetime
from interfaces.grovepiinterface import *


[temp,hum] = GrovePiInterface.read_temp_humidity_sensor_digitalport(7)
now = time.time()
dictofvalues = {"temp":temp,"hum":hum, "time":now}
print(dictofvalues)
url = "https://nielbrad.pythonanywhere.com/uploadhistory"
response = urlrequest.sendurlrequest(url, dictofvalues) #feel like a callback function should be used
print(response)
resultsdict = json.loads(response)
GrovePiInterface.set_OLED_I2C1_RGBtuple_message((255,0,0), resultsdict['message'])
time.sleep(2)


#PLACE ON AN EXTERNAL SERVER
'''# update the users location and access time
@app.route('/uploadhistory', methods=['GET','POST'])
def uploadhistory():
    resultsdict = {"message":""}
    if request.method == "POST":
        temp = request.form.get('temp')
        hum = request.form.get('hum')
        resultsdict = {"message":"It is very hot"}
    return jsonify(resultsdict)'''