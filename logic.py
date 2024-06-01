# add valve logic here
class ValveLogic:
    def __init__(self, json_data):
        self.valve_data = json_data  # Store the valve data from the JSON file

    def update_valve_state(self, user_input):
        # Parse the user input
        dept = user_input.get("DEPT", None)
        dragon = user_input.get("DRAGON", None)
        arm = user_input.get("ARM", None)
        supply = user_input.get("SUPPLY", None)
        inf = user_input.get("INF", None)
        tank = user_input.get("TANK", None)

        # Initialize an empty list to store the valve states
        valve_states = []

        # Look up valve states based on user input
        if dept is not None:
            valve_states.append(self.valve_data["Valves"]["DEPT"][f"option_{dept}"])
        if dragon is not None:
            valve_states.append(self.valve_data["Valves"]["DRAGON"][f"option_{dragon}"])
        if arm is not None:
            valve_states.append(self.valve_data["Valves"]["ARM"][f"option_{int(arm)}"])
        if supply is not None:
            valve_states.append(self.valve_data["Valves"]["SUPPLY"][f"option_{supply}"])
        if inf is not None:
            valve_states.append(self.valve_data["Valves"]["INF"][f"option_{inf}"])
        if tank is not None:
            valve_states.append(self.valve_data["Valves"]["TANK"][f"option_{tank}"])

        return valve_states





