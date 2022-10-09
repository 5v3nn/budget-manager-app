"""
This script handles the general settings of the application
"""

from kivy.uix.screenmanager import SlideTransition
from kivymd.uix.screen import MDScreen
from save_system import SaveSystem
import loghandler


class SettingsView(MDScreen):

    LOG_FILE = './logs/settings_view.log'


    def get_dark_theme_value(self):
        # apply dark theme settings

        try:
            dark = SaveSystem.load_variable(SaveSystem().SAVE_FILE_SETTINGS, 'dark_mode')

            if dark and dark is not None:
                return dark
            else:
                raise Exception(f'Value error for dark mode = {dark}')

        except Exception as dark_mode_err:
            errmsg = f"GET DARK MODE VALUE ERROR: {str(dark_mode_err)}"
            loghandler.write_log(self.LOG_FILE, errmsg)
            print(errmsg)
            return False

    def on_back_button(self):
        """
        Go back to the default screen

        :return:
        """

        # transition options
        self.manager.transition = SlideTransition()
        self.manager.transition.direction = 'right'
        self.manager.current = 'entry_view'

    @staticmethod
    def on_dark_theme_switch(active_value: bool, theme_cls):
        """
        Call this function to set theme style

        :param active_value: pass True for dark theme, False for light theme
        :param theme_cls: the theme class
        :return:
        """

        # add this parameter in hope it'll create a nice transition animation
        theme_cls.theme_style_switch_animation = True

        # set theme style
        if active_value:
            theme_cls.theme_style = "Dark"
            theme_cls.primary_palette = "BlueGray"
            theme_cls.accent_palette = "BlueGray"
        else:
            theme_cls.theme_style = "Light"
            theme_cls.primary_palette = "Blue"
            theme_cls.accent_palette = "Gray"

        # save new value
        SaveSystem().save_variable(SaveSystem().SAVE_FILE_SETTINGS, 'dark_mode', active_value)
