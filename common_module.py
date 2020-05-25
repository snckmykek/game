from sqlite_requests import db
from dialog.main import dialog
from miniature.main import miniature
from kivy.clock import Clock


class GameAction:

    def __init__(self, **kwargs):
        super(GameAction, self).__init__(**kwargs)

        self.action_list = list()
        self.action_index = 0

    def execute_action(self, when_to_call, loc_id, lvl_id):
        self.action_index = 0
        self.action_list = db.get_actions(when_to_call, loc_id, lvl_id)  # id, action_type, object_id

        self.do_next_action()

    def do_next_action_deferred(self):
        Clock.schedule_once(self.do_next_action, .1)

    def do_next_action(self, d=.1):
        # логика такая: где-то уже получили список экшенов, выполняем их по очереди, после выполения предыдущего
        try:
            next_action = self.action_list[self.action_index]
            self.action_index += 1
        except IndexError:
            return

        if next_action[1] == 'open_skill':
            db.unblock_skill(next_action[2])
        elif next_action[1] == 'open_manuscript':
            db.unblock_manuscript(next_action[2])
        elif next_action[1] == 'location':
            pass  # stub
        elif next_action[1] == 'dialog':
            dialog.speech_list = db.get_speech_list(next_action[2])
            dialog.bind(on_dismiss=self.do_next_action)
            if dialog._window is not None:  # Бывает, когда окно не успело закрыться. Скорее это особенности
                # последовательности кода, в которые мне лезть впадлу. Если еще не закрылось, то вызывает отложенно
                # эту функцию через 0.1 сек
                self.action_index -= 1
                self.do_next_action_deferred()
            else:
                dialog.open()
            return  # диалог заряжен на вызов функции ду некст экшен, поэтому ретюрнимся отсюда после открытия
        elif next_action[1] == 'miniature':
            miniature.miniature_list = db.get_miniature_list(next_action[2])
            miniature.bind(on_dismiss=self.do_next_action)
            if miniature._window is not None:  # Бывает, когда окно не успело закрыться. Скорее это особенности
                # последовательности кода, в которые мне лезть впадлу. Если еще не закрылось, то вызывает отложенно
                # эту функцию через 0.1 сек
                self.action_index -= 1
                self.do_next_action_deferred()
            else:
                miniature.open()
            return  # миниатюра заряжена на вызов функции ду некст экшен, поэтому ретюрнимся отсюда после открытия

        # db.change_actions_completed([next_action])  # в массив, т.к. функция принимает массив

        self.do_next_action()


game_action = GameAction()