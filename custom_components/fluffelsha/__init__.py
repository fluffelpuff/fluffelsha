# config/custom_components/fluffelsha/__init__.py

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Fluffelsha component."""
    # Richten Sie die Button-Entitäten ein
    hass.helpers.discovery.load_platform("button", "fluffelsha", {}, config)
    return True