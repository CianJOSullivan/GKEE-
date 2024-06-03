import json

class ValveLogic:
    def __init__(self, json_file):
        # Load the valve data from the JSON file
        with open(json_file) as f:
            self.valve_data = json.load(f)["Valves"][0]  # Access the dictionary within the list


    def get_current_state(self, locations, selected_states):
        current_state = {}
        for valve_name in locations:
            if selected_states[valve_name][0]:
                for i in range(2, 5):
                    if selected_states[valve_name][i]:
                        current_state[valve_name] = f"green-{i-1}"
            elif selected_states[valve_name][1]:
                current_state[valve_name] = "cylinder"
            else:
                for i in range(2, 5):
                    if selected_states[valve_name][i]:
                        current_state[valve_name] = str(i - 1)
                        break
        return current_state
    

    def find_optimal_solution(self, current_state):
        green_location = None
        cylinder_location = None

        for location, state in current_state.items():
            if "green" in state:
                green_location = location
            if state == "cylinder":
                cylinder_location = location

        max_matches = -1
        best_output = None

        for option_key in ["option_1", "option_2"]:
            option_data = self.valve_data[green_location][option_key]
            option_matches = 0

            for key, values in option_data.items():
                if key == f"cylinder_{cylinder_location}":
                    for location in current_state:
                        if str(current_state[location]) == str(values[location]):
                            option_matches += 1

                    if option_matches > max_matches:
                        max_matches = option_matches
                        best_output = values

        return best_output
    

    def get_changes_required(self, current_state, best_output):
        changes_required = {}
        for valve_name, value in best_output.items():
            current_value = current_state.get(valve_name)
            # Remove the "green-" prefix if present in the current state
            if isinstance(current_value, str) and current_value.startswith("green-"):
                current_value = current_value.split("-")[1]
            # Convert string values to integers if necessary
            if isinstance(current_value, str) and current_value.isdigit():
                current_value = int(current_value)
            # Check if the values are different
            if current_value != value:
                changes_required[valve_name] = value
        return changes_required
        

    def return_optimal_solution(self, locations, selected_states):
        # Check for optimal solution if a green light is turned on
        current_state = self.get_current_state(locations, selected_states)
        if any("green" in value for value in current_state.values()):
            best_output = self.find_optimal_solution(current_state)
            if best_output:
                changes_required = self.get_changes_required(current_state, best_output)
                results = []
                for valve_name, value in changes_required.items():
                    results.append(f"{valve_name} -> {value}")
                return results
        return []
        


    




