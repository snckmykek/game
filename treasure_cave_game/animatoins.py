from kivy.animation import Animation


def move_car(obj, params):
    # animation = Animation(y=params, d=.5, t='out_bounce')
    animation = Animation(y=params, d=.5)
    return animation


def take_item(obj, params):
    animation = Animation(width=0, height=0, d=.5)
    animation.bind(on_complete=lambda *l: params(obj))

    return animation


def get_animation_from_id(animation_id, obj, params):
    animations = {'move_car': move_car,
                  'take_item': take_item
                  }

    current_func = animations.get(animation_id,
                                  move_car)  # Если значения ключа нет, вернет дефолтную анимацию

    return current_func(obj, params)


def do_animation(animation_id, obj, params=None):
    animation = get_animation_from_id(animation_id, obj, params)

    animation.start(obj)
