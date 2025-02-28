# config/custom_components/fluffelsha/switch.py

from homeassistant.components.switch import SwitchEntity

class FluffelshaButton(SwitchEntity):
    """Schalt-Entität, die als Button fungiert."""
    
    def __init__(self):
        self._state = False  # Der Standardstatus des Buttons ist 'aus'

    @property
    def name(self):
        """Name des Buttons."""
        return "FluffelsHA Button"

    @property
    def is_on(self):
        """Zeigt den Status des Buttons."""
        return self._state

    def turn_on(self, **kwargs):
        """Wenn der Button gedrückt wird, sende eine Benachrichtigung."""
        self._state = True
        self.send_notification()
        self.async_write_ha_state()  # Aktualisiert den Zustand der Entität

    def turn_off(self, **kwargs):
        """Setzt den Button auf 'aus' zurück."""
        self._state = False
        self.async_write_ha_state()

    def send_notification(self):
        """Sende eine Benachrichtigung an alle mobilen Geräte."""
        self.hass.services.call("notify", "mobile_app", {
            "message": "Der FluffelsHA Button wurde gedrückt!"
        })


from homeassistant.helpers.entity_platform import AddEntitiesCallback

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Fluffelsha platform."""
    async_add_entities([FluffelshaButton()])