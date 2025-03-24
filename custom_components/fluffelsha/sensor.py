# config/custom_components/fluffelsha/sensor.py

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.core import callback
from homeassistant.helpers.event import async_track_state_change

class StrompreisSensor(SensorEntity):
    """Sensor, der den Strompreis bereitstellt."""

    def __init__(self, entity_id):
        self._attr_name = "Strompreis"
        self._attr_unique_id = "fluffelsha_strompreis"
        self._entity_id = entity_id
        self._state = None

    async def async_added_to_hass(self):
        """Wird aufgerufen, wenn die Entität zu Home Assistant hinzugefügt wird."""
        @callback
        def async_state_changed_listener(entity, old_state, new_state):
            """Wird aufgerufen, wenn sich der Zustand der Strompreis-Entität ändert."""
            if new_state is not None:
                self._state = float(new_state.state)
                self.async_write_ha_state()

        async_track_state_change(self.hass, self._entity_id, async_state_changed_listener)

    @property
    def state(self):
        """Gibt den aktuellen Strompreis zurück."""
        return self._state

class VerbrauchInEuroSensor(SensorEntity):
    """Sensor, der den aktuellen Verbrauch in Euro berechnet."""

    def __init__(self, strompreis_sensor, verbrauchs_entities):
        self._attr_name = "Verbrauch in Euro"
        self._attr_unique_id = "fluffelsha_verbrauch_in_euro"
        self._strompreis_sensor = strompreis_sensor
        self._verbrauchs_entities = verbrauchs_entities
        self._state = None

    async def async_added_to_hass(self):
        """Wird aufgerufen, wenn die Entität zu Home Assistant hinzugefügt wird."""
        @callback
        def async_state_changed_listener(entity, old_state, new_state):
            """Wird aufgerufen, wenn sich der Zustand einer Verbrauchs- oder Strompreis-Entität ändert."""
            self._update_state()
            self.async_write_ha_state()

        # Überwache alle Verbrauchs- und Strompreis-Entitäten
        for entity_id in self._verbrauchs_entities:
            async_track_state_change(self.hass, entity_id, async_state_changed_listener)
        async_track_state_change(self.hass, self._strompreis_sensor.entity_id, async_state_changed_listener)

    def _update_state(self):
        """Berechnet den Verbrauch in Euro basierend auf dem Strompreis und dem Verbrauch."""
        strompreis = self._strompreis_sensor.state
        if strompreis is None:
            self._state = None
            return

        gesamtverbrauch = 0
        for entity_id in self._verbrauchs_entities:
            state = self.hass.states.get(entity_id)
            if state is not None and state.state not in ("unknown", "unavailable"):
                try:
                    gesamtverbrauch += float(state.state)  # Verbrauchswert in Watt
                except ValueError:
                    pass  # Falls der Verbrauchswert kein gültiger Float ist

        self._state = round(strompreis * (gesamtverbrauch / 1000), 2)  # Umrechnung von Watt zu kWh

    @property
    def state(self):
        """Gibt den Verbrauch in Euro zurück."""
        return self._state

class GesamtverbrauchInWattSensor(SensorEntity):
    """Sensor, der den Gesamtverbrauch in Watt berechnet."""

    def __init__(self, verbrauchs_entities):
        self._attr_name = "Gesamtverbrauch in Watt"
        self._attr_unique_id = "fluffelsha_gesamtverbrauch_in_watt"
        self._verbrauchs_entities = verbrauchs_entities
        self._state = None

    async def async_added_to_hass(self):
        """Wird aufgerufen, wenn die Entität zu Home Assistant hinzugefügt wird."""
        @callback
        def async_state_changed_listener(entity, old_state, new_state):
            """Wird aufgerufen, wenn sich der Zustand einer Verbrauchs-Entität ändert."""
            self._update_state()
            self.async_write_ha_state()

        # Überwache alle Verbrauchs-Entitäten
        for entity_id in self._verbrauchs_entities:
            async_track_state_change(self.hass, entity_id, async_state_changed_listener)

    def _update_state(self):
        """Berechnet den Gesamtverbrauch in Watt basierend auf den Verbrauchssensoren."""
        gesamtverbrauch = 0
        for entity_id in self._verbrauchs_entities:
            state = self.hass.states.get(entity_id)
            if state is not None and state.state not in ("unknown", "unavailable"):
                try:
                    gesamtverbrauch += float(state.state)  # Verbrauchswert in Watt
                except ValueError:
                    pass  # Falls der Verbrauchswert kein gültiger Float ist

        self._state = round(gesamtverbrauch, 2)  # Gesamtverbrauch in Watt

    @property
    def state(self):
        """Gibt den Gesamtverbrauch in Watt zurück."""
        return self._state

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Fluffelsha sensor platform."""
    strompreis_entity = config.get("strompreis_entity")
    verbrauchs_entities = config.get("verbrauchs_entities", [])

    if not strompreis_entity or not verbrauchs_entities:
        return  # Konfiguration ist nicht vollständig, daher keine Entitäten erstellen

    # Stelle sicher, dass die übergebenen Entitäten gültige Strings sind
    if not isinstance(strompreis_entity, str) or not all(isinstance(e, str) for e in verbrauchs_entities):
        return  # Ungültige Konfiguration, daher keine Entitäten erstellen

    # Erstelle die Sensoren
    strompreis_sensor = StrompreisSensor(strompreis_entity)
    verbrauch_in_euro_sensor = VerbrauchInEuroSensor(strompreis_sensor, verbrauchs_entities)
    gesamtverbrauch_in_watt_sensor = GesamtverbrauchInWattSensor(verbrauchs_entities)

    # Füge die Entitäten hinzu
    async_add_entities([verbrauch_in_euro_sensor, gesamtverbrauch_in_watt_sensor])
