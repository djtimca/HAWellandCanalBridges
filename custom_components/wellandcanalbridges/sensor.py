"""Definition and setup of the Welland Canal Bridges Sensors for Home Assistant."""

import logging

from datetime import timedelta

from homeassistant.components.sensor import ENTITY_ID_FORMAT
from homeassistant.const import ATTR_NAME
import homeassistant.helpers.config_validation as cv
import homeassistant.util.dt as dt_util
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from . import WellandCanalBridgeUpdater

from .const import COORDINATOR, DOMAIN, ATTR_IDENTIFIERS, ATTR_MANUFACTURER, ATTR_MODEL

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities, discovery_info=None):
    """Set up the sensor platforms."""

    coordinator = hass.data[DOMAIN][entry.entry_id][COORDINATOR]
    bridges = []
    
    for bridge_id, bridge in coordinator.data.items():
        bridges.append(WellandCanalBridge(coordinator, bridge, bridge_id))
    
    async_add_entities(bridges)

class WellandCanalBridge(CoordinatorEntity):
    """Defines a Welland Canal Bridge sensor."""

    def __init__(
        self, 
        coordinator: WellandCanalBridgeUpdater, 
        bridge: dict, 
        bridge_id: str
        ):
        """Initialize Entities."""

        super().__init__(coordinator=coordinator)

        bridgename = f"{bridge['name']} - {bridge['location']}"
        if bridge["nickname"] != "":
            bridgename = f"{bridgename} ({bridge['nickname']})"
        
        self._name = bridgename
        self._unique_id = f"wellandcanalbridge_{bridge_id}"
        self._state = bridge["status"]["status"]
        self._icon = "mdi:bridge"
        self._bridge_id = bridge_id
        self._attrs = {}

    @property
    def unique_id(self):
        """Return the unique Home Assistant friendly identifier for this entity."""
        return self._unique_id

    @property
    def name(self):
        """Return the friendly name of this entity."""
        return self._name

    @property
    def icon(self):
        """Return the icon for this entity."""
        return self._icon

    @property
    def device_state_attributes(self):
        """Return the attributes."""
        self._attrs["last_updated"] = self.coordinator.data[self._bridge_id]["status"]["updated_at"]
        self._attrs["available"] = (self.coordinator.data[self._bridge_id]["status"]["status_type"] == 1)

        return self._attrs

    @property
    def device_info(self):
        """Define the device based on device_identifier."""

        device_name = "Welland Canal Bridges"
        device_model = "Bridges Detail"

        return {
            ATTR_IDENTIFIERS: {(DOMAIN, "wellandcanalbridgesdetail")},
            ATTR_NAME: device_name,
            ATTR_MANUFACTURER: "Saint Lawrence Seaway",
            ATTR_MODEL: device_model,
        }

    @property
    def state(self):
        """Return the state."""
        
        return self.coordinator.data[self._bridge_id]["status"]["status"]

    async def async_update(self):
        """Update Welland Canal Bridge Entity."""
        await self.coordinator.async_request_refresh()
                
    async def async_added_to_hass(self):
        """Subscribe to updates."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

