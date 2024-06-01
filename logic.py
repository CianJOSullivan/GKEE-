import json

class ValveLogic:
    def __init__(self, json_file):
        # Load the valve data from the JSON file
        with open(json_file) as f:
            self.valve_data = json.load(f)["Valves"][0]  # Access the dictionary within the list

    def find_optimal_solution(self, current_state):
        """
        Find the most optimal solution based on the current state of the valves.
        """
        green_location = None
        cylinder_location = None

        # Identify the green location and the cylinder location
        for location, state in current_state.items():
            if "green" in state:
                green_location = location
                green_number = state.split('-')[1]
            if state == "cylinder":
                cylinder_location = location

        best_option = None
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
                        best_option = option_key
                        best_output = values

        return best_option, best_output

    




