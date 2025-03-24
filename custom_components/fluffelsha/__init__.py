# config/custom_components/fluffelsha/__init__.py

from homeassistant.core import HomeAssistant

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Fluffelsha component."""
    # Lade die Sensor-Plattform und übergebe die Konfiguration
    hass.helpers.discovery.load_platform("sensor", "fluffelsha", config.get("fluffelsha", {}), config)
    return True