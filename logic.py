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



class GobbleGums:
    def __init__(self):
        self.Abh = True
        self.Nukes = True
        self.Extra_Credit = True
        self.Idle_Eyes = True
        self.Reign_Drops = True
        self.Shopping_Free = True
        self.gobblegums = [self.Abh, self.Nukes, self.Extra_Credit, self.Idle_Eyes, self.Reign_Drops, self.Shopping_Free]

    def return_results(self):
        self.gobblegums = [self.Abh, self.Nukes, self.Extra_Credit, self.Idle_Eyes, self.Reign_Drops, self.Shopping_Free]
        if not any(self.gobblegums):
            for i in range(len(self.gobblegums)):
                self.gobblegums[i] = True
        return self.gobblegums 
    
    def remove_gobblegum(self, gobblegum):
        if gobblegum == "Abh":
            self.Abh = False
        elif gobblegum == "Nukes":
            self.Nukes = False
        elif gobblegum == "Extra_Credit":
            self.Extra_Credit = False
        elif gobblegum == "Idle_Eyes":
            self.Idle_Eyes = False
        elif gobblegum == "Reign_Drops":
            self.Reign_Drops = False
        elif gobblegum == "Shopping_Free":
            self.Shopping_Free = False
        self.gobblegums = [self.Abh, self.Nukes, self.Extra_Credit, self.Idle_Eyes, self.Reign_Drops, self.Shopping_Free]
        return self.gobblegums
    

