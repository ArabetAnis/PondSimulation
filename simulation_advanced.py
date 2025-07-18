import time
import random
import datetime
import os

# --- ANSI Color Codes for Terminal Output ---
class Colors:
    RESET = '\033[0m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    CYAN = '\033[96m'

# --- Configuration ---
# Each sensor now includes 'safe_range' and 'critical_range' for the alerting system.
SENSORS_CONFIG = {
    "pH": {
        "value": 7.8, "fluctuation": 0.05, "min_val": 6.0, "max_val": 9.5, "unit": "",
        "battery": 100.0, "drain_rate": 0.1, "format": "{:<15.2f}",
        "safe_range": (7.0, 8.5), "critical_range": (6.5, 9.0)
    },
    "Salinity": {
        "value": 0.5, "fluctuation": 0.02, "min_val": 0, "max_val": 10, "unit": "ppt",
        "battery": 100.0, "drain_rate": 0.08, "format": "{:<15.2f}",
        "safe_range": (0, 2.0), "critical_range": (0, 4.0)
    },
    "Suspended Solids": {
        "value": 25, "fluctuation": 2, "min_val": 0, "max_val": 200, "unit": "mg/L",
        "battery": 100.0, "drain_rate": 0.12, "format": "{:<15.2f}",
        "safe_range": (0, 50), "critical_range": (0, 80)
    },
    "Nitrite (NO2)": {
        "value": 0.1, "fluctuation": 0.01, "min_val": 0, "max_val": 5, "unit": "mg/L",
        "battery": 100.0, "drain_rate": 0.15, "format": "{:<15.4f}",
        "safe_range": (0, 0.5), "critical_range": (0, 1.0)
    },
    "Nitrate (NO3)": {
        "value": 20, "fluctuation": 1, "min_val": 0, "max_val": 100, "unit": "mg/L",
        "battery": 100.0, "drain_rate": 0.15, "format": "{:<15.2f}",
        "safe_range": (0, 40), "critical_range": (0, 80)
    },
    "Ammonia (NH3)": {
        "value": 0.05, "fluctuation": 0.01, "min_val": 0, "max_val": 2, "unit": "mg/L",
        "battery": 100.0, "drain_rate": 0.15, "format": "{:<15.4f}",
        "safe_range": (0, 0.1), "critical_range": (0, 0.25)
    },
    "Water Level": {
        "value": 4.5, "fluctuation": 0.01, "min_val": 1.0, "max_val": 5.0, "unit": "m",
        "battery": 100.0, "drain_rate": 0.05, "format": "{:<15.2f}",
        "safe_range": (3.0, 4.8), "critical_range": (2.0, 4.9)
    }
}

# --- Event Simulation Functions ---

def simulate_feeding(sensors):
    """Simulates the effect of feeding fish: increases Ammonia and Suspended Solids."""
    print(f"{Colors.CYAN}EVENT: Simulating fish feeding...{Colors.RESET}")
    # Increase Ammonia due to waste
    sensors["Ammonia (NH3)"]["value"] += random.uniform(0.1, 0.25)
    # Increase Suspended Solids due to uneaten food and activity
    sensors["Suspended Solids"]["value"] += random.uniform(20, 40)
    return "Fish have been fed. Ammonia and Solids increased."

def simulate_rainfall(sensors):
    """Simulates heavy rainfall: increases water level and dilutes chemicals."""
    print(f"{Colors.CYAN}EVENT: Simulating heavy rainfall...{Colors.RESET}")
    rain_mm = random.uniform(20, 50) # rainfall in mm
    water_increase_m = rain_mm / 1000.0
    
    current_level = sensors["Water Level"]["value"]
    new_level = current_level + water_increase_m
    sensors["Water Level"]["value"] = new_level
    
    # Calculate dilution factor
    dilution_factor = current_level / new_level
    
    # Apply dilution
    sensors["Salinity"]["value"] *= dilution_factor
    sensors["Nitrite (NO2)"]["value"] *= dilution_factor
    sensors["Nitrate (NO3)"]["value"] *= dilution_factor
    sensors["Ammonia (NH3)"]["value"] *= dilution_factor
    
    return f"Heavy rain ({rain_mm:.1f}mm). Water level rose, chemicals diluted."


# --- Core Logic ---

def update_sensor(sensor_data):
    """Simulates a natural reading for a single sensor and drains its battery."""
    if sensor_data["battery"] <= 0:
        return

    # Update value with natural fluctuation
    fluctuation = sensor_data["fluctuation"]
    change = random.uniform(-fluctuation, fluctuation)
    sensor_data["value"] += change
    sensor_data["value"] = max(sensor_data["min_val"], min(sensor_data["max_val"], sensor_data["value"]))

    # Drain battery
    drain = sensor_data["drain_rate"] + random.uniform(-0.005, 0.005)
    sensor_data["battery"] = max(0, sensor_data["battery"] - drain)

def check_status(sensor_data):
    """Checks a sensor's value against its ranges and returns a colored status."""
    if sensor_data["battery"] <= 0:
        return f"{Colors.RED}OFFLINE{Colors.RESET}"
    
    val = sensor_data["value"]
    crit_min, crit_max = sensor_data["critical_range"]
    safe_min, safe_max = sensor_data["safe_range"]
    
    if not (crit_min <= val <= crit_max):
        return f"{Colors.RED}CRITICAL{Colors.RESET}"
    if not (safe_min <= val <= safe_max):
        return f"{Colors.YELLOW}WARNING{Colors.RESET}"
    return f"{Colors.GREEN}OK{Colors.RESET}"

# --- Main Simulation Loop ---

def run_simulation():
    """Starts the interactive fish pond sensor simulation."""
    sensors = SENSORS_CONFIG
    last_message = "Simulation started."

    try:
        while True:
            # Clear console for a clean display
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print("--- Interactive Fish Farming Pond Simulation ---")
            
            # Update every sensor
            active_sensors = sum(1 for data in sensors.values() if data["battery"] > 0)
            for data in sensors.values():
                update_sensor(data)
            
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Display readings table
            print(f"--- Timestamp: {timestamp} ---")
            print(f"| {'Parameter':<20} | {'Value':<15} | {'Battery':<10} | {'Status':<18} | {'Unit':<10} |")
            print(f"|{'-'*22}|{'-'*17}|{'-'*12}|{'-'*20}|{'-'*12}|")

            for name, data in sensors.items():
                status_str = check_status(data)
                if data["battery"] > 0:
                    value_str = data["format"].format(data["value"])
                    battery_str = f"{data['battery']:.1f}%"
                else:
                    value_str = "---".ljust(15)
                    battery_str = "0.0%"

                print(f"| {name:<20} | {value_str} | {battery_str:<10} | {status_str:<10} | {data['unit']:<10} |")
            
            print("-" * 88)
            print(f"Last Event: {last_message}\n")

            if active_sensors == 0:
                print("--- ALL SENSOR BATTERIES DEPLETED. SIMULATION ENDED. ---")
                break

            # Interactive Controls
            print("CONTROLS: [f]eed fish | [r]ainfall | [q]uit | Press [Enter] to advance time")
            choice = input("Your choice: ").lower()

            if choice == 'f':
                last_message = simulate_feeding(sensors)
            elif choice == 'r':
                last_message = simulate_rainfall(sensors)
            elif choice == 'q':
                break
            else:
                last_message = "Time advanced normally."
                
    except KeyboardInterrupt:
        print("\n--- Simulation stopped by user. ---")

if __name__ == "__main__":
    run_simulation()
