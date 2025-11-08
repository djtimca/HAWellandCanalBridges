"""Definition and setup of the Welland Canal Bridges Sensors for Home Assistant."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.const import ATTR_NAME
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    ATTR_IDENTIFIERS,
    ATTR_MANUFACTURER,
    ATTR_MODEL,
    COORDINATOR,
    DOMAIN,
)

if TYPE_CHECKING:
    from . import WellandCanalBridgeUpdater

async def async_setup_entry(hass, entry, async_add_entities, discovery_info=None):
    """Set up the binary sensor platforms."""

    coordinator: WellandCanalBridgeUpdater = hass.data[DOMAIN][entry.entry_id][
        COORDINATOR
    ]

    entities = [
        WellandCanalBridge(coordinator, bridge, bridge_id)
        for bridge_id, bridge in coordinator.data.items()
    ]

    async_add_entities(entities, update_before_add=True)


class WellandCanalBridge(CoordinatorEntity, BinarySensorEntity):
    """Defines a Welland Canal Bridge binary sensor."""

    _attr_device_class = BinarySensorDeviceClass.DOOR
    _attr_icon = "mdi:bridge"

    def __init__(
        self,
        coordinator: WellandCanalBridgeUpdater,
        bridge: dict[str, Any],
        bridge_id: str,
    ) -> None:
        """Initialize the bridge entity."""

        super().__init__(coordinator)
        self._bridge_id = bridge_id

        name = bridge.get("name", bridge_id)
        nickname = bridge.get("nickname")
        if nickname:
            name = f"{name} ({nickname})"

        self._attr_name = name
        self._attr_unique_id = f"wellandcanalbridge_{bridge_id}"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the dynamic entity attributes."""

        bridge = self.coordinator.data.get(self._bridge_id, {})

        attrs: dict[str, Any] = {}
        if bridge.get("status") is not None:
            attrs["status"] = bridge["status"]
        if bridge.get("status_code") is not None:
            attrs["status_code"] = bridge["status_code"]
        if bridge.get("last_updated") is not None:
            attrs["last_updated"] = bridge["last_updated"]

        return attrs

    @property
    def device_info(self):
        """Define the device based on device_identifier."""

        device_name = "Welland Canal Bridges"
        device_model = "Bridges"

        return {
            ATTR_IDENTIFIERS: {(DOMAIN, "wellandcanalbridges")},
            ATTR_NAME: device_name,
            ATTR_MANUFACTURER: "Saint Lawrence Seaway",
            ATTR_MODEL: device_model,
        }

    @property
    def is_on(self) -> bool:
        """Return the state."""
        bridge = self.coordinator.data.get(self._bridge_id, {})
        status_code = bridge.get("status_code")
        return status_code in (1, 2)
