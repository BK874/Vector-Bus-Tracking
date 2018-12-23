# Brian Knotten
# Vector Bus Tracker

from datetime import datetime as dt, timedelta
import requests
import sys
import xml.etree.ElementTree as ET

from settings import API_KEY, DURATION, LOG_FILE, PREDICTIONS, STOPS

import anki_vector

# Constants:
API_URL = 'http://realtime.portauthority.org/bustime/api/v1/getpredictions'
end_time = dt.now() + timedelta(seconds = DURATION)

args = anki_vector.util.parse_command_args()

# Log messages
def log(msg, file = LOG_FILE, mode = 'w', display = True):
    # Writes a message 'msg' to log file at path 'log_file'
    if file:
        with open(file, mode) as f:
            f.write("{}  ::  {}\n".format(dt.now().isoformat(), msg))
    elif display:
        print(msg)

# Send requests to Port Authority's RealTime API
# For each stop, route, direction listed in settings, find the next
# arrival time and print it
message = ""
for request in PREDICTIONS:
    # Insert API key into request
    request.update({'key': API_KEY})
    # Request the API
    response = requests.get(API_URL, params = request)
        
    if response.status_code == 200:
        # Parse into ElementTree
        results = ET.fromstring(response.text)
        log(request['rt'])
        
        # The first prediction result is the next arrival
        if not results.findall('error'):
            prediction = results.findall('prd')[0]
            
            if len(prediction):
                arrival = dt.strptime(prediction.findall('prdtm')[0].text,
                                      "%Y%m%d %H:%M")
                time = arrival - dt.now()
                message += "The {} will arrive at {} in {:.0f} minutes at {}.\n".format(request['rt'], STOPS[request['stpid']], (time.seconds / 60), arrival.strftime('%I:%M'))
                # No predictions frequently means the bus isn't coming
                # in the next 30 minutes.
        else:
            log('[ERROR] - no predictions for {}'.format(request['rt']))
            message += "The {} is not being tracked.\n".format(request['rt'])
    else:
        log('[ERROR] - request error (code: {})'.format(response.status_code))
        message += "API ERROR"
if not message:
    message = "No buses predicted in the next 30 minutes"
    
log('No errors')
with anki_vector.Robot(args.serial) as robot:
    robot.say_text(message)
print(message)
