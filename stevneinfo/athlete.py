class Athlete:
    def __init__(self, fn, ln, dob, team):
        self.FirstName   = fn
        self.LastName    = ln
        self.DateOfBirth = dob
        self.Team        = team

    def __str__(self):
        return f"{self.FirstName} {self.LastName} {self.dateOfBirth} {self.Team} "

