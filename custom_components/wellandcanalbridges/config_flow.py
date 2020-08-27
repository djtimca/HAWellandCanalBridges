"""Config flow for Welland Canal Bridge Status."""
from wellandcanalbridges import WellandCanalBridges

from homeassistant import config_entries
from homeassistant.helpers import config_entry_flow

from .const import DOMAIN


async def _async_has_devices(hass) -> bool:
    """Return if there are devices that can be discovered."""
    # TODO Check if there are any devices that can be discovered in the network.
    api = WellandCanalBridges()
    devices = await api.get_bridge_status()
    return len(devices) > 0


config_entry_flow.register_discovery_flow(
    DOMAIN, "Welland Canal Bridge Status", _async_has_devices, config_entries.CONN_CLASS_UNKNOWN
)
