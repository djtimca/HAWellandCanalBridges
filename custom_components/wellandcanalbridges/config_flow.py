"""Config flow for Welland Canal Bridge Status."""
from wellandcanalbridges import WellandCanalBridges

from homeassistant import config_entries
from homeassistant.helpers import config_entry_flow

from .const import DOMAIN


async def _async_has_devices(hass) -> bool:
    """Return if there are devices that can be discovered."""

    api = WellandCanalBridges()
    bridge_data = await api.get_bridge_status()
    return bool(bridge_data.get("bridges"))


config_entry_flow.register_discovery_flow(
    DOMAIN, "Welland Canal Bridge Status", _async_has_devices
)
