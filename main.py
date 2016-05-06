#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from time import time

try:
    import kivy
except ImportError:
    from utils import encontrar_kivy
    encontrar_kivy()


from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.logger import Logger
# from kivy.factory import Factory


DEBUG = os.environ.get('DEBUG', False)

# Configuración de fullscreen
# No funcioan bien en OS X
# if sys.platform == 'darwin':
#     pass
# else:
#     Window.fullscreen = 'auto'
# Window.set_title("Semáforo")

try:
    from kivy.core.audio import SoundLoader
    light_1_sound = SoundLoader.load('data/light_1.wav')
    light_2_sound = SoundLoader.load('data/light_2.wav')
except:
    light_1_sound = light_2_sound = None


class LightLabel(Label):
    """
    Luz verde
    """
    red   = NumericProperty(0)
    green = NumericProperty(.9)
    blue  = NumericProperty(0)
    alpha = NumericProperty(0)


class SemaforoSumo(Screen):
    '''
    Este widget es una pantalla, por lo que es el root para el cálculo
    de los IDs
    Intenta emular a https://www.youtube.com/watch?v=L9SEuYpGrjg
    '''

    counter = 0
    mins = NumericProperty(3)
    countdown = 0
    STATE_INITIAL_COUNTER = 0
    STATE_PRECOUNTDOWN = 1
    STATE_COUNTDOWN = 2
    STATE_PAUSED = 3


    # Countdown
    if not DEBUG:
        CONTADOR_INICIAL = 4
        CONTADOR_APAGADO = 4 + 5
        CONTADOR_FLASH = 4 + 5 + 1
        ANIMATION_DELAY = 0.3
    else:
        CONTADOR_INICIAL = 1
        CONTADOR_APAGADO = 2
        CONTADOR_FLASH = 3
        ANIMATION_DELAY = 0.3
    def start(self):
        self.counter = 0
        Clock.schedule_interval(self.tick, 1)
        self.ids.start_button.disabled = True
        # Arreglo disperso de leds
        # {1: Led1, 2: Led2, 3: Led3}
        self.leds = {i: getattr(self.ids, 'led%d' % i, None) for i in range(1, 4)}
        self.state = self.STATE_PRECOUNTDOWN

    def tick(self, elapsed):
        self.counter += 1

        if self.counter < self.CONTADOR_INICIAL:

            # self.counter < self.CONTADOR_INICIAL:
            # Iluminación progresiva de los leds
            anim = Animation(alpha=0.8, duration=self.ANIMATION_DELAY)
            anim.start(self.leds[self.counter])  # 1, 2, 3
            if light_1_sound:
                light_1_sound.play()
        elif self.counter == self.CONTADOR_INICIAL:
            for n, led in self.leds.items():
                anim = Animation(alpha=0, duration=self.ANIMATION_DELAY)
                anim.start(led)
        # 5 segundos apagado
        elif self.counter == self.CONTADOR_APAGADO:
            for n, led in self.leds.items():
                anim = Animation(
                    alpha=1, duration=self.ANIMATION_DELAY * .5
                ) + Animation(
                    alpha=0, duration=self.ANIMATION_DELAY * 2
                )
                anim.start(led)
                if light_2_sound:
                    light_2_sound.play()
        elif self.counter == self.CONTADOR_FLASH:
            Clock.unschedule(self.tick)
            # self.ids.start_button.disabled = False
            self.ids.sem_screen_mgr.current = 'contador'

            self.countdown = time() + (self.mins * 60)
            self.counter += elapsed
            mins, secs = divmod(self.countdown, 60)
            self.ids.coundown_label.text = '3:00.000'
            Clock.schedule_interval(self.tick, 0.01)
            self.state = self.STATE_COUNTDOWN
        elif self.STATE_COUNTDOWN:  # self.counter >= self.CONTADOR_FLASH:
            remaining = self.countdown - time()
            mins, secs = divmod(remaining, 60)
            self.ids.coundown_label.text = '%d:%-2.3f' % (mins, secs)
        else:
            Logger.info("State is %s", self.state)


    def spacebar_pressed(self):
        if self.STATE_COUNTDOWN:
            Clock.unschedule(self.tick)



class SemaforoApp(App):
    """Aplicacion de light app"""
    def __init__(self):
        super(SemaforoApp, self).__init__()
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        Logger.info("DEBUG: %s", DEBUG)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, code_str, hex, others):
        code, key = code_str

        if key == 'f' and 'ctrl' in others:
            print "*" * 10
            Window.toggle_fullscreen()
        elif key == 'spacebar':
            try:
                self.root.current_screen.spacebar_pressed()
            except Exception:
                Logger.info("Not in screen")

        if key == 'q' and not others:
            sys.exit(1)


if __name__ == '__main__':
    app = SemaforoApp()
    app.run()
