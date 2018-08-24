import time
import random
import string
import logging
import requests
import fliclib

# POST with JSON
import json

DEBOUNCE_SECONDS = 3

BASE_URL = "http://localhost:8123/api/"
STATE_URL = BASE_URL + "states/"
TURN_ON_URL = BASE_URL + "services/switch/turn_on"
TURN_OFF_URL = BASE_URL + "services/switch/turn_off"
HA_DEIVE_ENTRY = "group.living_room"

FLIC_DEVICE_ADDR = "80:e4:da:72:7b:e8"

lastTriggerTime = 0

# Setup logging level
logging.basicConfig(level=logging.DEBUG)
client = fliclib.FlicClient("localhost")


# Device Status : Only for LIGHT
def isAnyLightOn():
    lightFlag = False

    # Request QUERY
    resp = requests.get(STATE_URL + HA_DEIVE_ENTRY , headers='')
    data = json.loads(resp.text)

    # Get LIGHT status
    state = data.get('state')
    if state == 'on':
        lightFlag = True

    return lightFlag


# Trun On/Off Light
def turnOnOffLight(onoff):
    # Service Data format
    req_data = {'entity_id': HA_DEIVE_ENTRY }

    # Request Service
    if onoff == True:
        requests.post(TURN_ON_URL, headers='', json=req_data)
    else :
        requests.post(TURN_OFF_URL, headers='', json=req_data)


# Debounce triggering
def debounce():
    global lastTriggerTime
    debounceFlag = False

    if (time.time() - lastTriggerTime) < DEBOUNCE_SECONDS:
        debounceFlag = True

    lastTriggerTime = time.time()
    return debounceFlag


# Process Light
def process_light():
    if debounce():
        logging.debug("Trigger debounced.")
        return

    lightFlag = isAnyLightOn()
    logging.debug("Light is %d", lightFlag)
    # Toggle Light
    if lightFlag == 1:
        turnOnOffLight(False)
    else:
        turnOnOffLight(True)


# Button detect event
def got_button(channel, click_type, was_queued, time_diff):
    if (channel.bd_addr == FLIC_DEVICE_ADDR and str(click_type) == "ClickType.ButtonDown") :
        logging.debug("Button pressed.")
        process_light()


def got_info(items):
    print(items)
    for bd_addr in items["bd_addr_of_verified_buttons"]:
        cc = fliclib.ButtonConnectionChannel(bd_addr)
        cc.on_button_up_or_down = got_button
        client.add_connection_channel(cc)


# Main routine
# Register Flic info
client.get_info(got_info)
client.handle_events()
