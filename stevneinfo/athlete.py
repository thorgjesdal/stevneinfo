class Athlete:
    def __init__(self, firstname, lastname, gender, dob, team):
        self.firstname   = firstname
        self.lastname    = lastname
        self.gender      = gender
        self.dateofbirth = dob
        self.team        = team

    def __str__(self):
        return f"{self.firstname} {self.lastname} {self.gender} {self.dateofbirth} {self.team} "

