"""
This script generates a splash screen at the start of the app.
"""

# import kivy modules
from kivy.uix.screenmanager import NoTransition, SlideTransition
from kivymd.uix.screen import MDScreen
from kivy.clock import Clock


class SplashScreen(MDScreen):
    """Dummy screen"""

    def on_enter(self):
        # switch immediately to entry view
        Clock.schedule_once(self.switch_screen)

    def switch_screen(self, dt):
        self.manager.transition = NoTransition()
        self.manager.current = 'entry_view'
        self.manager.transition = SlideTransition()

