# config/custom_components/fluffelsha/button.py

from homeassistant.components.button import ButtonEntity

class FluffelshaButton(ButtonEntity):
    """Button-Entität für FluffelsHA."""

    def __init__(self):
        self._attr_name = "FluffelsHA Button"

    def press(self):
        """Handle the button press."""
        self.hass.services.call("notify", "mobile_app", {
            "message": "Der FluffelsHA Button wurde gedrückt!"
        })


from homeassistant.helpers.entity_platform import AddEntitiesCallback

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Fluffelsha platform."""
    async_add_entities([FluffelshaButton()])