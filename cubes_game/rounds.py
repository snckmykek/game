# Rounds / Levels
class SingleRound:

    def __init__(self):
        self.name = '0'
        self.cols = 5
        self.rows = 5
        self.swipes = 20
        self.colors = 4
        self.text_round = ''


# Zero round
zero_round = SingleRound()
zero_round.name = '0'
zero_round.swipes = 10
zero_round.colors = 3
zero_round.text_round = 'Нулевой уровень. Необходимо собирать одинаковые цвета минимум по три в ряд. При ' \
                         'взрыве, на соседних кубах появляются и увеличиваются бонусы, максимум 5. При ' \
                         'взрыве кубов, очки считаются по одному за каждый взорванный + количество ' \
                         'бонусов на кубе. 3 цвета'

# First round
first_round = SingleRound()
first_round.name = '1'
first_round.swipes = 10
first_round.colors = 3
first_round.cols = 4
first_round.rows = 4
first_round.text_round = 'Первый уровень. В зависимости от уровня, количество столбцов и колонок может меняться.'

# Second round
second_round = SingleRound()
second_round.name = '2'
second_round.swipes = 20
second_round.colors = 4
second_round.text_round = 'Второй уровень. 4 цвета'

# Third round
third_round = SingleRound()
third_round.name = '3'
third_round.swipes = 40
third_round.colors = 5
third_round.text_round = 'Третий уровень. 5 цветов'

# Fourth round
fourth_round = SingleRound()
fourth_round.name = '4'
fourth_round.swipes = 20
fourth_round.colors = 2
fourth_round.text_round = 'Четвертый уровень - бонусный, всего 2 цвета.'

# Fifth round
fifth_round = SingleRound()
fifth_round.name = '5'
fifth_round.swipes = 30
fifth_round.colors = 4
fifth_round.cols = 8
fifth_round.rows = 8
fifth_round.text_round = 'Пятый уровень. Большое поле - большие возможности.'

# Sixth round
sixth_round = SingleRound()
sixth_round.name = '6'
sixth_round.swipes = 30
sixth_round.colors = 3
sixth_round.cols = 4
sixth_round.rows = 6
sixth_round.text_round = 'Шестой уровень. Поле не всегда может быть квадратным.'

rounds = [zero_round, first_round, second_round, third_round, fourth_round, fifth_round, sixth_round]
