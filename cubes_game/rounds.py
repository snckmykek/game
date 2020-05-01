# Rounds / Levels
class SingleRound:

    def __init__(self):
        self.name = '0'
        self.cols = 5
        self.rows = 5
        self.time = -1
        self.swipes = 20
        self.colors = 4
        self.text_round = ''
        self.single_star_diamonds = 0
        self.two_star_diamonds = 0
        self.three_star_diamonds = 0


# Zero round
zero_round = SingleRound()
zero_round.name = '0'
zero_round.swipes = 10
zero_round.colors = 3
zero_round.text_round = ''
zero_round.time = 10

# First round
first_round = SingleRound()
first_round.name = '1'
first_round.swipes = 10
first_round.colors = 3
first_round.text_round = ''

# Second round
second_round = SingleRound()
second_round.name = '2'
second_round.swipes = 20
second_round.colors = 3
second_round.cols = 3
second_round.rows = 3
second_round.text_round = ''

# Third round
third_round = SingleRound()
third_round.name = '3'
third_round.swipes = 20
third_round.colors = 5
third_round.text_round = ''

# Fourth round
fourth_round = SingleRound()
fourth_round.name = '4'
fourth_round.swipes = 5
fourth_round.colors = 2
fourth_round.text_round = ''

# Fifth round
fifth_round = SingleRound()
fifth_round.name = '5'
fifth_round.swipes = 20
fifth_round.colors = 4
fifth_round.cols = 8
fifth_round.rows = 8
fifth_round.text_round = ''

# Sixth round
sixth_round = SingleRound()
sixth_round.name = '6'
sixth_round.swipes = 30
sixth_round.colors = 4
sixth_round.cols = 4
sixth_round.rows = 6
sixth_round.text_round = ''

rounds = [zero_round, first_round, second_round, third_round, fourth_round, fifth_round, sixth_round]
