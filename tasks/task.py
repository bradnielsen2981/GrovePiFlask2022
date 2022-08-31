#TO CREATE A CRON TASK ON YOUR RASPBERRY PI FOLLOW THE STEPS BELOW
#!/usr/bin/python
# crontab -e
# INSERT THE FOLLOWING LINE:
# * * * * * python3 /home/pi/Desktop/MyProject/task.py > /home/pi/Desktop/MyProject/logs/log.txt

#EXAMPLE OF A CRON TASK THAT SENDS DATA TO AN EXTERNAL SERVER
from interfaces import urlrequest
import json, time, datetime
from interfaces.grovepiinterface import *
import global_vars


[temp,hum] = GrovePiInterface.read_temp_humidity_sensor_digitalport(7)
now = time.time()
dictofvalues = {"temp":temp,"hum":hum, "time":now}
print(dictofvalues)

#send the data to a URL (Your web server) as form data
url = "https://nielbrad.pythonanywhere.com/uploadhistory" #you can use localhost
response = urlrequest.sendurlrequest(url, dictofvalues) #feel like a callback function should be used

resultsdict = json.loads(response) #if json is return, convert to python dictionary
GrovePiInterface.set_OLED_I2C1_RGBtuple_message((255,0,0), resultsdict['message'])


#PLACE ON AN EXTERNAL SERVER (FLASK)
'''# update the users location and access time
@app.route('/uploadhistory', methods=['GET','POST'])
def uploadhistory():
    resultsdict = {"message":""}
    if request.method == "POST":
        temp = request.form.get('temp')
        hum = request.form.get('hum')
        resultsdict = {"message":"It is very hot"}
        #save data to database
    return jsonify(resultsdict)'''

#PLACE ON AN EXTERNAL SERVER (XAMP)
# create php file called uploadhistory 
# 
'''$_POST['temp'] and $_POST['hum']''' #could be used to access the form data