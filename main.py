from kivy.app import App
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.graphics import Color, Rectangle
from kivy.animation import Animation
from kivy.clock import Clock

# Настройки окна
Window.clearcolor = (0.05, 0.05, 0.08, 1)
Window.fullscreen = 'auto'

# --- 1. ГЛАВНОЕ МЕНЮ ---
class MainMenu(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        with self.canvas.before:
            Color(0.05, 0.05, 0.08, 1)
            self.bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)

        self.add_widget(Label(
            text="ROCKET SYSTEM", font_size='32sp', bold=True,
            color=(0.2, 0.6, 1, 1), pos_hint={"center_x": 0.5, "top": 0.9}
        ))

        btn = Button(
            text="ЗАПУСТИТЬ WINLOCKER",
            font_size='20sp', bold=True,
            background_color=(0.8, 0.1, 0.1, 1),
            size_hint=(0.7, 0.12),
            pos_hint={"center_x": 0.5, "center_y": 0.4}
        )
        btn.bind(on_release=self.go_to_locker)
        self.add_widget(btn)

    def update_bg(self, instance, value):
        self.bg.pos = instance.pos
        self.bg.size = instance.size

    def go_to_locker(self, instance):
        self.manager.current = 'locker'

# --- 2. ВИНЛОКЕР ---
class WinlockerScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.passwords = ["0000", "1234"]
        self.build_ui()

    def build_ui(self):
        with self.canvas.before:
            Color(0.02, 0.02, 0.02, 1)
            self.bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)

        self.title = Label(
            text="", font_size='28sp', bold=True,
            color=(1, 0.2, 0.2, 1), pos_hint={"center_x": 0.5, "top": 0.85}
        )
        self.add_widget(self.title)

        self.pwd_input = TextInput(
            hint_text="Введите пароль...", password=True, font_size='24sp',
            multiline=False, size_hint=(0.7, 0.1),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            background_color=(0.15, 0.15, 0.2, 1), foreground_color=(1, 1, 1, 1)
        )
        self.add_widget(self.pwd_input)

        self.btn = Button(
            text="РАЗБЛОКИРОВАТЬ", font_size='20sp', bold=True,
            background_color=(0.2, 0.6, 1, 1), size_hint=(0.6, 0.1),
            pos_hint={"center_x": 0.5, "center_y": 0.3}
        )
        self.btn.bind(on_release=self.check_password)
        self.add_widget(self.btn)

        self.error_lbl = Label(
            text="", font_size='18sp', color=(1, 0, 0, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.2}
        )
        self.add_widget(self.error_lbl)

    def update_bg(self, instance, value):
        self.bg.pos = instance.pos
        self.bg.size = instance.size

    def check_password(self, instance):
        if self.pwd_input.text.strip() in self.passwords:
            self.error_lbl.text = "ДОСТУП РАЗРЕШЕН"
            self.error_lbl.color = (0, 1, 0, 1)
            self.title.text = "СИСТЕМА РАЗБЛОКИРОВАНА"
            self.title.color = (0, 1, 0, 1)
            self.btn.disabled = True
            self.pwd_input.disabled = True
            
            # Возврат в меню через 1.5 сек
            Clock.schedule_once(lambda dt: self.go_back(), 1.5)
        else:
            self.error_lbl.text = "НЕВЕРНЫЙ ПАРОЛЬ"
            self.pwd_input.text = ""
            # Тряска
            anim = Animation(pos_hint={"center_x": 0.55}, duration=0.05) + \
                   Animation(pos_hint={"center_x": 0.45}, duration=0.05) + \
                   Animation(pos_hint={"center_x": 0.5}, duration=0.05)
            anim.start(self.pwd_input)

    def go_back(self):
        self.manager.current = 'menu'
        self.reset_ui()

    def reset_ui(self):
        self.title.text = "."
        self.title.color = (1, 0.2, 0.2, 1)
        self.error_lbl.text = ""
        self.pwd_input.text = ""
        self.pwd_input.disabled = False
        self.btn.disabled = False

# --- 3. ГЛАВНОЕ ПРИЛОЖЕНИЕ ---
class MainApp(App):
    def build(self):
        self.title = "ROCKET System"
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(MainMenu(name='menu'))
        sm.add_widget(WinlockerScreen(name='locker'))
        return sm

    def on_start(self):
        Window.bind(on_keyboard=self.hook_keyboard)

    def hook_keyboard(self, window, key, *largs):
        # Блокируем кнопку "Назад", пока мы на экране винлокера
        if key == 27 and self.root.current == 'locker':
            return True 
        return False

if __name__ == '__main__':
    MainApp().run()