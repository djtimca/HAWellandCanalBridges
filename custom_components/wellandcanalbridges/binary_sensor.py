""" Binary Sensor reporting the status of Welland Canal Bridges in Niagara, ON, Canada """

import logging
from homeassistant.helpers.entity import Entity
from homeassistant.components.binary_sensor import BinarySensorDevice

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
  """ Setup the Bridge Sensors """
  
  async_add_entities(WellandCanalBridge(), True)

class WellandCanalBridge(BinarySensorDevice):
  """ Representation of a Bridge """

  def __init__(self):
    """ Initialize the Sensor """
    self._state  = None
    self._name = "Test"
    self._device_class = "door"

  @property
  def name(self):
    """ Return the name """
    return self._name

  @property
  def is_on(self):
    """ Return the state """
    return self._state
  
  @property
  def device_class(self):
    """ Return the device class """
    return self._device_class

  async def async_update(self):
    """ Update the Status """
    self._state = True
