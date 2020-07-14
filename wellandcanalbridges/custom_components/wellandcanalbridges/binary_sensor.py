import logging

from datetime import timedelta
from homeassistant.components.binary_sensor import BinarySensorDevice
from wellandcanalbridges import WellandCanalBridges

__version__ = '0.0.1'

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=60)

ICON = 'mdi:bridge'

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):

    """Set up the bridge status devices."""
    api_client = WellandCanalBridges()

    response = await api_client.get_bridge_status()

    devices = []

    for bridge in response['bridges']:
      devices.append(WellandCanalBridge(bridge))

    async_add_entities(devices, True)

class WellandCanalBridge(BinarySensorDevice):

  def __init__(self, bridge):
    self.api_client = WellandCanalBridges()
    self.bridge = bridge
    self.device_name = bridge['name'].replace(" ", "_")
    self._status = None
    self._statustext = None
    self._friendly_name = bridge['location']

    if bridge['nickname'] != "":
      self._friendly_name += " (" + bridge['nickname'] + ")"

  async def async_update(self):
    response = await self.api_client.get_bridge_status()

    for bridge in response['bridges']:
      if bridge['name'].replace(" ","_") == self._device_name:
        if bridge['status']['status_type'] == 1:
          self._status = True
        else:
          self._status = False
        
        self._statustext = bridge['status']['status']
    
  @property
  def name(self):
    return self.device_name
  
  @property
  def is_on(self):
    return self._status
  
  @property
  def device_class(self):
    return 'door'
  
  @property
  def icon(self):
    return ICON

  @property
  def friendly_name(self):
    return self._friendly_name

  @property
  def device_state_attributes(self):
    return {"Status":self._statustext}

    

    