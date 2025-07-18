import time
import random
import datetime

# --- Configuration ---
# Each sensor is now a dictionary containing its specific parameters,
# including its own battery and drain rate.

SENSORS_CONFIG = {
    "pH": {
        "value": 7.8,
        "fluctuation": 0.1,
        "min_val": 6.0,
        "max_val": 9.5,
        "unit": "",
        "battery": 100.0,
        "drain_rate": 0.1, # Percent per reading
        "format": "{:<15.2f}"
    },
    "Salinity": {
        "value": 0.5,
        "fluctuation": 0.05,
        "min_val": 0,
        "max_val": 10, # Arbitrary max
        "unit": "ppt",
        "battery": 100.0,
        "drain_rate": 0.08,
        "format": "{:<15.2f}"
    },
    "Suspended Solids": {
        "value": 25,
        "fluctuation": 5,
        "min_val": 0,
        "max_val": 200, # Arbitrary max
        "unit": "mg/L",
        "battery": 100.0,
        "drain_rate": 0.12,
        "format": "{:<15.2f}"
    },
    "Nitrite (NO2)": {
        "value": 0.1,
        "fluctuation": 0.02,
        "min_val": 0,
        "max_val": 5, # Arbitrary max
        "unit": "mg/L",
        "battery": 100.0,
        "drain_rate": 0.15,
        "format": "{:<15.4f}"
    },
    "Nitrate (NO3)": {
        "value": 20,
        "fluctuation": 2,
        "min_val": 0,
        "max_val": 100, # Arbitrary max
        "unit": "mg/L",
        "battery": 100.0,
        "drain_rate": 0.15,
        "format": "{:<15.2f}"
    },
    "Ammonia (NH3)": {
        "value": 0.05,
        "fluctuation": 0.01,
        "min_val": 0,
        "max_val": 2, # Arbitrary max
        "unit": "mg/L",
        "battery": 100.0,
        "drain_rate": 0.15,
        "format": "{:<15.4f}"
    },
    "Water Level": {
        "value": 4.5,
        "fluctuation": 0.05,
        "min_val": 1.0,
        "max_val": 5.0,
        "unit": "m",
        "battery": 100.0,
        "drain_rate": 0.05, # This sensor might use less power
        "format": "{:<15.2f}"
    }
}

# Simulation Parameters
SIMULATION_INTERVAL_SECONDS = 5 # Time between sensor readings

# --- Generic Sensor Update Function ---

def update_sensor(sensor_data):
    """
    Simulates a reading for a single sensor, updating its value and draining its battery.
    """
    # If battery is dead, do nothing.
    if sensor_data["battery"] <= 0:
        return

    # 1. Update the sensor's value
    fluctuation = sensor_data["fluctuation"]
    change = random.uniform(-fluctuation, fluctuation)
    new_value = sensor_data["value"] + change
    
    # Enforce min/max limits for the sensor's value
    sensor_data["value"] = max(sensor_data["min_val"], min(sensor_data["max_val"], new_value))

    # 2. Drain the battery
    drain = sensor_data["drain_rate"] + random.uniform(-0.01, 0.01) # Add slight randomness to drain
    new_battery_level = sensor_data["battery"] - drain
    sensor_data["battery"] = max(0, new_battery_level) # Battery can't go below 0


# --- Main Simulation Loop ---

def run_simulation():
    """Starts the fish pond sensor simulation."""
    print("--- Starting Fish Farming Pond Sensor Simulation (Individual Batteries) ---")
    print("Press CTRL+C to stop the simulation.\n")

    # The SENSORS_CONFIG dictionary will now hold the state for all sensors
    sensors = SENSORS_CONFIG

    try:
        while True:
            # Update every sensor in our configuration
            active_sensors = 0
            for sensor_name in sensors:
                update_sensor(sensors[sensor_name])
                if sensors[sensor_name]["battery"] > 0:
                    active_sensors += 1
            
            # Get current timestamp
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # --- Display the readings in a formatted table ---
            print(f"--- Timestamp: {timestamp} ---")
            print(f"| {'Parameter':<20} | {'Value':<15} | {'Battery':<10} | {'Unit':<10} |")
            print(f"|{'-'*22}|{'-'*17}|{'-'*12}|{'-'*12}|")

            for name, data in sensors.items():
                if data["battery"] > 0:
                    value_str = data["format"].format(data["value"])
                    battery_str = f"{data['battery']:.1f}%"
                else:
                    value_str = "--- OFFLINE ---".ljust(15)
                    battery_str = "0.0%"

                print(f"| {name:<20} | {value_str} | {battery_str:<10} | {data['unit']:<10} |")
            
            print("-" * 68 + "\n")

            # If all sensors are offline, end the simulation
            if active_sensors == 0:
                print("--- ALL SENSOR BATTERIES DEPLETED. SIMULATION ENDED. ---")
                break

            # Wait for the next interval
            time.sleep(SIMULATION_INTERVAL_SECONDS)

    except KeyboardInterrupt:
        print("\n--- Simulation stopped by user. ---")

if __name__ == "__main__":
    run_simulation()
