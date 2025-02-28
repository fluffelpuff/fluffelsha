# config/custom_components/fluffelsha/__init__.py

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up the Fluffelsha integration from a config entry."""
    # Richten Sie die Button-Entität ein
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "button")
    )
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload the Fluffelsha integration."""
    # Entladen Sie die Button-Entität
    await hass.config_entries.async_forward_entry_unload(entry, "button")
    return True