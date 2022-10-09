"""
This script handles the screen where entries are added.

"""
from kivy.core.window import Window
# import kivy modules
from kivy.metrics import dp
from kivy.properties import BooleanProperty, NumericProperty, StringProperty, ListProperty
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFlatButton
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.textfield import MDTextField

# import modules
import datetime

# import scripts
import data_management
import loghandler


# path to log file from main.pys view
LOG_FILE_ENTRY_VIEW = "./logs/entry_add_view.log"


class EntryAddView(MDScreen):
    """Screen for adding a new entry"""

    # type
    default_entry_type_button_id = StringProperty()
    default_entry_type = 1  # 0: Income, 1: Expense
    add_entry_type = NumericProperty()  # get assigned in the kivy file

    # item
    item_input_id = StringProperty()

    # category dropdown menu
    select_category_caller_id = StringProperty()
    menu_select_category = None

    # date picker
    date_dialog = None
    date_picker_id = StringProperty()

    # earning or cost field label
    earning_or_cost_field_id = ListProperty()  # ['label_id', 'input_id']
    earning_or_cost_field_label_text_value = ListProperty()  # ['income_text', 'expense_text']


    def create_menu_select_category(self):
        """
        Create menu dropdown to select the category which will be submitted to create a new entry.

        :return:
        """

        # define dropdown menu items
        items = [
            {
                "text": f"{category}",
                "viewclass": "OneLineListItem",
                "height": dp(54),
                "on_release": lambda x=category: self.on_menu_select_category(str(x)),
            }
            for category in data_management.DataManagement().get_categories()
        ]

        # create dropdown menu
        self.menu_select_category = MDDropdownMenu(
            caller=self.ids[self.select_category_caller_id],
            items=items,
            width_mult=4,
            border_margin=10,
            position='bottom',
            ver_growth='down',
            elevation=10,
        )

        # logging
        loghandler.write_log(
            LOG_FILE_ENTRY_VIEW, f"Created dropdown menu to select category; items: {items};"
        )

    def on_menu_select_category(self, category: str):
        """
        This event is called when a dropdown item is selected.

        :param category name
        :return:
        """

        self.menu_select_category.dismiss()  # close menu dropdown
        self.ids[self.select_category_caller_id].text = category  # assign value of item to button text

    @staticmethod
    def get_default_category() -> str:
        """
        Call this function to get the default category.
        (This will be the first one in the list of the saved categories.)

        :return: string of default category name
        """

        return str(data_management.DataManagement().get_categories()[0])

    # region date_picker
    def date_picker_create(self):
        """ Create date picker"""

        # create date picker dialog
        self.date_dialog = MDDatePicker()
        # bind functions to it
        self.date_dialog.bind(on_save=self.date_picker_on_save, on_cancel=self.date_picker_on_cancel)

    def date_picker_show(self):
        """Open date picker."""

        if self.date_dialog is None:
            self.date_picker_create()

        # open date picker dialog
        self.date_dialog.open()

    def date_picker_on_save(self, instance, value, date_range):
        """
        Events called when the "OK" dialog box button is clicked.

        :type instance: <kivymd.uix.picker.MDDatePicker object>;
        :param value: selected date;
        :type value: <class 'datetime.date'>;
        :param date_range: list of 'datetime.date' objects in the selected range;
        :type date_range: <class 'list'>;
        """

        # set button text to date:
        self.ids[self.date_picker_id].text = str(value)
        self.date_dialog.dismiss()

    def date_picker_on_cancel(self, instance, value):
        """
        Events called when the "CANCEL" dialog box button is clicked.
        """

        # We don't really want to overwrite the potentially selected date with the default date.
        # set date picker button back to default:
        # self.ids[self.date_picker_id].text = self.get_default_date()
        self.date_dialog.dismiss()

    @staticmethod
    def get_default_date() -> str:
        """
        Call this function to get the default date.
        (This will be the current datetime date.)

        :return: str of current date in format 'yyyy-mm'
        """

        return str(datetime.datetime.now()).split(' ')[0]
    # endregion

    def set_earning_or_cost_fields(self):
        """ Set the related variables according to the type of the entry """

        # case 0: add income:
        if self.add_entry_type == 0:
            self.ids[self.earning_or_cost_field_id[0]].text = self.earning_or_cost_field_label_text_value[self.add_entry_type]
            self.ids[self.earning_or_cost_field_id[1]].is_negative = False
            self.ids[self.earning_or_cost_field_id[1]].on_text_validate()  # re-validate the input
        # case 1: add expense:
        elif self.add_entry_type == 1:
            self.ids[self.earning_or_cost_field_id[0]].text = self.earning_or_cost_field_label_text_value[self.add_entry_type]
            self.ids[self.earning_or_cost_field_id[1]].is_negative = True
            self.ids[self.earning_or_cost_field_id[1]].on_text_validate()  # re-validate the input
        # non generic case:
        else:
            self.ids[self.earning_or_cost_field_id[0]].text = 'Money Value:'

    def add_entry(self):
        """
        Add values from fields to the database.

        :return:
        """

        try:
            data_management.DataManagement().add_element(
                self.ids[self.select_category_caller_id].text,
                self.ids[self.item_input_id].text,
                self.ids[self.earning_or_cost_field_id[1]].text,
                self.ids[self.date_picker_id].text
            )
        except Exception as add_err:
            errmsg = f"ADD ENTRY ERROR: {str(add_err)}"
            loghandler.write_log(LOG_FILE_ENTRY_VIEW,
                                 f"Could not add entry to database. Check database log. Error message: {str(errmsg)}")
            print(errmsg)
            return

        loghandler.write_log(LOG_FILE_ENTRY_VIEW, f"Added entry to database. ")

        # Snackbar feedback that entry was added
        # create a quick snackbar as feedback that category was created
        Snackbar(text=f'Added new entry.',
                 snackbar_x='20dp',
                 snackbar_y='20dp',
                 size_hint_x=(Window.width - (dp(20) * 2)) / Window.width,
                 duration=1.5,
                 ).open()

    def reset_entry_fields(self):
        """
        Reset add entry view fields to default.

        :return:
        """

        self.add_entry_type = self.default_entry_type
        self.ids[self.default_entry_type_button_id].state = 'down'
        self.ids[self.item_input_id].text = ''
        self.ids[self.select_category_caller_id].text = self.get_default_category()
        self.ids[self.date_picker_id].text = self.get_default_date()
        self.date_dialog = None
        self.ids[self.earning_or_cost_field_id[1]].text = ''  # money value


class MyToggleButton(MDFlatButton, MDToggleButton):
    """Toggle Button"""

    # set background color, when button is not selected
    background_normal = "#020202"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # assign the primary color when the button is selected
        self.background_down = self.theme_cls.primary_color


class TextInputMaxLength(MDTextField):
    min_length = NumericProperty(0)
    max_length = NumericProperty(None)

    def __init__(self, *args, **kwargs):
        super(TextInputMaxLength, self).__init__(**kwargs)
        self.multiline = False

    # overwrite the insert_text method to make sure the length of the input is correct.
    def insert_text(self, string, from_undo=False):
        new_text = self.text + string  # current text + recent input text
        if new_text != "":
            # insert text only if text is not too long
            if self.min_length <= len(new_text) <= self.max_length:
                MDTextField.insert_text(self, string, from_undo=from_undo)


class MoneyValueInput(MDTextField):
    is_negative = BooleanProperty(False)

    def __init__(self, *args, **kwargs):
        super(MoneyValueInput, self).__init__(**kwargs)
        self.multiline = False

    def on_text_validate(self):
        """overwrite the insert_text method to make sure the length of the input is correct."""
        if self.text:  # check if text is not empty
            # put the value of the text field in given structure
            value = float(self.text)
            new_text = str(
                "{:.2f}".format(
                    # abs(value) if value < 0 else (-value if self.is_negative else +value)
                    -abs(value) if self.is_negative else abs(value)
                )
            )
            self.text = new_text

    def _on_focus(self, instance, value, *largs):
        # validate text when clicking outside of widget
        if self.text != "":
            # only need to validate if it has content
            self.on_text_validate()

        # call parent function, otherwise it doesn't work
        MDTextField._on_focus(self, instance, value, *largs)

