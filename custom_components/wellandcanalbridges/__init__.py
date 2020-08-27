"""The Welland Canal Bridge Status integration."""
import asyncio

import voluptuous as vol
import logging

from datetime import timedelta
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.exceptions import ConfigEntryNotReady, PlatformNotReady
from wellandcanalbridges import WellandCanalBridges

from .const import DOMAIN, COORDINATOR, CANAL_API

CONFIG_SCHEMA = vol.Schema({DOMAIN: vol.Schema({})}, extra=vol.ALLOW_EXTRA)
_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["binary_sensor"]

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Welland Canal Bridge Status component."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Welland Canal Bridge Status from a config entry."""
    polling_interval = 5
    api = WellandCanalBridges()

    async def async_update_data():
        """Fetch data from API endpoint."""
        _LOGGER.debug("Updating the coordinator data.")
        bridge_data = await api.get_bridge_status()
        
        return bridge_data

    coordinator = DataUpdateCoordinator(
        hass, 
        _LOGGER, 
        name="WellandCanalBridges", 
        update_method=async_update_data,
        update_interval=timedelta(seconds=polling_interval),
    )

    await coordinator.async_refresh()
    
    if not coordinator.last_update_success:
        raise ConfigEntryNotReady

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        COORDINATOR: coordinator,
        CANAL_API: api
    }

    for component in PLATFORMS:
        _LOGGER.info("Setting up platform: %s", component)
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, component)
                for component in PLATFORMS
            ]
        )
    )
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
