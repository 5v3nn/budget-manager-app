"""
main script
"""
from kivy.metrics import dp
from kivy.properties import (
    ListProperty,
    BooleanProperty,
    StringProperty,
    ObjectProperty,
)
from kivy.uix.screenmanager import SlideTransition
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.config import Config
from kivy.core.window import Window
from kivy.utils import platform
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRectangleFlatButton, MDIconButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.toolbar import MDTopAppBar

from screens import settings, db_settings
from save_system import SaveSystem

# set file variables
KIVY_FILE_SCREEN_MANAGER = "./templates/screen_manager.kv"

# set version
__version__ = "0.1.0.3"  # change in the buildozer.spec too

# Set screen size (didn't work)
# Config.set('graphics', 'resizable', 1)
# Config.set('graphics', 'width', 1080)
# Config.set('graphics', 'height', 2160)
if platform in ("linux", "win", "macosx"):
    Window.size = (1080 * 0.4, 2160 * 0.4)


class BudgetManagerApp(MDApp):

    title = "Budget Manager Application"
    manager = None

    def build(self):

        # load dark mode settings and apply
        dark_mode = SaveSystem().load_variable(
            SaveSystem().SAVE_FILE_SETTINGS, "dark_mode"
        )
        dark_mode = dark_mode if dark_mode is not None else True  # dart mode default
        settings.SettingsView().on_dark_theme_switch(dark_mode, self.theme_cls)

        # print("dark mode", dark_mode)

        # load kivy file(s)
        self.manager = Builder.load_file(KIVY_FILE_SCREEN_MANAGER)
        return self.manager


class BMTopAppBar(MDTopAppBar):
    """ Custom Top Tool Bar """

    title = StringProperty(defaultvalue="Budget Manager")

    # screen manager properties
    screen_manager = ObjectProperty(defaultvalue=None)
    settings_screen_name = "settings_view"
    db_settings_screen_name = "dbsettings_view"
    entry_add_screen_name = "entry_add_view"

    # button icons
    settings_icon = "dots-vertical"
    back_icon = "arrow-left"
    plus = "plus"

    # dropdown menu settings
    create_settings_dropdown = BooleanProperty(defaultvalue=False)
    settings_dropdown_menu = None
    settings_dropdown_menu_caller = ObjectProperty(defaultvalue=None)

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        if self.screen_manager is None:
            print(
                f"WARNING: On toolbar {self.title} the screen_manager is None, {self}"
            )

        if self.create_settings_dropdown:
            self.settings_dropdown_menu_init()

    def switch_screen(
        self, destination_name: str, trans_anim=SlideTransition(), trans_dir="left"
    ):
        """Change current screen to destination_name"""

        if not self.screen_manager:
            print("Error: No screen_manager")
        else:
            self.screen_manager.transition = trans_anim
            self.screen_manager.transition.direction = trans_dir
            self.screen_manager.current = destination_name
            self.screen_manager.transition = trans_anim

    # region settings_features
    def settings_dropdown_menu_init(self):
        """Initial settings dropdown menu"""

        if not self.settings_dropdown_menu:
            # check caller
            if self.settings_dropdown_menu_caller is None:
                self.settings_dropdown_menu_caller = self
                print(f"WARNING: Caller for toolbar {self.title} is None; assign self.")

            # create dropdown menu
            self.settings_dropdown_menu = MDDropdownMenu(
                caller=self.settings_dropdown_menu_caller,
                items=[
                    {
                        "text": "Settings",
                        "viewclass": "OneLineListItem",
                        "height": dp(54),
                        "on_release": lambda: self.on_settings_dropdown_menu(
                            self.settings_screen_name
                        ),
                    },
                    {
                        "text": "Database Settings",
                        "viewclass": "OneLineListItem",
                        "height": dp(54),
                        "on_release": lambda: self.on_settings_dropdown_menu(
                            self.db_settings_screen_name
                        ),
                    },
                ],
                width_mult=3,
                border_margin=10,
                position="bottom",
                elevation=10,
            )

    def settings_dropdown_menu_open(self):
        """if settings_dropdown_menu exists open"""

        if not self.settings_dropdown_menu:
            self.settings_dropdown_menu_init()

        self.settings_dropdown_menu.open()

    def on_settings_dropdown_menu(self, destination_screen_name: str):
        """change screen to destination_name and close settings_dropdown_menu"""

        self.switch_screen(destination_screen_name)
        self.settings_dropdown_menu.dismiss()

    # endregion


if __name__ == "__main__":
    BudgetManagerApp().run()
