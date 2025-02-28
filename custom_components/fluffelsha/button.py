# config/custom_components/fluffelsha/button.py

from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback

class FluffelshaButton(ButtonEntity):
    """Button-Entität für FluffelsHA."""

    def __init__(self, name, unique_id):
        self._attr_name = name
        self._attr_unique_id = unique_id

    def press(self):
        """Handle the button press."""
        self.hass.services.call("notify", "mobile_app", {
            "message": f"Der Button {self.name} wurde gedrückt!"
        })


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Fluffelsha button platform."""
    # Erstellen Sie mehrere Buttons
    buttons = [
        FluffelshaButton("FluffelsHA Button 1", "fluffelsha_button_1"),
        FluffelshaButton("FluffelsHA Button 2", "fluffelsha_button_2"),
        FluffelshaButton("FluffelsHA Button 3", "fluffelsha_button_3"),
    ]
    async_add_entities(buttons)