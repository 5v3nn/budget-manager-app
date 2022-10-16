from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import SlideTransition
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import Snackbar
# from screens.entry_add_view import TextInputMaxLength
from save_system import SaveSystem
from data_management import DataManagement
from kivymd.app import MDApp


class DBSettingsView(MDScreen):
    """ Settings screen"""

    app = None

    # theme class
    theme_class = None

    # category management
    category_create_dialog = None
    category_delete_dialog = None
    category_delete_dialog_alert = None


    def __init__(self, **kwargs):
        super(DBSettingsView, self).__init__(**kwargs)

        # get running app
        self.app = MDApp.get_running_app()

        # get theme class
        self.theme_class = self.app.theme_cls

        # init dialogs
        self.init_category_management_dialogs()


    # region category_management
    def init_category_management_dialogs(self):
        """ Init dialogs for the category management beforehand.  """

        # create category dialog
        self.category_create_dialog = MDDialog(
            title="Create New Category:",
            type="custom",
            auto_dismiss=False,
            content_cls=CreateCategoryDialog(),
            buttons=[
                MDFlatButton(
                    text="Cancel",
                    theme_text_color="Custom",
                    text_color=self.theme_class.primary_color,
                    on_release=lambda x: self.category_create_dialog_on_close()
                ),
                MDFlatButton(
                    text="Create",
                    theme_text_color="Custom",
                    text_color=self.theme_class.primary_color,
                    on_release=lambda x: self.category_create_dialog_on_create()
                ),
            ],
        )

        # delete category dialog
        self.category_delete_dialog = MDDialog(
            title="Select Category to Delete:",
            type="confirmation",
            auto_dismiss=False,
            buttons=[
                MDFlatButton(
                    text="Cancel",
                    theme_text_color="Custom",
                    text_color=self.theme_class.primary_color,
                    on_release=lambda x: self.category_delete_dialog_on_close()
                ),
                MDFlatButton(
                    text="Delete",
                    theme_text_color="Custom",
                    text_color=self.theme_class.primary_color,
                    on_release=lambda x: self.category_delete_dialog_on_delete(self.theme_class)
                ),
            ],
            items=[],
        )

    def on_create_category_button(self, theme_cls):
        """Show Dialog for creating a new category, which will be added to the database.

        :param theme_cls: theme class
        :return:
        """

        if not self.category_create_dialog:
            self.init_category_management_dialogs()

        self.category_create_dialog.open()

    def category_create_dialog_on_close(self):
        """ Close and reset category create dialog"""
        self.category_create_dialog.dismiss()
        self.category_create_dialog = None

    def category_create_dialog_on_create(self):
        """ Create a new category and submit to database """

        category_name = self.category_create_dialog.content_cls.ids['create_category_button'].text

        if not category_name:
            self.category_create_dialog_on_close()
            return

        # add new category
        DataManagement().add_category(category_name)

        # create a quick snackbar as feedback that category was created
        Snackbar(text=f'Created new category: "{category_name}".',
                 snackbar_x='20dp',
                 snackbar_y='20dp',
                 size_hint_x=(Window.width - (dp(20) * 2)) / Window.width,
                 duration=3,
                 ).open()

        # close dialog
        self.category_create_dialog_on_close()

    def on_delete_category_button(self):
        """Show Dialog for deleting a category, which will be submitted to the database.

        :return:
        """

        #todo remove arguments

        if not self.category_delete_dialog:
            self.init_category_management_dialogs()

        # set dialog items
        self.category_delete_dialog.update_items([
            DeleteCategoryDialogItem(text=f"{category_name}") for category_name in DataManagement().get_categories()
        ])

        self.category_delete_dialog.open()

    def category_delete_dialog_on_close(self):
        """ Close and reset category delete dialog"""
        self.category_delete_dialog.dismiss()
        self.category_delete_dialog = None

    def category_delete_dialog_on_delete(self, theme_cls):
        """ creates an alert dialog to confirm deletion of category """

        # get items text by iterating through the items, i.e. category list
        items_to_delete = []
        for item in self.category_delete_dialog.items:
            # if item is checked add to deletion list
            if item.ids['check'].active:
                items_to_delete.append(item.text)

        if not items_to_delete:
            self.category_delete_dialog_on_close()
            return

        # get number of items to delete
        nr_of_entries_to_delete = 0
        for item in items_to_delete:
            nr_of_entries_to_delete += len(DataManagement().get_entries_by_category(item))

        # create alert title and text
        alert_title, alert_text = "Delete Category?", f"Delete category: '{items_to_delete[0]}',\nand {nr_of_entries_to_delete} related entries?"
        # change alert title and text if there are mor than one category to delete
        if len(items_to_delete) > 1:
            alert_title, alert_text = "Delete Categories?", f"Delete categories: "
            for i in range(len(items_to_delete)):
                alert_text += f"'{items_to_delete[i]}'" + ", "
            alert_text += f"\nand {nr_of_entries_to_delete} related entries?"

        # alert box for confirmation to delete category and related entries
        if not self.category_delete_dialog_alert:
            # its okay to create dialog here, since this one doesn't cost too much.
            self.category_delete_dialog_alert = MDDialog(
                title=alert_title,
                text=alert_text,
                buttons=[
                    MDFlatButton(
                        text="Cancel",
                        theme_text_color="Custom",
                        text_color=theme_cls.primary_color,
                        on_release=lambda x: self.category_delete_alert_dialog_on_close()
                    ),
                    MDFlatButton(
                        text="Delete",
                        theme_text_color="Custom",
                        text_color=theme_cls.primary_color,
                        on_release=lambda x: self.category_delete_alert_dialog_on_confirm(items_to_delete)
                    ),
                ],
            )
        self.category_delete_dialog_alert.open()

    def category_delete_alert_dialog_on_close(self):
        """ Close and reset category delete alert dialog"""
        self.category_delete_dialog_alert.dismiss()
        self.category_delete_dialog_alert = None
        self.category_delete_dialog_on_close()

    def category_delete_alert_dialog_on_confirm(self, items_to_delete):
        """ submit deletion to database """

        print(items_to_delete)

        # make deletion on database
        for item in items_to_delete:
            DataManagement().del_category(item)

        # create snackbar text
        alert_text = f"Deleted category: '{items_to_delete[0]}'?"
        # change alert title and text if there are mor than one category to delete
        if len(items_to_delete) > 1:
            alert_text = f"Deleted categories: "
            for i in range(len(items_to_delete)):
                alert_text += f"'{items_to_delete[i]}'" + (", " if i <= len(items_to_delete) - 2 else "")

        # create a quick snackbar as feedback that category/ies was deleted
        Snackbar(text=alert_text,
                 snackbar_x='20dp',
                 snackbar_y='20dp',
                 size_hint_x=(Window.width - (dp(20) * 2)) / Window.width,
                 duration=3,
                 ).open()
        # close dialog
        self.category_delete_alert_dialog_on_close()
    # endregion


class CreateCategoryDialog(MDBoxLayout):
    """ Dialog for creating a new category. """
    pass


class DeleteCategoryDialogItem(OneLineAvatarIconListItem):
    """ Category item in delete category dialog. """

    divider = None

    @classmethod
    def set_icon(cls, instance_check):
        # switch check
        instance_check.active = not instance_check.active
