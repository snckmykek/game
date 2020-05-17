from kivy.animation import Animation
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
from kivy.clock import Clock
from global_variables import WINDOW
from sqlite_requests import db
from store import store
from cubes_game.animatoins import do_animation

from dialog.main import dialog

import math
import random

Builder.load_file(r'cubes_game/main.kv')


class CubesGame(ModalView):
    time: NumericProperty(0.0)
    task_counter: NumericProperty(0)
    mega_task_counter: NumericProperty(0)

    def __init__(self, **kwargs):
        super(CubesGame, self).__init__(**kwargs)

        self.ge = GameEnding()
        self.dialog = dialog
        self.store = store

        self.world_map = ObjectProperty
        self.current_level = ObjectProperty
        self.current_location = ObjectProperty
        self.cols = 4  # Колонки
        self.rows = 4  # Столбцы
        self.swipes = 20  # Количество ходов
        self.level_swipes = 20  # Это число не меняется в процессе игры (только при запуске) и при перезапуске используется
        self.task_name = 'break_stone_color'  # 'get_prize', 'break_stone'
        self.mega_task_name = 'combo'

        self.a = WINDOW.width / (self.cols + 1)
        self.score = 0
        self.score_label = self.ids.score_label
        self.swipes_label = self.ids.swipes_label
        self.update_status_board()
        self.playing_field = self.ids.playing_field
        self.ids.rl.size = (self.a * self.cols, self.a * self.rows)
        self.cube_pattern = 'images/patterns/square'
        self.ids.character.skills = self.ids.skills
        self.ids.character.cubes_game = self
        self.scores_for_stars = list()
        self.game_is_active = False

        self.objects = list()
        self.background_objects = list()
        self.prizes = list()
        self.x_movement_blocked = False
        self.y_movement_blocked = False
        self.active_column = list()
        self.active_line = list()
        self.touch_start = (0, 0)
        self.touch_blocked = False
        self.touch_is_down = False
        self.forced_up = False
        self.starting_point = None  # Чтобы знать, откуда начал двигать, и если чо, вернуться обратно
        self.combo = 0
        self.statistics = dict()
        self.colors_bonuses = dict()  # {(1, 0, 0, 1): 5, color: bonus, ...}
        self.cube_colors = list()  # [(1, 0, 0, 1), (r, g, b, a), ...]

    def go_clock(self, dt):
        if self.current_level.time == -1:  # Если игра не на время
            return

        if self.game_is_active:
            self.time -= dt
            if self.time <= 0:
                self.time = 0
                self.end_game()
                return
        Clock.schedule_once(self.go_clock, 0.01)

    def on_open(self):
        self.open_dialog()

    def open_dialog(self):
        self.dialog.location = self.current_location.loc_id
        self.dialog.level = self.current_level.lvl_id

        if self.dialog.dialog_is_completed() or self.dialog.current_npc_speech == 'stub' or self.dialog.current_npc_speech == (
                '', ''):
            return

        self.dialog.open()

    def open_shop(self):
        self.store.open()

    def on_pre_dismiss(self):
        self.world_map.open_location(self.current_location)

    def on_dismiss(self):
        pass
        # self.open_dialog()

    def end_game(self, *l):
        self.ge.game = self
        self.ge.open()

    def down(self, instance, touch):
        if self.touch_blocked:
            return

        if not instance.collide_point(*touch.pos):
            return

        if self.process_skill(instance):  # Проверяет есть ли активированный бонус, если есть, работает с ним
            return

        self.active_column.clear()
        self.active_line.clear()
        for cube in self.objects:
            if cube.column == instance.column:
                self.active_column.append(cube)
            if cube.line == instance.line:
                self.active_line.append(cube)

        self.touch_start = touch.ppos

        self.touch_is_down = True
        self.forced_up = False

        if not self.starting_point:
            self.starting_point = StartingPoint()
            self.starting_point.pos = [s - self.starting_point.width / 2 for s in touch.pos]
            self.playing_field.add_widget(self.starting_point)

    def up(self, instance, touch):
        if self.touch_blocked:
            return

        if not instance.collide_point(*touch.pos):
            return

        if self.starting_point:
            self.playing_field.remove_widget(self.starting_point)
            self.starting_point = None

        if ((abs(touch.pos[0] - self.touch_start[0]) > instance.width / 2) and self.y_movement_blocked) \
                or ((abs(touch.pos[1] - self.touch_start[1]) > instance.width / 2) and self.x_movement_blocked):
            if self.touch_is_down and not self.touch_blocked:
                self.swipes -= 1
        self.touch_is_down = False

        if self.y_movement_blocked or self.x_movement_blocked \
                or (not self.playing_field.collide_point(*touch.pos) and not self.forced_up):
            self.forced_up = True
            self._move_line(instance, touch)
            self.x_movement_blocked = False
            self.y_movement_blocked = False

    def _move_line(self, instance, touch, *l):

        animation = Animation(d=0.1, pos=(0, 0))

        self.touch_blocked = True
        # Запускается анимация на перемещение по нужным координатам для всех кубов в строке или колонке
        is_leveling_up = None  # Эта наркомания обусловлена тем, что бывает подвисают координаты кнопок
        # и соседние кнопки разъезжаются в разные стороны
        if self.y_movement_blocked:
            for but in self.active_line:
                if is_leveling_up is None:
                    is_leveling_up = round(but.pos[0] / but.width) == math.ceil(but.pos[0] / but.width)
                but.column = math.ceil(but.pos[0] / but.width) if is_leveling_up else math.floor(but.pos[0] / but.width)
                animation.animated_properties['pos'] = (but.column * but.width, but.pos[1])
                animation.start(but)
        elif self.x_movement_blocked:
            for but in self.active_column:
                if is_leveling_up is None:
                    is_leveling_up = round(but.pos[1] / but.height) == math.ceil(but.pos[1] / but.height)
                but.line = math.ceil(but.pos[1] / but.height) if is_leveling_up else math.floor(but.pos[1] / but.height)
                animation.animated_properties['pos'] = (but.pos[0], but.line * but.height)
                animation.start(but)
        Clock.schedule_once(self.boom, .25)

    def boom(self, instance=None, *l):

        self.combo += 1
        self.game_is_active = True

        suicidal_cubes = list()

        for obj in self.objects:
            obj_prev_x = None
            obj_next_x = None
            obj_prev_y = None
            obj_next_y = None
            for o in self.objects:
                if o.line == obj.line:
                    if o.column == obj.column - 1:
                        obj_prev_x = o
                    if o.column == obj.column + 1:
                        obj_next_x = o
                if o.column == obj.column:
                    if o.line == obj.line - 1:
                        obj_prev_y = o
                    if o.line == obj.line + 1:
                        obj_next_y = o

            if obj_prev_x and obj_next_x:
                if (obj.background_color == obj_prev_x.background_color) \
                        and (obj.background_color == obj_next_x.background_color):
                    suicidal_cubes.extend([obj, obj_prev_x, obj_next_x])
            if obj_prev_y and obj_next_y:
                if (obj.background_color == obj_prev_y.background_color) \
                        and (obj.background_color == obj_next_y.background_color):
                    suicidal_cubes.extend([obj, obj_prev_y, obj_next_y])

        self.touch_blocked = True

        if self.combo > 1 and set(suicidal_cubes):
            self.statistics['combo'] += 1
            do_animation('combo', self.ids.combo)

        for cube in set(suicidal_cubes):
            self.statistics[tuple(cube.background_color)] += 1

            self.score += 1 + (int(cube.text) if cube.text != '' else 0) \
                + self.colors_bonuses[tuple(cube.background_color)]

            cube.text = ''
            do_animation('decrease', cube, random.choice(self.cube_colors))

        copy_background_objects = self.background_objects.copy()
        for background_obj in copy_background_objects:
            for cube in set(suicidal_cubes):
                if (background_obj.column == cube.column) and (background_obj.line == cube.line):
                    self.background_objects.remove(background_obj)
                    self.playing_field.remove_widget(background_obj)

        copy_prizes = self.prizes.copy()
        for prize in copy_prizes:
            take_prize = True
            for background_obj in self.background_objects:
                if (background_obj.column in prize.column) and (background_obj.line in prize.line):
                    take_prize = False
            if take_prize:
                self.playing_field.remove_widget(prize)
                self.ids.rl.add_widget(prize)
                self.prizes.remove(prize)
                animation = Animation(size=(prize.size[0] * 1.2, prize.size[1] * 1.2), d=.4)
                animation += Animation(size=prize.size, d=.4)
                animation += Animation(size=(10, 10), d=.8)
                animation &= Animation(pos=(self.ids.bonus_1.center_x, self.ids.bonus_1.center_y), d=1.3)
                animation.bind(on_complete=self.delete_prize)
                animation.start(prize)

        if set(suicidal_cubes):
            Clock.schedule_once(self.boom, .8)
        else:
            self.combo = 0
            self.touch_blocked = False
            if self.swipes <= 0:
                Clock.schedule_once(self.end_game, .3)

        for boosted_cube in self.get_boosted_cube(set(suicidal_cubes)):
            if boosted_cube.text != '':
                if int(boosted_cube.text) == 3:
                    continue
                boosted_cube.text = str(int(boosted_cube.text) + 1)
            else:
                boosted_cube.text = str(1)

        self.update_status_board()

    def delete_prize(self, animation, instance):
        self.ids.rl.remove_widget(instance)

    def get_boosted_cube(self, cubes):
        boosted_cubes = list()
        for obj in cubes:
            for o in self.objects:
                if o.line == obj.line:
                    if o.column == obj.column - 1:
                        boosted_cubes.append(o)
                    if o.column == obj.column + 1:
                        boosted_cubes.append(o)
                if o.column == obj.column:
                    if o.line == obj.line - 1:
                        boosted_cubes.append(o)
                    if o.line == obj.line + 1:
                        boosted_cubes.append(o)

        return set(boosted_cubes) - cubes

    def update_status_board(self):
        self.score_label.text = str(self.score)
        self.swipes_label.text = str(self.swipes)
        self.ids.progress.value = self.score

        try:
            if self.task_name == 'break_stone_color':
                self.task_counter = self.current_level.task_counter - self.statistics[tuple(self.ids.task_label.background_color)]

            if self.mega_task_name == 'break_stone_color':
                self.mega_task_counter = self.current_level.mega_task_counter \
                                      - self.statistics[tuple(self.ids.mega_task_label.background_color)]
            elif self.mega_task_name == 'combo':
                self.mega_task_counter = self.current_level.mega_task_counter - self.statistics['combo']

        except AttributeError:
            pass

        if self.task_counter < 0:
            self.task_counter = 0

        if self.mega_task_counter < 0:
            self.mega_task_counter = 0

    def movement(self, instance, touch):
        if self.touch_blocked or not self.touch_is_down:
            return

        if not self.playing_field.collide_point(*touch.pos):
            self.up(instance, touch)
            return

        if (abs(touch.dx) > abs(touch.dy)) or self.y_movement_blocked:
            if (instance in self.active_line) and not self.x_movement_blocked:
                self.y_movement_blocked = True
                for but in self.active_line:
                    new_pos_x = (touch.pos[0] - self.touch_start[0]) + but.column * but.width
                    if new_pos_x > self.cols * but.width - but.width / 2:
                        new_pos_x -= self.cols * but.width
                    elif new_pos_x < - but.width / 2:
                        new_pos_x += self.cols * but.width
                    but.pos[0] = new_pos_x

        if (abs(touch.dx) < abs(touch.dy)) or self.x_movement_blocked:
            if (instance in self.active_column) and not self.y_movement_blocked:
                self.x_movement_blocked = True
                for but in self.active_column:
                    new_pos_y = (touch.pos[1] - self.touch_start[1]) + but.line * but.height
                    if new_pos_y > self.rows * but.height - but.height / 2:
                        new_pos_y -= self.rows * but.height
                    elif new_pos_y < - but.height / 2:
                        new_pos_y += self.rows * but.height
                    but.pos[1] = new_pos_y

    def process_skill(self, instance):

        active_skills = [s.ids.skill for s in self.ids.skills.children if s.ids.skill.state == 'down']
        if not active_skills:
            return False
        else:
            active_skill = active_skills[0]

        active_skill.skill_is_activated()  # Уменьшает количество на 1

        suicidal_cubes = list()
        suicidal_cubes.append(instance)
        for o in self.objects:
            if active_skill.name == 'bomb_1':
                break
            elif active_skill.name == 'bomb_2':
                if o.line == instance.line:
                    if (o.column == instance.column - 1) or (o.column == instance.column + 1):
                        suicidal_cubes.append(o)
            elif active_skill.name == 'bomb_3':
                if o.column == instance.column:
                    if (o.line == instance.line - 1) or (o.line == instance.line + 1):
                        suicidal_cubes.append(o)
            elif active_skill.name == 'bomb_4':
                if o.line == instance.line:
                    if (o.column == instance.column - 1) or (o.column == instance.column + 1):
                        suicidal_cubes.append(o)
                if o.column == instance.column:
                    if (o.line == instance.line - 1) or (o.line == instance.line + 1):
                        suicidal_cubes.append(o)
            elif active_skill.name == 'bomb_5':
                if (o.line == instance.line) or (o.line == instance.line - 1) or (o.line == instance.line + 1):
                    if (o.column == instance.column - 1) or (o.column == instance.column + 1) or (
                            o.column == instance.column):
                        suicidal_cubes.append(o)
            elif active_skill.name == 'destroy_color':
                if o.background_color == instance.background_color:
                    suicidal_cubes.append(o)

        self.touch_blocked = True
        for cube in set(suicidal_cubes):
            self.score += 1 + (int(cube.text) if cube.text != '' else 0)
            cube.text = ''
            do_animation('explosion', cube, random.choice(self.cube_colors))
        Clock.schedule_once(self.boom, .6)

        return True

    def start_game(self, cubes=None):
        self.game_is_active = False
        self.cols = self.current_level.cols
        self.rows = self.current_level.rows
        self.swipes = self.current_level.swipes
        self.colors_bonuses = self.current_level.colors_bonuses
        self.cube_colors = self.current_level.cube_colors
        self.time = self.current_level.time
        self.task_counter = self.current_level.task_counter
        self.mega_task_counter = self.current_level.mega_task_counter
        self.task_name = self.current_level.task_name
        self.mega_task_name = self.current_level.mega_task_name
        self.scores_for_stars = db.get_scores_for_stars(self.current_level.loc_id, self.current_level.lvl_id)
        self.ids.progress.max = max(self.scores_for_stars)
        self.ids.max_score_label.text = str(self.ids.progress.max)
        self.ids.task_label.background_normal = self.current_level.task_image
        self.ids.mega_task_label.background_normal = self.current_level.mega_task_image
        self.a = WINDOW.width / ((self.cols if self.cols >= self.rows else self.rows) + 1)
        self.ids.rl.size = (self.a * self.cols, self.a * self.rows)
        if cubes:
            pass  # stub Прошло 4 месяца и я не ебу зачем эта заглушка долбоеб почему бы не пояснить было тогда??))))00

        if self.task_name == 'break_stone_color':
            self.ids.task_label.background_color = random.choice(self.cube_colors)
        else:
            self.ids.task_label.background_color = (1, 1, 1, 0)

        if self.mega_task_name == 'break_stone_color':
            self.ids.mega_task_label.background_color = random.choice(self.cube_colors)
        elif self.mega_task_name == 'combo':
            self.ids.mega_task_label.background_color = (1, 1, 1, 1)
        else:
            self.ids.task_label.background_color = (1, 1, 1, 0)

        self.statistics.clear()
        self.statistics.update({'combo': 0})
        for color in self.cube_colors:
            self.statistics.update({color: 0})
        for prize in self.prizes:
            self.statistics.update({prize: 0})

        self.score = 0
        self.update_status_board()

        coordinates = list([tuple([x, y]) for x in (range(self.cols))] for y in (range(self.rows)))
        self.objects = list()
        for i, row in enumerate(coordinates):
            for j, coords in enumerate(row):
                button = Cube(size_hint=(None, None), size=(self.a, self.a),
                              pos=list(map(lambda x, y: x * y, coords, (self.a, self.a))),
                              on_touch_move=self.movement, on_touch_down=self.down, on_touch_up=self.up)
                button.background_color = random.choice(self.cube_colors)
                button.pattern = self.cube_pattern
                button.background_down = button.pattern + (button.text if button.text != '' else '0') + '.png'
                button.background_normal = button.pattern + (button.text if button.text != '' else '0') + '.png'
                button.line = i
                button.column = j
                self.objects.append(button)

        self.playing_field.clear_widgets()

        for obj in self.objects:
            self.playing_field.add_widget(obj)

        character = db.get_current_manuscript()
        self.ids.character_level.text = str(character[3])
        self.ids.character.skills.clear_widgets()
        for skill in db.get_skills(character[0]):
            if not skill[5]:  # это параметр скилла is_unblock
                continue
            sk_box = SkillBox()
            sk = sk_box.ids.skill
            sk.name = skill[1]
            sk.background_normal = skill[2]
            sk.skill_level = skill[3]
            sk.quantity = skill[4]
            sk.is_unblock = skill[5]
            sk_box.ids.quantity.text = str(sk.quantity)
            self.ids.character.skills.add_widget(sk_box)

        Clock.schedule_once(self.go_clock, 0.01)


class GameEnding(ModalView):

    def __init__(self, **kwargs):
        super(GameEnding, self).__init__(**kwargs)

        self.score = 0
        self.task_is_completed = False
        self.mega_task_is_completed = False
        self.game = ObjectProperty
        self.auto_dismiss = False
        self.real_prize = {}
        self.current_result = []
        self.is_treasure_hunting = True

    def on_pre_open(self):
        self.score = self.game.score
        self.task_is_completed = (self.game.task_counter == 0)
        self.mega_task_is_completed = (self.game.mega_task_counter == 0)
        self.is_treasure_hunting = self.game.world_map.is_treasure_hunting

        if not self.task_is_completed:
            self.score = 0

        self.ids.lbl.text = 'GG! Your score is: ' + str(self.score)

        self.real_prize = self.get_real_prize()
        self.ids.stars.text = 'Stars: ' + str(self.real_prize['stars'])
        self.ids.exp.text = str(self.real_prize['exp'])
        self.ids.gold.text = str(self.real_prize['gold'])

    def get_real_prize(self):
        self.current_result = list(db.get_current_result(self.game.current_location.loc_id,
                                                         self.game.current_level.lvl_id, self.score))
        self.up_current_result_by_bonuses(self.current_result)
        if self.is_treasure_hunting:
            past_result = db.get_past_result(self.game.current_location.loc_id, self.game.current_level.lvl_id)
        else:
            past_result = [0, 0, 0]  # Сделано, чтобы при работе на шахте всегда платились бабки, а в приключении только первый раз

        real_prize = {
            'stars': self.current_result[0],
            'stars_difference': (self.current_result[0] - past_result[0]) if self.current_result[0] > past_result[0] else 0,
            'exp': (self.current_result[1] - past_result[1]) if self.current_result[1] > past_result[1] else 0,
            'gold': (self.current_result[2] - past_result[2]) if self.current_result[2] > past_result[2] else 0
            }

        return real_prize

    def up_current_result_by_bonuses(self, current_result):
        if self.is_treasure_hunting:
            if self.mega_task_is_completed:  # Добавляет звезду за выполненое доп задание
                current_result[0] += 1

    def play_again(self):
        self.save_result()

        self.game.start_game()
        self.dismiss()

    def exit_level(self):
        self.save_result()

        self.dismiss()
        self.game.dismiss()

    def save_result(self):
        if self.is_treasure_hunting:
            db.set_completed_level(self.game.current_location.loc_id, self.game.current_level.lvl_id)
            if (self.real_prize['exp'] != 0) or (self.real_prize['gold'] != 0):
                db.set_current_result(self.game.current_location.loc_id, self.game.current_level.lvl_id,
                                      self.current_result[1], self.current_result[2], self.current_result[0])

                db.set_manuscript_exp(self.ids.character.name, self.real_prize['exp'])
                db.change_items_qty(self.real_prize['gold'], object_type='gold')
            elif self.real_prize['stars_difference'] != 0:
                db.set_current_result(self.game.current_location.loc_id, self.game.current_level.lvl_id,
                                      self.current_result[1], self.current_result[2], self.current_result[0])
        else:
            db.change_items_qty(self.real_prize['gold'], object_type='gold')

        # делать еще таблицу (или в текущую) и в нее загружать счетчик для количества раз пройденных уровней

        if not self.is_treasure_hunting:
            # stub получить количество пройденных уровней, установить нужное кол-во звезд
            # (не надо проверку, тупо всегда перезапись)
            pass

    def on_dismiss(self):
        self.execute_action()

    def execute_action(self):

        actions = db.get_actions(self.game.current_location.loc_id, self.game.current_level.lvl_id)  # (action_id, action_type, object_id)

        for string in actions:
            if string[1] == 'open_skill':
                db.unblock_skill(string[2])
            elif string[1] == 'open_manuscript':
                db.unblock_manuscript(string[2])

        db.change_actions_completed([x[0] for x in actions])


class Cube(Button):

    def __init__(self, **kwargs):
        super(Cube, self).__init__(**kwargs)

        self.column = 0
        self.line = 0

    def change_pattern(self):
        self.background_down = self.pattern + (self.text if self.text != '' else '0') + '.png'
        self.background_normal = self.pattern + (self.text if self.text != '' else '0') + '.png'


class StartingPoint(Label):

    def __init__(self, **kwargs):
        super(StartingPoint, self).__init__(**kwargs)

        self.size = (WINDOW.width / 20, WINDOW.width / 20)


class Character(Button):

    def __init__(self, **kwargs):
        super(Character, self).__init__(**kwargs)

        self.character_changer = CharacterChanger()
        self.skills = ObjectProperty
        self.cubes_game = ObjectProperty
        character = db.get_current_manuscript()
        self.name = character[0]
        self.background_normal = character[1] if character[6] == '1' else character[2]
        self.available = True if character[6] == '1' else False

    def open_character_changer(self, change_skills=True):
        self.character_changer.change_skills = change_skills
        self.character_changer.character = self
        self.character_changer.cubes_game = self.cubes_game
        self.character_changer.open()


class Character2(Button):

    def __init__(self, **kwargs):
        super(Character2, self).__init__(**kwargs)

        self.character_changer = CharacterChanger()
        self.skills = ObjectProperty
        self.cubes_game = ObjectProperty
        character = db.get_current_manuscript()
        self.name = character[0]
        self.background_normal = character[1] if character[6] == '1' else character[2]
        self.available = True if character[6] == '1' else False

    def open_character_changer(self, change_skills=True):
        self.character_changer.change_skills = change_skills
        self.character_changer.character = self
        self.character_changer.cubes_game = self.cubes_game
        self.character_changer.open()


class CharacterChanger(ModalView):

    def __init__(self, **kwargs):
        super(CharacterChanger, self).__init__(**kwargs)

        self.cubes_game = ObjectProperty
        self.character = ObjectProperty
        self.character_level = ObjectProperty
        self.change_skills = True

    def on_pre_open(self):
        self.ids.character_selection.clear_widgets()
        for ch in db.get_manuscripts():
            but = Button(background_normal=ch[1] if str(ch[6]) == '1' else ch[2], border=[0, 0, 0, 0])
            but.bind(on_press=self.change_character)
            but.background_down = but.background_normal
            but.available = True if str(ch[6]) == '1' else False
            but.level = ch[3]
            but.name = ch[0]
            self.ids.character_selection.add_widget(but)

    def change_character(self, instance):
        if not instance.available:
            return

        if self.cubes_game != ObjectProperty:
            self.character = self.cubes_game.ids.character
            self.character_level = self.cubes_game.ids.character_level

        self.character.name = instance.name
        self.character.background_normal = instance.background_normal
        db.set_current_manuscript(self.character.name)

        if self.change_skills:
            self.character_level.text = str(instance.level)
            self.character.skills.clear_widgets()
            for skill in db.get_skills(instance.name):
                if not skill[5]:  # это параметр скилла is_unblock
                    continue
                sk_box = SkillBox()
                sk = sk_box.ids.skill
                sk.name = skill[1]
                sk.background_normal = skill[2]
                sk.skill_level = skill[3]
                sk.quantity = skill[4]
                sk.is_unblock = skill[5]
                sk_box.ids.quantity.text = str(sk.quantity)
                self.character.skills.add_widget(sk_box)

        self.dismiss()


class SkillBox(BoxLayout):
    def __init__(self, **kwargs):
        super(SkillBox, self).__init__(**kwargs)


class Skill(ToggleButton):

    def __init__(self, **kwargs):
        super(Skill, self).__init__(**kwargs)

        self.skill_id = -1
        self.name = ''
        self.group = 'skills'
        self.skill_level = 1
        self.is_unblock = False

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            self.state = 'normal'

        if self.quantity <= 0:
            return

        return super(Skill, self).on_touch_down(touch)

    def change_color(self):
        self.c = (0, .72, .65, 1) if self.state == 'down' else (.88, .72, .31, 1)

    def skill_is_activated(self):
        self.quantity -= 1
        db.set_skill_quantity(self.skill_id, self.quantity)

        if self.quantity <= 0:
            self.state = 'normal'


class CharacterLevelButton(Button):

    def __init__(self, **kwargs):
        super(CharacterLevelButton, self).__init__(**kwargs)

        self.character_level_info = CharacterLevelInfo()

    def open_character_level_info(self, character_name):
        self.character_level_info.character_name = character_name
        self.character_level_info.open()


class CharacterLevelInfo(ModalView):

    def __init__(self, **kwargs):
        super(CharacterLevelInfo, self).__init__(**kwargs)

        self.character_name = ''

    def on_pre_open(self):
        info = db.get_manuscript_lvl_info(self.character_name)
        level = info[0]
        current_exp = info[1]
        exp_for_next_level = info[2]

        self.ids.character_level.text = 'Уровень: ' + str(level)
        self.ids.exp.text = 'Опыт: ' + str(current_exp) + ' из ' + str(exp_for_next_level)
