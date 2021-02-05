


# class Player:
#     def __init__(self, role, location, player_number):
#         self.role = role
#         self.location = location
#         # self.abilities = ""
#         self.supplies_on_card = 0
#         self.player_number = player_number


class bladiblpe():
    def __init__(self, Board):

        self.NumberOfCards = 36
        self.infection_deck = []
        self.drawed_infection_deck = []
        self.player_deck = []
        self.removed_player_deck = []
        self.stockpile = 36
        self.incidents = 0
        self.infection_grade_mapping = {0: 2, 1: 2, 2: 3, 3: 3, 4: 4, 5: 4}
        self.infection_grade_loc = 0
        self.infection_grade = self.infection_grade_mapping[self.infection_grade_loc]
        self.turn_of_player = turn_of_player