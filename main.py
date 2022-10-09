"""
main script
"""

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.config import Config
from kivy.core.window import Window
from screens import settings
from save_system import SaveSystem

# set file variables
KIVY_FILE_SCREEN_MANAGER = './templates/screen_manager.kv'

# set version
__version__ = "0.1.0.1"  # change in the buildozer.spec too

# Set screen size (didn't work)
# Config.set('graphics', 'resizable', 1)
# Config.set('graphics', 'width', 1080)
# Config.set('graphics', 'height', 2160)
# Window.size = (1080 * .4, 2160 * .4)


class BudgetManagerApp(MDApp):
    title = 'Budget Manager Application'


    def build(self):

        # load dark mode settings and apply
        dark_mode = SaveSystem().load_variable(SaveSystem().SAVE_FILE_SETTINGS, 'dark_mode')
        dark_mode = dark_mode if dark_mode is not None else True
        settings.SettingsView().on_dark_theme_switch(dark_mode, self.theme_cls)
        # self.theme_cls.theme_style_switch_animation = True
        # self.theme_cls.theme_style = "Dark"
        # self.theme_cls.primary_palette = "BlueGray"
        # self.theme_cls.accent_palette = "Gray"

        manager = Builder.load_file(KIVY_FILE_SCREEN_MANAGER)
        return manager



if __name__ == '__main__':
    BudgetManagerApp().run()
