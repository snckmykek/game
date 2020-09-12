from kivy.animation import Animation


def its_lock_animation(obj, params):
    s = obj.size_lock
    animation = Animation(size_lock=[s[0] * 1.1, s[1] * 1.1], d=.1) + Animation(size_lock=obj.size_lock_default, d=.1)

    return animation


def open_close_menu_buttons_animation(obj, new_size):
    animation = Animation(size=new_size, center=obj.center.copy(), d=1, t='out_elastic')

    return animation


def decrease_animation(obj, color):
    animation = Animation(size=(0, 0), center=obj.center.copy(), d=0.15) \
                + Animation(size=obj.size.copy(), center=obj.center.copy(), d=0.1, background_color=color)

    return animation


def combo_animation(obj, color):
    size = obj.size.copy()
    center = obj.center.copy()
    obj.size = (0, 0)
    obj.center = center
    animation = Animation(size=(size[0]*1.2, size[1]*1.2), center=center, color=(1, 1, 1, 1), d=.3) \
                + Animation(size=size, center=center) + Animation(d=1.5) + Animation(d=1, color=(1, 1, 1, 0))

    return animation


def explosion_animation(obj, color):
    transparent_background_color = obj.background_color.copy()
    transparent_background_color.insert(3, 0)
    animation = Animation(center=obj.center.copy(), d=0.15, background_color=transparent_background_color) \
                + Animation(size=obj.size.copy(), center=obj.center.copy(), d=0.1, background_color=color)

    return animation


def get_animation_from_id(animation_id, obj, params):
    animations = {'decrease': decrease_animation,
                  'explosion': explosion_animation,
                  'its_lock': its_lock_animation,
                  'open_close_menu_buttons': open_close_menu_buttons_animation,
                  'combo': combo_animation}

    current_func = animations.get(animation_id,
                                  decrease_animation)  # Если значения ключа нет, вернет дефолтную анимацию

    return current_func(obj, params)


def do_animation(animation_id, obj, params=None):
    animation = get_animation_from_id(animation_id, obj, params)

    animation.start(obj)
