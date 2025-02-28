# config/custom_components/fluffelsha/button.py

from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback

class FluffelshaButton(ButtonEntity):
    """Button-Entität für FluffelsHA."""

    def __init__(self):
        self._attr_name = "FluffelsHA Button"
        self._attr_unique_id = "fluffelsha_button"

    def press(self):
        """Handle the button press."""
        # Hier können Sie die Logik für den Button-Klick hinzufügen.
        self.hass.services.call("notify", "mobile_app", {
            "message": "Der FluffelsHA Button wurde gedrückt!"
        })


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Fluffelsha button platform."""
    async_add_entities([FluffelshaButton()])