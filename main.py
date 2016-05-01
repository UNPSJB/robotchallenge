# -*- coding: utf-8 -*-
import sys
try:
    import kivy
except ImportError:
    from utils import encontrar_kivy
    encontrar_kivy()


from kivy.app import App
from kivy.uix.label import Label
# from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout

from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.animation import Animation
from kivy.core.window import Window

# Configuración de fullscreen
# No funcioan bien en OS X
if sys.platform == 'darwin':
    pass
else:
    Window.fullscreen = 'auto'
Window.set_title("Semáforo")

try:
    from kivy.core.audio import SoundLoader
    light_1_sound = SoundLoader.load('data/light_1.wav')
    light_2_sound = SoundLoader.load('data/light_2.wav')
except:
    light_1_sound = light_2_sound = None


class LightLabel(Label):
    red   = NumericProperty(0)
    green = NumericProperty(.9)
    blue  = NumericProperty(0)
    alpha = NumericProperty(0)


class LightBox(BoxLayout):
    '''
    Intenta emular a https://www.youtube.com/watch?v=L9SEuYpGrjg
    '''

    counter = 0

    def start(self):
        self.counter = 0

        Clock.schedule_interval(self.tick, 1)
        self.ids.buttons.ids.start_button.disabled = True
        # Arreglo disperso de leds
        # {1: Led1, 2: Led2, 3: Led3}
        self.leds = {i: getattr(self.ids, 'led%d' % i, None) for i in range(1, 4)}

    def tick(self, elapsed):
        self.counter += 1

        if self.counter < 4:
            # Iluminación progresiva de los leds
            anim = Animation(alpha=0.8, duration=0.3)
            anim.start(self.leds[self.counter])  # 1, 2, 3
            if light_1_sound:
                light_1_sound.play()
        elif self.counter == 4:
            for n, led in self.leds.items():
                anim = Animation(alpha=0, duration=0.3)
                anim.start(led)
        # 5 segundos apagado
        elif self.counter == (4+5):
            for n, led in self.leds.items():
                anim = Animation(alpha=1, duration=0.2) + Animation(alpha=0, duration=0.5)
                anim.start(led)
                if light_2_sound:
                    light_2_sound.play()
        elif self.counter == (4+5+1):
            Clock.unschedule(self.tick)
            self.ids.buttons.ids.start_button.disabled = False


class TorneoApp(App):
    """Aplicacion de light app"""
    def build(self):
        return LightBox()

if __name__ == '__main__':
    app = LightApp()
    app.run()
