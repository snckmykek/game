from kivy.lang.builder import Builder
from kivy.uix.modalview import ModalView
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from sqlite_requests import db
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton

Builder.load_file('store.kv')


class Store(ModalView):

    def __init__(self, **kwargs):
        super(Store, self).__init__(**kwargs)

        self.ids.character.skills = self.ids.skills
        self.ids.character.character_changer.change_character(self.ids.character)

    def on_pre_open(self):
        self.calculate_resources()

    def calculate_resources(self):
        self.crystal, self.crystal_fragments = db.get_resources()

    def give_crystal_fragments_test(self):
        db.set_crystal_fragments(500)
        self.calculate_resources()


class CharacterShop(Button):

    def __init__(self, **kwargs):
        super(CharacterShop, self).__init__(**kwargs)

        self.character_changer = CharacterChangerShop()
        self.character_changer.character = self
        self.skills = ObjectProperty
        character = db.get_current_character()
        self.name = character[0]
        self.background_normal = character[1] if character[6] == '1' else character[2]
        self.background_down = self.background_normal
        self.available = True if character[6] == '1' else False

    def open_character_changer(self):
        self.character_changer.character = self
        self.character_changer.open()


class CharacterChangerShop(ModalView):

    def __init__(self, **kwargs):
        super(CharacterChangerShop, self).__init__(**kwargs)

        self.character = ObjectProperty

    def on_pre_open(self):
        self.ids.character_selection.clear_widgets()
        for ch in db.get_characters():
            but = Button(background_normal=ch[1] if ch[6] == '1' else ch[2], border=[0, 0, 0, 0])
            but.bind(on_press=self.change_character)
            but.background_down = but.background_normal
            but.available = True if ch[6] == '1' else False
            but.level = ch[3]
            but.name = ch[0]
            self.ids.character_selection.add_widget(but)

    def change_character(self, instance):
        if not instance.available:
            return

        self.character.name = instance.name
        self.character.background_normal = instance.background_normal
        self.character.background_down = instance.background_down

        self.character.skills.clear_widgets()
        for skill in db.get_skills(instance.name):
            sk_box = SkillBoxShop()
            sk = sk_box.ids.skill
            sk.name = skill[1]
            sk.background_normal = skill[2]
            sk.skill_level = skill[3]
            sk.quantity = skill[4]
            sk.is_unblock = skill[5]
            self.character.skills.add_widget(sk_box)

        self.dismiss()


class SkillBoxShop(BoxLayout):
    def __init__(self, **kwargs):
        super(SkillBoxShop, self).__init__(**kwargs)


class SkillShop(Button):

    def __init__(self, **kwargs):
        super(SkillShop, self).__init__(**kwargs)

        self.name = ''
        self.skill_level = 1


    def open_deal(self):
        deal.skill_shop = self
        deal.open()


class Deal(ModalView):

    def __init__(self, **kwargs):
        super(Deal, self).__init__(**kwargs)

        self.skill_shop = ObjectProperty
        self.price = 0

    def on_pre_open(self):
        self.price = int(db.get_skill_price(self.skill_shop.name))

    def make_dial(self, extra_quantity):
        if extra_quantity * self.price > store.crystal_fragments:
            return

        self.skill_shop.quantity += extra_quantity
        db.set_crystal_fragments((extra_quantity * self.price) * (- 1))
        db.set_skill_quantity(self.skill_shop.name, self.skill_shop.quantity)
        
        store.calculate_resources()

    def on_pre_dismiss(self):
        store.calculate_resources()


store = Store()
deal = Deal()
