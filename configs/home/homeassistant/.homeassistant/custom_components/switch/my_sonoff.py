"""
Send HTTP rest call to control Sonoff
"""
import logging
import requests
import json
import time
import voluptuous as vol

from homeassistant.components.switch import SwitchDevice, PLATFORM_SCHEMA
from homeassistant.const import (
    CONF_SWITCHES, CONF_NAME, CONF_IP_ADDRESS)
import homeassistant.helpers.config_validation as cv

RESP_TIMEOUT = 1
POWER_ON_CMD = '/cm?cmnd=Power%20On'
POWER_OFF_CMD = '/cm?cmnd=Power%20Off'
GET_STATUS_CMD = '/cm?cmnd=Status'

_LOGGER = logging.getLogger(__name__)

SWITCH_SCHEMA = vol.Schema({
    vol.Required(CONF_IP_ADDRESS): cv.string,
})

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_SWITCHES): vol.Schema({cv.string: SWITCH_SCHEMA}),
})


# pylint: disable=no-member
def setup_platform(hass, config, add_entities, discovery_info=None):
    """Find and return switches controlled by shell commands."""
    devices = config.get(CONF_SWITCHES, {})
    switches = []

    for dev_name, device_config in devices.items():
        switches.append(
            SonoffSwitch(
                device_config.get(CONF_NAME, dev_name),
                device_config.get(CONF_IP_ADDRESS))
            )

    if not switches:
        _LOGGER.error("No switches added")
        return False

    add_entities(switches)


class SonoffSwitch(SwitchDevice):
    """Representation of a Sonoff switch."""

    def __init__(self, name, ip_address):
        """Initialize the switch."""
        self._name = name
        self._base_url = 'http://' + ip_address
        self._state = False

    @property
    def should_poll(self):
        """No polling needed."""
        return True

    @property
    def name(self):
        """Return the name of the switch."""
        return self._name

    @property
    def is_on(self):
        """Return true if device is on."""
        return self._state

    def _send_code(self, url):
        """Send the code(s)."""
        try:
            resp = requests.get(url, timeout=RESP_TIMEOUT)
            resp.raise_for_status()
        except requests.exceptions.ConnectionError as errc:
            _LOGGER.error("Connection Error %s", errc)
            return None
        except requests.exceptions.Timeout as errt:
            _LOGGER.error("Connection Timeout %s", errt)
            return None

        data = json.loads(resp.text)
        return data

    def update(self):
        """Update device state."""
        power_state = 0
        data = self._send_code(self._base_url + GET_STATUS_CMD)
        if data != None:
            power_state = data.get('Status')['Power']
        self._state = power_state

    def turn_on(self, **kwargs):
        """Turn the switch on."""
        data = self._send_code(self._base_url + POWER_ON_CMD)
        self._state = True
        self.schedule_update_ha_state()

    def turn_off(self, **kwargs):
        """Turn the switch off."""
        data = self._send_code(self._base_url + POWER_OFF_CMD)
        self._state = False
        self.schedule_update_ha_state()
