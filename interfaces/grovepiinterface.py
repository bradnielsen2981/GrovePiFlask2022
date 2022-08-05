import datetime, time, json, logging

LOADED = True
try:
    import urlrequest
    import grove_rgb_lcd    
    import grovepi #must have installed grovepi library   
    import grove_led_strip             
except ImportError: #could be being called from flask file
    LOADED = False #must be trying to run from the web server.

class GrovePiInterface:

    # Any initialisation code should be here - could keep track of ports
    def __init__(self, logger=logging.getLogger()):
        self.logger = logger 
        LOADED = True
        pass

    def log(self, message):
        self.logger.info(message)
        return

    # ------------------------ DEVICES -----------------------------
    # Turn on the led using digital port (1 or 0)
    def set_led_digitalport_value(self, port, value=1):
        try:
            grovepi.pinMode(port,"OUTPUT") #should be in initialise
            grovepi.digitalWrite(port,value)
        except Exception as error:
            print('Problem with LED ' + repr(error))
        return

    # Display the time. Needs to start a Thread
    def set_digit_display_time_digitalport(self, port):
        grovepi.pinMode(port,"OUTPUT")
        grovepi.fourDigit_init(port)
        grovepi.fourDigit_on(port)
        grovepi.fourDigit_brightness(port,8)
        now = datetime.datetime.now()
        grovepi.fourDigit_score(port,now.hour,now.minute)
        return

    # Display a number
    def set_digit_display_number_digitalport(self, number,port):
        leading_zero = 0
        grovepi.pinMode(port,"OUTPUT")
        grovepi.fourDigit_init(port)
        grovepi.fourDigit_on(port)
        grovepi.fourDigit_brightness(port,8)
        grovepi.fourDigit_number(port,number,leading_zero)
        return

    # OLED monitor - set_OLED_I2C1_RGBtuple_message((0,0,125),"It works!!")
    def set_OLED_I2C1_RGBtuple_message(self, colour, message):   #colour is a tuple of (255,255,255)
        grove_rgb_lcd.setRGB(*colour) 
        grove_rgb_lcd.setText(message)
        return

    # grove buzzer is turned on (1 or 0) - this is super annoying
    def set_buzzer_digitalport(self, port, value=1):
        grovepi.pinMode(port,"OUTPUT")
        grovepi.digitalWrite(port,value)
        return

    # TODO Grove - I2C Motor Driver
    # -----------------------------
    # ----------------------------- 
    # -----------------------------

    # ------------------------ SENSORS -----------------------------
    # Read the distance using sound waves return centimeters (2-350cm)
    def read_ultra_digitalport(self, port):
        grovepi.pinMode(port,"INPUT")
        distance = grovepi.ultrasonicRead(port)
        time.sleep(0.03)
        return distance 

    # Read water flow sensor
    def read_waterflow_digitalport(self, port):
        period = 2000
        grovepi.flowEnable(port,period)
        waterflow = grovepi.flowRead()
        #THIS MAY NEED TO RUN OVER 10 SECONDS TO GET A PROPER WATER FLOW
        grovepi.flowDisable()
        return waterflow

    # Read the PH Level
    def read_ph_analogueport(self, port):
        adc_ref = 5 #Reference voltage of ADC is 5v
        grovepi.pinMode(port,"INPUT")
        sensor_value = grovepi.analogRead(port)
        ph = 7 - 1000 * (float)(sensor_value) * adc_ref / 59.16 / 1023
        return ph

    # Read Button return 0 or 1 
    def read_button_digitalport(self, port):
        grovepi.pinMode(port,"INPUT")
        distance = grovepi.digitalRead(port)
        return distance 

    # Read temp (0 - 50 degrees Celsius) and humidity (20% - 90%)
    def read_temp_humidity_sensor_digitalport(self, port):
        grovepi.pinMode(port,"INPUT")
        temp_humidity_list = grovepi.dht(port,0)
        return temp_humidity_list #[temp,hum] = read_temp_humidity_sensor_digitalport(4) - break into parts

    # Read sound sensor returns analogue value 0 - 1023 loudness - to translate to decibels you need identify the distance
    def read_sound_analogueport(self, port):
        grovepi.pinMode(port,"INPUT")
        sound = grovepi.analogRead(port)
        return sound

    # Read the moisture sensor
    def read_moisture_analogueport(self, port):
        grovepi.pinMode(port,"INPUT")
        moisture = grovepi.analogRead(port)
        return moisture

    # Read light sensor returns analogue value 0 - 1023 - not sure how to translate into lux
    def read_light_analogueport(self, port):
        grovepi.pinMode(port,"INPUT")
        light = grovepi.analogRead(port)
        return light

    # read rotation sensor (Grove Rotary Angle Sensor) - can return voltage, degrees
    def read_rotation_analogueport(self, port):
        adc_ref = 5 # Reference voltage of ADC is 5v
        grove_vcc = 5 # Vcc of the grove interface is normally 5v
        grovepi.pinMode(port,"INPUT")
        sensor_value = grovepi.analogRead(port)
        voltage = round((float)(sensor_value) * adc_ref / 1023, 2)
        degrees = round((voltage * 360) / grove_vcc, 2)
        data = [voltage,degrees]
        return data

# ---------------------------------------------------------------------------------
#SINGLETON - CREATE INSTANCE COMMAND FROM FILE
def create_grovepi():
    grove = None
    if LOADED: #ensure libraries can load
        grove = GrovePiInterface() #create instance and return
    return grove

#-------------------------------------------------------------------------------\
# TEST CODE - only runs from within file execution
if __name__ == '__main__':
    grove = GrovePiInterface()
    if grove == None:
        exit()
       
    