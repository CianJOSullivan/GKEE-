# add valve logic here


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
    

