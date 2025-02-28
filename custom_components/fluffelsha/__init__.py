from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.helpers import discovery
from homeassistant.helpers.entity import Entity
from homeassistant.components.switch import SwitchEntity

async def async_setup(hass: HomeAssistant, config: dict):
    """Initialisiere die Entitäten ohne Konfigurationsfluss."""
    # Registriere den Schalter direkt ohne den config_flow
    hass.helpers.entity_component.async_add_entities([FluffelshaButton()])
    return True

async def async_setup_entry(hass: HomeAssistant, entry, async_add_entities):
    """Wird aufgerufen, wenn die Integration über HACS oder die Konfigurationseinträge installiert wird."""
    async_add_entities([FluffelshaButton()])
