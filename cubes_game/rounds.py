# Rounds / Levels
class SingleRound:

    def __init__(self):
        self.cols = 5
        self.rows = 5
        self.swipes = 20
        self.colors = 4


# First round
first_round = SingleRound()
first_round.swipes = 10
first_round.colors = 3

# Second round
second_round = SingleRound()
second_round.swipes = 12
second_round.colors = 4

# Third round
third_round = SingleRound()
third_round.swipes = 20
third_round.colors = 2

rounds = [first_round, second_round, third_round]
