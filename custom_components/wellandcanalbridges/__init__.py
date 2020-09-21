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

PLATFORMS = ["binary_sensor", "sensor"]

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Welland Canal Bridge Status component."""
    hass.data.setdefault(DOMAIN, {})

    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Welland Canal Bridge Status from a config entry."""
    polling_interval = 5
    api = WellandCanalBridges()

    try:
        await api.get_bridge_status()
    except ConnectionError as error:
        _LOGGER.debug("Welland Canal API: %s", error)
        raise PlatformNotReady from error
        return False
    except ValueError as error:
        _LOGGER.debug("Welland Canal API: %s", error)
        raise ConfigEntryNotReady from error
        return False

    coordinator = WellandCanalBridgeUpdater(
        hass, 
        api=api, 
        name="WellandCanalBridges", 
        polling_interval=polling_interval,
    )

    await coordinator.async_refresh()
    
    if not coordinator.last_update_success:
        raise ConfigEntryNotReady

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

class WellandCanalBridgeUpdater(DataUpdateCoordinator):
    """Class to manage fetching update data from the Welland Canal API."""

    def __init__(
        self,
        hass: HomeAssistant,
        api: str,
        name: str,
        polling_interval: int,
    ):
        """Initialize the global Welland Canal Bridges data updater."""
        self.api = api

        super().__init__(
            hass = hass,
            logger = _LOGGER,
            name = name,
            update_interval = timedelta(seconds=polling_interval),
        )

    async def _async_update_data(self):
        """Fetch data from Welland Canal Bridges API."""

        try:
            _LOGGER.debug("Updating the coordinator data.")
            bridge_data = await self.api.get_bridge_status()
        except ConnectionError as error:
            _LOGGER.info("Welland Canal API: %s", error)
            raise PlatformNotReady from error
        except ValueError as error:
            _LOGGER.info("Welland Canal API: %s", error)
            raise ConfigEntryNotReady from error

        return bridge_data
