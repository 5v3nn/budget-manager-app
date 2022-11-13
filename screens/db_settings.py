import json
import os

from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import SlideTransition
from kivymd.toast import toast
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.list import OneLineAvatarIconListItem, BaseListItem
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import Snackbar
# from screens.entry_add_view import TextInputMaxLength
from kivymd.app import MDApp
from kivy.utils import platform

from save_system import SaveSystem
from data_management import DataManagement
from assets.utilities.permission_manager import PermissionManager
import loghandler


class DBSettingsView(MDScreen):
    """ Settings screen"""

    LOG_FILE = './logs/db_settings.log'

    app = None

    # theme class
    theme_class = None

    # category management
    category_create_dialog = None
    category_delete_dialog = None
    category_delete_dialog_alert = None
    _category_items_to_delete = []
    month_delete_dialog = None
    month_delete_dialog_alert = None
    _month_items_to_delete = []

    # export db
    export_file_manager = None
    export_manager_open = False
    import_file_manager = None
    import_manager_open = False


    def __init__(self, **kwargs):
        super(DBSettingsView, self).__init__(**kwargs)

        # get running app
        self.app = MDApp.get_running_app()

        # get theme class
        self.theme_class = self.app.theme_cls

        # init dialogs
        self.init_category_management_dialogs()

        # init export file manager
        self.init_export_import_file_manager()

    def on_back_button(self):
        """
        Go back to the default screen

        :return:
        """

        # transition options
        self.manager.transition = SlideTransition()
        self.manager.transition.direction = 'right'
        self.manager.current = 'entry_view'

    def init_category_management_dialogs(self):
        """ Init dialogs for the category management beforehand.  """

        print('init database management dialogs')

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
        self.category_delete_dialog = CheckboxItemsDialog(
            title="Select Category to Delete:",
            # text='text',
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
                    on_release=lambda x: self.category_delete_dialog_on_delete()
                ),
            ],
            items=[],
        )

        # delete category alert confirmation dialog
        self.category_delete_dialog_alert = MDDialog(
            title='',
            text='',
            buttons=[
                MDFlatButton(
                    text="Cancel",
                    theme_text_color="Custom",
                    text_color=self.theme_class.primary_color,
                    on_release=lambda x: self.category_delete_alert_dialog_on_close()
                ),
                MDFlatButton(
                    text="Delete",
                    theme_text_color="Custom",
                    text_color=self.theme_class.primary_color,
                    on_release=lambda x: self.category_delete_alert_dialog_on_confirm()
                ),
            ],
        )

        # delete month dialog
        self.month_delete_dialog = CheckboxItemsDialog(
            title="Select Month to Delete:",
            # text='text',
            type="confirmation",
            auto_dismiss=False,
            buttons=[
                MDFlatButton(
                    text="Cancel",
                    theme_text_color="Custom",
                    text_color=self.theme_class.primary_color,
                    on_release=lambda x: self.month_delete_dialog_on_close()
                ),
                MDFlatButton(
                    text="Delete",
                    theme_text_color="Custom",
                    text_color=self.theme_class.primary_color,
                    on_release=lambda x: self.month_delete_dialog_on_delete()
                ),
            ],
            items=[],
        )

        # delete month alert confirmation dialog
        self.month_delete_dialog_alert = MDDialog(
            title='',
            text='',
            buttons=[
                MDFlatButton(
                    text="Cancel",
                    theme_text_color="Custom",
                    text_color=self.theme_class.primary_color,
                    on_release=lambda x: self.month_delete_alert_dialog_on_close()
                ),
                MDFlatButton(
                    text="Delete",
                    theme_text_color="Custom",
                    text_color=self.theme_class.primary_color,
                    on_release=lambda x: self.month_delete_alert_dialog_on_confirm()
                ),
            ],
        )

    # region create_category
    def on_create_category_button(self):
        """Show Dialog for creating a new category, which will be added to the database."""

        if not self.category_create_dialog:
            self.init_category_management_dialogs()

        self.category_create_dialog.open()

    def category_create_dialog_on_close(self):
        """ Close and reset category create dialog"""

        self.category_create_dialog.content_cls.ids['create_category_input'].text = ''  # reset input field content
        self.category_create_dialog.dismiss()

    def category_create_dialog_on_create(self):
        """ Create a new category and submit to database """

        category_name = self.category_create_dialog.content_cls.ids['create_category_input'].text

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
    # endregion

    # region delete_category
    def on_delete_category_button(self):
        """Show Dialog for deleting a category, which will be submitted to the database.

        :return:
        """

        if not self.category_delete_dialog:
            self.init_category_management_dialogs()

        [print(category_name) for category_name in DataManagement().get_categories()]

        # set dialog items; list all categories
        self.category_delete_dialog.update_items([
            DeleteCategoryDialogItem(text=f"{category_name}") for category_name in DataManagement().get_categories()
        ])

        self.category_delete_dialog.open()

    def category_delete_dialog_on_close(self):
        """ Close and reset category delete dialog"""
        self.category_delete_dialog.dismiss()

    def category_delete_dialog_on_delete(self):
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
            # it's okay to create dialog here, since this one doesn't cost too much.
            self.init_category_management_dialogs()

        # assign title and text
        self.category_delete_dialog_alert.title = alert_title
        self.category_delete_dialog_alert.text = alert_text

        # assign items_to_delete
        self._category_items_to_delete = items_to_delete[:]

        # open
        self.category_delete_dialog_alert.open()

    def category_delete_alert_dialog_on_close(self):
        """ Close and reset category delete alert dialog"""
        self.category_delete_dialog_alert.dismiss()
        self._category_items_to_delete = []  # make sure list it empty again
        self.category_delete_dialog_on_close()

    def category_delete_alert_dialog_on_confirm(self):
        """ submit deletion to database """

        # get items_to_delete
        items_to_delete = self._category_items_to_delete

        if not items_to_delete:
            loghandler.write_log(self.LOG_FILE, f"No categories selected to delete; cancel process;")
            return

        # make deletion on database
        for item in items_to_delete:
            DataManagement().del_category(item)
        loghandler.write_log(self.LOG_FILE, f"Deleted categories: {items_to_delete};")

        # create snackbar text
        alert_text = f"Deleted category: '{items_to_delete[0]}'."
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

    # region delete_month
    def on_delete_month_button(self):
        """Show Dialog for deleting a month, which will be submitted to the database.

        :return:
        """

        if not self.month_delete_dialog:
            self.init_category_management_dialogs()

        [print(category_name) for category_name in DataManagement().get_categories()]

        # set dialog items; list all categories
        self.month_delete_dialog.update_items([
            DeleteCategoryDialogItem(text=f"{month_name}") for month_name in DataManagement().get_available_dates()
        ])

        self.month_delete_dialog.open()

    def month_delete_dialog_on_close(self):
        """ Close and reset month delete dialog"""
        self.month_delete_dialog.dismiss()

    def month_delete_dialog_on_delete(self):
        """ creates an alert dialog to confirm deletion of month """

        # get items text by iterating through the items, i.e. month list
        items_to_delete = self.month_delete_dialog.get_all_checked_items()

        print(f"month checked items: {items_to_delete}")

        if not items_to_delete:
            self.month_delete_dialog_on_close()
            return

        # get number of items to delete
        nr_of_entries_to_delete = 0
        for item in items_to_delete:
            nr_of_entries_to_delete += len(DataManagement().get_entries_by_date(item))

        # create alert title and text
        alert_title, alert_text = "Delete Month?", f"Delete month: '{items_to_delete[0]}',\nand {nr_of_entries_to_delete} related entries?"
        # change alert title and text if there are mor than one category to delete
        if len(items_to_delete) > 1:
            alert_title, alert_text = "Delete months?", f"Delete months: "
            for i in range(len(items_to_delete)):
                alert_text += f"'{items_to_delete[i]}'" + ", "
            alert_text += f"\nand {nr_of_entries_to_delete} related entries?"

        # alert box for confirmation to delete category and related entries
        if not self.month_delete_dialog_alert:
            # it's okay to create dialog here, since this one doesn't cost too much.
            self.init_category_management_dialogs()

        # assign title and text
        self.month_delete_dialog_alert.title = alert_title
        self.month_delete_dialog_alert.text = alert_text

        # assign items_to_delete
        self._month_items_to_delete = items_to_delete[:]

        # open
        self.month_delete_dialog_alert.open()

    def month_delete_alert_dialog_on_close(self):
        """ Close and reset month delete alert dialog"""
        self.month_delete_dialog_alert.dismiss()
        self._month_items_to_delete = []  # make sure list it empty again
        self.month_delete_dialog_on_close()

    def month_delete_alert_dialog_on_confirm(self):
        """ submit deletion to database """

        print('')

        # get items_to_delete
        items_to_delete = self._month_items_to_delete

        if not items_to_delete:
            loghandler.write_log(self.LOG_FILE, f"No months selected to delete; cancel process;")
            return

        # make deletion on database
        for item in items_to_delete:
            DataManagement().del_month(item)
        loghandler.write_log(self.LOG_FILE, f"Deleted months: {items_to_delete};")

        # create snackbar text
        alert_text = f"Deleted month: '{items_to_delete[0]}'."
        # change alert title and text if there are mor than one category to delete
        if len(items_to_delete) > 1:
            alert_text = f"Deleted months: "
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
        self.month_delete_alert_dialog_on_close()
    # endregion

    # region export_import_db

    def init_export_import_file_manager(self):

        # export file manager
        self.export_manager_open = False
        self.export_file_manager = MDFileManager(
            exit_manager=self.export_exit_manager,
            select_path=self.export_select_path
        )

        # import file manager
        self.import_manager_open = False
        self.import_file_manager = MDFileManager(
            exit_manager=self.import_exit_manager,
            select_path=self.import_select_path
        )


    def export_file_manager_open(self):

        if not self.export_file_manager:
            self.init_export_import_file_manager()

        self.export_file_manager.show(os.path.expanduser(PermissionManager().get_default_external_storage()))
        self.export_manager_open = True

    def export_select_path(self, path: str):
        """ It will be called when you click on the file name
        or the catalog selection button.

        :param path: path to the selected directory or file;
        """

        # print(path, toast(path))
        path = self.export_db_data(path)

        self.export_exit_manager()
        toast(f"Exported to '{path}'")

    def export_db_data(self, path: str):
        """ Export the db data into a json file """

        # todo error handling

        # make sure it's a folder not a file
        if not os.path.isdir(path):
            path = os.path.dirname(path)
            self.export_db_data(path)
            return path

        # get data
        data = DataManagement().export_all()

        # add file name
        path = os.path.join(path, 'db.json')

        # dump data to file
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, fp=f, indent=4)

        return path

    def export_exit_manager(self, *args):
        """ Called when the user reaches the root of the directory tree """

        self.export_manager_open = False
        self.export_file_manager.close()

    def import_file_manager_open(self):

        if not self.import_file_manager:
            self.init_export_import_file_manager()

        self.import_file_manager.show(os.path.expanduser(PermissionManager().get_default_external_storage()))
        self.import_manager_open = True

    def import_select_path(self, path: str):
        """ It will be called when you click on the file name
        or the catalog selection button.

        :param path: path to the selected directory or file;
        """

        # print(path, toast(path))
        success = self.import_db_data(path)

        self.import_exit_manager()
        if not success:
            toast('Error on import')
        else:
            toast('Imported data')

    def import_db_data(self, path: str) -> bool:
        """ Export the db data into a json file """

        # make sure it's a folder not a file
        if not os.path.isfile(path):
            loghandler.write_log(self.LOG_FILE, f"IMPORT ERROR: NO FILE SELECTED: '{path}';")
            return False

        # get data
        data = {}
        try:
            with open(path, 'r', encoding='utf-8', errors='replace') as f:
                data = json.load(fp=f)
        except Exception as read_dict_err:
            err_msg = f"IMPORT JSON READ FILE ERROR: {str(read_dict_err)}"
            loghandler.write_log(self.LOG_FILE, err_msg, print_log=True)
            return False

        # import data
        if data:
            DataManagement().import_all(data)
        else:
            loghandler.write_log(self.LOG_FILE, f"IMPORT ERROR: Read file error, either no content or ")
            return False

        loghandler.write_log(self.LOG_FILE, f"IMPORTED DATA from file: '{path}'", print_log=True)
        return True

    def import_exit_manager(self, *args):
        """ Called when the user reaches the root of the directory tree """

        self.import_manager_open = False
        self.import_file_manager.close()

    # endregion


class CreateCategoryDialog(MDBoxLayout):
    """ Dialog for creating a new category. """
    pass


class CheckboxItemsDialog(MDDialog):
    """ Dialog with checkboxes """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_all_checked_items(self) -> list:

        checked_items = []

        try:
            for item in self.items:
                # if item is checked add to deletion list
                if item.ids['check'].active:
                    checked_items.append(item.text)

        except:
            return []

        return checked_items

    def update_items(self, items: list) -> None:
        self.ids.box_items.clear_widgets()
        self.items = items
        self.create_items()

    def create_items(self) -> None:

        if not self.text:
            # add here try and except
            try:
                self.ids.container.remove_widget(self.ids.text)
            except:
                pass
            height = 0
        else:
            try:
                height = self.ids.text.height
            except:
                height = 0

        for item in self.items:
            if issubclass(item.__class__, BaseListItem):
                height += item.height  # calculate height contents
                self.edit_padding_for_item(item)
                self.ids.box_items.add_widget(item)

        if height > Window.height:
            self.ids.scroll.height = self.get_normal_height()
        else:
            self.ids.scroll.height = height


class DeleteCategoryCheckboxItemsDialog(CheckboxItemsDialog):

    def __init__(self,  **kwargs):

        super().__init__(**kwargs)





class DeleteCategoryDialogItem(OneLineAvatarIconListItem):
    """ Category item in delete category dialog. """

    divider = None

    @classmethod
    def set_icon(cls, instance_check):
        # switch check
        instance_check.active = not instance_check.active
