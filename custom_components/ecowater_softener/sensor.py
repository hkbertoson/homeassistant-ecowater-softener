from dataclasses import dataclass

from homeassistant.helpers.entity import DeviceInfo
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass
)
from homeassistant import config_entries
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.const import (
    UnitOfVolume,
    UnitOfVolumeFlowRate,
    UnitOfMass,
    UnitOfTemperature,
    UnitOfTime,
    CONCENTRATION_PARTS_PER_MILLION,
    PERCENTAGE,
    EntityCategory
)

from .const import (
    DOMAIN,
    MODEL,
    SOFTWARE_VERSION,
    WATER_AVAILABLE,
    WATER_USAGE_TODAY,
    WATER_USAGE_DAILY_AVERAGE,
    WATER_USAGE_TOTAL,
    UNTREATED_WATER_TOTAL,
    CURRENT_WATER_FLOW,
    PEAK_WATER_FLOW,
    WATER_TEMPERATURE,
    WATER_TEMPERATURE_AVERAGE,
    WATER_TDS,
    CAPACITY_REMAINING_PERCENTAGE,
    EXHAUSTION_PERCENTAGE_AVERAGE,
    OPERATING_CAPACITY,
    WATER_HARDNESS,
    SALT_LEVEL_PERCENTAGE,
    OUT_OF_SALT_ON,
    DAYS_UNTIL_OUT_OF_SALT,
    SALT_TYPE,
    SALT_USAGE_TOTAL,
    SALT_USAGE_PER_RECHARGE_AVERAGE,
    SALT_EFFICIENCY,
    LAST_RECHARGE,
    DAYS_SINCE_RECHARGE,
    RECHARGE_ENABLED,
    RECHARGE_STATUS,
    RECHARGE_TIME_REMAINING,
    RECHARGE_COUNT,
    MANUAL_RECHARGE_COUNT,
    RECHARGE_DAYS_BETWEEN_AVERAGE,
    ROCK_REMOVED,
    ROCK_REMOVED_DAILY_AVERAGE,
    ROCK_REMOVED_SINCE_RECHARGE,
    ERROR_CODE,
    LOW_SALT_TRIP_LEVEL_DAYS,
    DAYS_IN_OPERATION,
    POWER_OUTAGE_COUNT,
    LONGEST_OUTAGE_MINUTES,
    TIME_LOST_EVENTS,
    DAYS_SINCE_LAST_TIME_LOSS
)

from .coordinator import EcowaterDataCoordinator

@dataclass
class EcowaterSensorEntityDescription(SensorEntityDescription):
        """A class that describes sensor entities"""

SENSOR_TYPES: tuple[EcowaterSensorEntityDescription, ...] = (
    EcowaterSensorEntityDescription(
        key=WATER_AVAILABLE,
        name="Water Available",
        icon="mdi:water",
        device_class=SensorDeviceClass.WATER,
        state_class=SensorStateClass.TOTAL,
        native_unit_of_measurement=UnitOfVolume.GALLONS
    ),
    EcowaterSensorEntityDescription(
        key=WATER_USAGE_TODAY,
        name="Water Used Today",
        icon="mdi:water",
        device_class=SensorDeviceClass.WATER,
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement=UnitOfVolume.GALLONS
    ),
    EcowaterSensorEntityDescription(
        key=WATER_USAGE_DAILY_AVERAGE,
        name="Average Water Used per Day",
        icon="mdi:water",
        device_class=SensorDeviceClass.WATER,
        state_class=SensorStateClass.TOTAL,
        native_unit_of_measurement=UnitOfVolume.GALLONS
    ),
    EcowaterSensorEntityDescription(
        key=CURRENT_WATER_FLOW,
        name="Water Flow",
        icon="mdi:water",
        device_class=SensorDeviceClass.VOLUME_FLOW_RATE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfVolumeFlowRate.GALLONS_PER_MINUTE
    ),
    EcowaterSensorEntityDescription(
        key=SALT_LEVEL_PERCENTAGE,
        name="Salt Level Percentage",
        icon="mdi:altimeter",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE
    ),
    EcowaterSensorEntityDescription(
        key=OUT_OF_SALT_ON,
        name="Out of Salt Date",
        icon="mdi:calendar",
        device_class=SensorDeviceClass.DATE
    ),
    EcowaterSensorEntityDescription(
        key=DAYS_UNTIL_OUT_OF_SALT,
        name="Days Until Out of Salt",
        icon="mdi:calendar",
        native_unit_of_measurement=UnitOfTime.DAYS
    ),
    EcowaterSensorEntityDescription(
        key=SALT_TYPE,
        name="Salt Type",
        icon="mdi:shaker-outline"
    ),
    EcowaterSensorEntityDescription(
        key=LAST_RECHARGE,
        name="Last Recharge Date",
        icon="mdi:calendar",
        device_class=SensorDeviceClass.DATE
    ),
    EcowaterSensorEntityDescription(
        key=DAYS_SINCE_RECHARGE,
        name="Days Since Last Recharge",
        icon="mdi:calendar",
        native_unit_of_measurement=UnitOfTime.DAYS
    ),
    EcowaterSensorEntityDescription(
        key=RECHARGE_ENABLED,
        name="Recharge Enabled",
        icon="mdi:refresh"
    ),
    EcowaterSensorEntityDescription(
        key=RECHARGE_STATUS,
        name="Recharge Status",
        icon="mdi:refresh"
    ),
    EcowaterSensorEntityDescription(
        key=ROCK_REMOVED,
        name="Rock Removed",
        icon="mdi:grain",
        device_class=SensorDeviceClass.WEIGHT,
        state_class=SensorStateClass.TOTAL,
        native_unit_of_measurement=UnitOfMass.POUNDS
    ),
    EcowaterSensorEntityDescription(
        key=ROCK_REMOVED_DAILY_AVERAGE,
        name="Average Rock Removed per Day",
        icon="mdi:grain",
        device_class=SensorDeviceClass.WEIGHT,
        state_class=SensorStateClass.TOTAL,
        native_unit_of_measurement=UnitOfMass.POUNDS
    ),
    EcowaterSensorEntityDescription(
        key=ROCK_REMOVED_SINCE_RECHARGE,
        name="Rock Removed Since Last Recharge",
        icon="mdi:grain",
        device_class=SensorDeviceClass.WEIGHT,
        state_class=SensorStateClass.TOTAL,
        native_unit_of_measurement=UnitOfMass.POUNDS
    ),
    EcowaterSensorEntityDescription(
        key=WATER_USAGE_TOTAL,
        name="Total Water Used",
        icon="mdi:water",
        device_class=SensorDeviceClass.WATER,
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement=UnitOfVolume.GALLONS
    ),
    EcowaterSensorEntityDescription(
        key=UNTREATED_WATER_TOTAL,
        name="Total Untreated Water",
        icon="mdi:water-alert",
        device_class=SensorDeviceClass.WATER,
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement=UnitOfVolume.GALLONS
    ),
    EcowaterSensorEntityDescription(
        key=PEAK_WATER_FLOW,
        name="Peak Water Flow",
        icon="mdi:water",
        device_class=SensorDeviceClass.VOLUME_FLOW_RATE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfVolumeFlowRate.GALLONS_PER_MINUTE
    ),
    EcowaterSensorEntityDescription(
        key=WATER_TEMPERATURE,
        name="Water Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS
    ),
    EcowaterSensorEntityDescription(
        key=WATER_TEMPERATURE_AVERAGE,
        name="Average Water Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS
    ),
    EcowaterSensorEntityDescription(
        key=WATER_TDS,
        name="Water TDS",
        icon="mdi:water-opacity",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION
    ),
    EcowaterSensorEntityDescription(
        key=CAPACITY_REMAINING_PERCENTAGE,
        name="Capacity Remaining",
        icon="mdi:gauge",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE
    ),
    EcowaterSensorEntityDescription(
        key=EXHAUSTION_PERCENTAGE_AVERAGE,
        name="Average Exhaustion",
        icon="mdi:gauge",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE
    ),
    EcowaterSensorEntityDescription(
        key=OPERATING_CAPACITY,
        name="Operating Capacity",
        icon="mdi:gauge",
        native_unit_of_measurement="grains"
    ),
    EcowaterSensorEntityDescription(
        key=WATER_HARDNESS,
        name="Water Hardness",
        icon="mdi:water-percent",
        native_unit_of_measurement="gpg"
    ),
    EcowaterSensorEntityDescription(
        key=SALT_USAGE_TOTAL,
        name="Total Salt Used",
        icon="mdi:shaker-outline",
        device_class=SensorDeviceClass.WEIGHT,
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement=UnitOfMass.POUNDS
    ),
    EcowaterSensorEntityDescription(
        key=SALT_USAGE_PER_RECHARGE_AVERAGE,
        name="Average Salt Used per Recharge",
        icon="mdi:shaker-outline",
        device_class=SensorDeviceClass.WEIGHT,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfMass.POUNDS
    ),
    EcowaterSensorEntityDescription(
        key=SALT_EFFICIENCY,
        name="Salt Efficiency",
        icon="mdi:shaker-outline",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement="grains/lb"
    ),
    EcowaterSensorEntityDescription(
        key=RECHARGE_TIME_REMAINING,
        name="Recharge Time Remaining",
        icon="mdi:refresh",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.SECONDS
    ),
    EcowaterSensorEntityDescription(
        key=RECHARGE_COUNT,
        name="Total Recharges",
        icon="mdi:counter",
        state_class=SensorStateClass.TOTAL_INCREASING
    ),
    EcowaterSensorEntityDescription(
        key=MANUAL_RECHARGE_COUNT,
        name="Manual Recharges",
        icon="mdi:counter",
        state_class=SensorStateClass.TOTAL_INCREASING
    ),
    EcowaterSensorEntityDescription(
        key=RECHARGE_DAYS_BETWEEN_AVERAGE,
        name="Average Days Between Recharges",
        icon="mdi:calendar",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTime.DAYS
    ),
    EcowaterSensorEntityDescription(
        key=ERROR_CODE,
        name="Error Code",
        icon="mdi:alert-circle-outline",
        entity_category=EntityCategory.DIAGNOSTIC
    ),
    EcowaterSensorEntityDescription(
        key=LOW_SALT_TRIP_LEVEL_DAYS,
        name="Low Salt Alert Trip Level",
        icon="mdi:calendar-alert",
        native_unit_of_measurement=UnitOfTime.DAYS,
        entity_category=EntityCategory.DIAGNOSTIC
    ),
    EcowaterSensorEntityDescription(
        key=DAYS_IN_OPERATION,
        name="Days in Operation",
        icon="mdi:calendar-clock",
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement=UnitOfTime.DAYS,
        entity_category=EntityCategory.DIAGNOSTIC
    ),
    EcowaterSensorEntityDescription(
        key=POWER_OUTAGE_COUNT,
        name="Power Outages",
        icon="mdi:power-plug-off",
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC
    ),
    EcowaterSensorEntityDescription(
        key=LONGEST_OUTAGE_MINUTES,
        name="Longest Power Outage",
        icon="mdi:power-plug-off",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.MINUTES,
        entity_category=EntityCategory.DIAGNOSTIC
    ),
    EcowaterSensorEntityDescription(
        key=TIME_LOST_EVENTS,
        name="Time Lost Events",
        icon="mdi:clock-alert-outline",
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC
    ),
    EcowaterSensorEntityDescription(
        key=DAYS_SINCE_LAST_TIME_LOSS,
        name="Days Since Last Time Loss",
        icon="mdi:clock-alert-outline",
        native_unit_of_measurement=UnitOfTime.DAYS,
        entity_category=EntityCategory.DIAGNOSTIC
    ),
)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the ecowater sensor."""
    config = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = config["coordinator"]

    async_add_entities(
        EcowaterSensor(coordinator, description, config['device_serial_number'])
        for description in SENSOR_TYPES
    )

class EcowaterSensor(
    CoordinatorEntity[EcowaterDataCoordinator],
    SensorEntity,
):
    """Implementation of an ecowater sensor."""

    _attr_has_entity_name = True
    entity_description: EcowaterSensorEntityDescription

    def __init__(
        self,
        coordinator: EcowaterDataCoordinator,
        description: EcowaterSensorEntityDescription,
        serialnumber
    ) -> None:
        """Initialize the ecowater sensor."""
        super().__init__(coordinator)
        self.entity_description = description

        self._serialnumber = serialnumber

        self._attr_unique_id = "ecowater_" + serialnumber.lower() + "_" + self.entity_description.key
        self._attr_native_value = getattr(self.coordinator.data, self.entity_description.key)

    @property
    def native_unit_of_measurement(self) -> StateType:
        if self.entity_description.native_unit_of_measurement != None:
            return self.entity_description.native_unit_of_measurement

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = getattr(self.coordinator.data, self.entity_description.key)
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
