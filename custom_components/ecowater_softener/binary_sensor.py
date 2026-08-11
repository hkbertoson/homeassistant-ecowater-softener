from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription
)
from homeassistant import config_entries
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    MODEL,
    SOFTWARE_VERSION,
    LOW_SALT_ALERT,
    ERROR_ALERT,
    EXCESSIVE_WATER_USE_ALERT,
    FLOW_MONITOR_ALERT,
    DEPLETION_ALERT,
    SERVICE_REMINDER_ALERT
)

from .coordinator import EcowaterDataCoordinator

BINARY_SENSOR_TYPES: tuple[BinarySensorEntityDescription, ...] = (
    BinarySensorEntityDescription(
        key=LOW_SALT_ALERT,
        name="Low Salt Alert",
        icon="mdi:shaker-outline",
        device_class=BinarySensorDeviceClass.PROBLEM
    ),
    BinarySensorEntityDescription(
        key=ERROR_ALERT,
        name="Error Alert",
        icon="mdi:alert-circle-outline",
        device_class=BinarySensorDeviceClass.PROBLEM
    ),
    BinarySensorEntityDescription(
        key=EXCESSIVE_WATER_USE_ALERT,
        name="Excessive Water Use Alert",
        icon="mdi:water-alert",
        device_class=BinarySensorDeviceClass.PROBLEM
    ),
    BinarySensorEntityDescription(
        key=FLOW_MONITOR_ALERT,
        name="Flow Monitor Alert",
        icon="mdi:water-alert",
        device_class=BinarySensorDeviceClass.PROBLEM
    ),
    BinarySensorEntityDescription(
        key=DEPLETION_ALERT,
        name="Depletion Alert",
        icon="mdi:water-off",
        device_class=BinarySensorDeviceClass.PROBLEM
    ),
    BinarySensorEntityDescription(
        key=SERVICE_REMINDER_ALERT,
        name="Service Reminder",
        icon="mdi:wrench-clock",
        device_class=BinarySensorDeviceClass.PROBLEM
    ),
)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the ecowater binary sensors."""
    config = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = config["coordinator"]

    async_add_entities(
        EcowaterBinarySensor(coordinator, description, config['device_serial_number'])
        for description in BINARY_SENSOR_TYPES
    )

class EcowaterBinarySensor(
    CoordinatorEntity[EcowaterDataCoordinator],
    BinarySensorEntity,
):
    """Implementation of an ecowater binary sensor."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: EcowaterDataCoordinator,
        description: BinarySensorEntityDescription,
        serialnumber
    ) -> None:
        """Initialize the ecowater binary sensor."""
        super().__init__(coordinator)
        self.entity_description = description

        self._serialnumber = serialnumber

        self._attr_unique_id = "ecowater_" + serialnumber.lower() + "_" + self.entity_description.key
        self._attr_is_on = getattr(self.coordinator.data, self.entity_description.key)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_is_on = getattr(self.coordinator.data, self.entity_description.key)
        self.async_write_ha_state()

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._serialnumber)},
            name="Ecowater " + self._serialnumber,
            manufacturer="Ecowater",
            serial_number=self._serialnumber,
            model = getattr(self.coordinator.data, MODEL),
            sw_version = getattr(self.coordinator.data, SOFTWARE_VERSION)
        )
