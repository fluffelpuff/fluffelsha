from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant

class FluffelshaButton(SwitchEntity):
    def __init__(self):
        self._state = False  # Der Standardstatus des Buttons ist 'aus'

    @property
    def name(self):
        return "FluffelsHA Button"  # Name des Buttons

    @property
    def is_on(self):
        return self._state  # Zeigt den Status des Buttons

    def turn_on(self, **kwargs):
        """Wenn der Button gedrückt wird, sende eine Benachrichtigung."""
        self._state = True  # Button wird gedrückt (aktiviert)
        self.send_notification()
        self.async_write_ha_state()  # Aktualisiert den Zustand der Entität

    def turn_off(self, **kwargs):
        """Setzt den Button auf 'aus' zurück."""
        self._state = False
        self.async_write_ha_state()

    def send_notification(self):
        """Sende eine Benachrichtigung an alle mobilen Geräte."""
        self.hass.services.async_call("notify", "mobile_app", {
            "message": "Der FluffelsHA Button wurde gedrückt!"
        })

async def async_setup(hass: HomeAssistant, config: dict):
    """Initialisiere die Entitäten ohne Konfigurationsfluss."""
    # Die korrekte Methode zur Registrierung der Entitäten verwenden
    from homeassistant.helpers.entity_platform import async_get_platform
    platform = await async_get_platform(hass, "switch")
    platform.async_add_entities([FluffelshaButton()])
    return True
