"""
This script handles the entry view where the entries are displayed.
"""
# import kivy modules
from kivy.properties import (
    StringProperty,
    ListProperty,
    BooleanProperty,
    NumericProperty,
    ObjectProperty,
)
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import SlideTransition, NoTransition
from kivymd.app import MDApp
from kivymd.uix.behaviors import TouchBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton, MDIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu

# import scripts
import data_management
import loghandler
import re


# path to log file from main.pys view
LOG_FILE_ENTRY_VIEW = "./logs/entry_view.log"


class EntryView(MDScreen):
    """EntryView class"""

    # parent id of where to add the data table
    parent_id = (
        StringProperty()
    )  # will be assigned in the kv file in the _on_pre_entry method
    table_widths = ListProperty()
    table_header_names = ListProperty()

    # default display month
    default_display_month = StringProperty()  # will be assigned in the kv file

    # select month dropdown menu
    select_display_month_caller_id = "dropdown_select_month_button"
    menu_select_display_month = None
    _selected_display_month = None

    @staticmethod
    def get_default_display_month() -> str:
        """
        Call this function to get the default display month.

        This will get a list of available dates from the database, which are sorted ascending.
        So this function will return the last (newest) date in that list.

        :return:
        """

        try:
            return data_management.DataManagement().get_available_dates()[-1]
        except Exception as get_default_month_err:
            err_msg = (
                f"ERROR GET DEFAULT MONTH TO DISPLAY: {str(get_default_month_err)}"
            )
            loghandler.write_log(LOG_FILE_ENTRY_VIEW, err_msg)
            print(err_msg)
            return "Select Month"

    @staticmethod
    def clear_parent_children(parent_widget):
        """Delete children of widget."""
        if parent_widget.children:
            for child in parent_widget.children:
                print("debug: remove child: %s" % child)
                parent_widget.remove_widget(child)

    def show_data_table(self, display_month=""):
        def get_float(string):
            try:
                return float(string)
            except:
                return 0.0

        if not display_month:
            display_month = self.default_display_month

        # assign selected month
        self._selected_display_month = display_month
        self.ids[self.select_display_month_caller_id].text = display_month

        # get parent and clear it
        parent = self.ids[self.parent_id]
        # self.clear_parent_children(parent)

        # check if display_month has right format
        try:
            self.clear_parent_children(self.ids["error_parent"])

            if not re.match(r".{4}-.{2}", display_month):
                raise Exception(f"Invalid format for display_month = '{display_month}'")

        except Exception as format_err:
            err_msg = f"ERROR SHOW DATA TABLE FORMAT ERROR: {str(format_err)}"
            loghandler.write_log(LOG_FILE_ENTRY_VIEW, err_msg)
            print(err_msg)

            # add error widget
            self.ids["error_parent"].add_widget(
                MDLabel(
                    text=f"Could not retrieve entries from database.\n"
                    f"You may have to add a new entry or select a month to display entries."
                )
            )
            return None

        # get row data: [['<date>', '<item>', '<category>', '<cost>', '<rowid for button>'],...]
        row_data = data_management.DataManagement().get_entries_by_date(display_month)

        # add total costs
        row_data = row_data + [
            [
                "",
                "",
                "[b]Total:[/b]",
                f"{(sum([get_float(d[3]) for d in row_data])):.2f}",
                "",
            ]
        ]

        parent.show_entries(row_data, self)

    def delete_row(self, index: int):
        """
        Cal this function to delete an entry from the database.

        :param index: rowid of entry to delete
        :return:
        """

        if index < 0:
            return

        print(f"{index} deleted")
        # delete entry
        data_management.DataManagement().delete_entry(index)

        # refresh data table
        self.show_data_table(self.ids[self.select_display_month_caller_id].text)

    def create_menu_select_display_month(self):
        """
        Create menu dropdown to display the selection of available months to display in the data table.

        :return:
        """

        if not self.menu_select_display_month:
            # create dropdown menu
            self.menu_select_display_month = MDDropdownMenu(
                caller=self.ids[self.select_display_month_caller_id],
                # items=items,
                items=[],
                width_mult=2,
                border_margin=10,
                position="bottom",
                ver_growth="down",
                elevation=10,
            )

        # update items
        # define dropdown menu items
        items = [
            {
                "text": f"{month}",
                "viewclass": "OneLineListItem",
                "height": dp(54),
                "on_release": lambda x=month: self.on_menu_select_display_month(str(x)),
            }
            for month in data_management.DataManagement().get_available_dates()
        ]
        items.reverse()  # reverse, so the newest item is on top
        self.menu_select_display_month.items = items

        # if _selected_display_month is not in items anymore, get default one
        if self._selected_display_month:
            if self._selected_display_month not in items:
                self._selected_display_month = self.get_default_display_month()

        # logging
        loghandler.write_log(
            LOG_FILE_ENTRY_VIEW,
            f"Created dropdown menu; items: {self.menu_select_display_month.items};",
        )

    def on_menu_select_display_month(self, month: str):
        """
        This event is called when a dropdown item is selected.

        :param month: string of month of format 'yyyy-mm'
        :return:
        """

        self.menu_select_display_month.dismiss()  # close menu dropdown
        self.ids[
            self.select_display_month_caller_id
        ].text = month  # assign value of item to button text
        self.default_display_month = month  # assign value to this variable, so the next time the screen changes it won't get reset.
        self.show_data_table(month)  # show/update the data table


class EntryLabel(MDLabel):
    def __init__(self, text, size_hint, **kwargs):
        super().__init__(**kwargs)
        self.entry_label = MDLabel(
            text=text,
            size_hint=size_hint,
            markup=True,
            shorten=True,
            valign="center",
            **kwargs,
        )


# region data_table
class EntryEditDialog(MDBoxLayout):
    pass


class SelectableRecycleBoxLayout(FocusBehavior, RecycleBoxLayout):
    """Adds selection and focus behaviour to the view."""

    multiselect = False
    touch_multiselect = False


class RecycleDataRow(RecycleDataViewBehavior, GridLayout):
    # app = None
    # theme_class = None

    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    cols = 5

    entry_dialog = None

    # def __init__(self, **kwargs):
    #     super(RecycleDataRow, self).__init__(**kwargs)
    #
    #     # get running app
    #     self.app = MDApp.get_running_app()
    #     # get theme class
    #     self.theme_class = self.app.theme_cls
    #
    #     self.init_entry_edit_dialog()
    #
    # def init_entry_edit_dialog(self):
    #
    #     self.entry_dialog = MDDialog(
    #         title="",
    #         type="custom",
    #         auto_dismiss=False,
    #         content_cls=EntryEditDialog(),
    #         buttons=[
    #             MDFlatButton(
    #                 text="Cancel",
    #                 theme_text_color="Custom",
    #                 text_color=self.theme_class.primary_color,
    #                 on_release=lambda x: self.entry_dialog.dismiss(),
    #             ),
    #         ],
    #     )

    def refresh_view_attrs(self, rv, index, data):
        # print("refresh_view_attrs with data: %s" % data)
        self.index = index
        self.label_date_text = data["label_date"]["text"]
        self.label_item_text = data["label_item"]["text"]
        self.label_category_text = data["label_category"]["text"]
        self.label_cost_text = data["label_cost"]["text"]
        self.label_delete_text = data["label_delete"]["text"]
        if "rowid" in data["label_delete"]:
            self.label_delete_rowid = data["label_delete"]["rowid"]
        if "root_obj" in data["label_delete"]:
            self.root_obj = data["label_delete"]["root_obj"]

        return super(RecycleDataRow, self).refresh_view_attrs(rv, index, data)

    def delete_row(self, rowid):

        if rowid < 0:
            return

        print(f"{rowid} deleted")

        # delete entry
        data_management.DataManagement().delete_entry(rowid)

    # def open_entry_edit_dialog(self, root, rowid):
    #     print(f'Opening entry edit dialog for id {rowid}')
    #
    #     # todo entry edit dialog
    #     if self.entry_dialog is None:
    #         self.init_entry_edit_dialog()
    #
    #     self.entry_dialog.title = f"Edit: {root.label_item_text}"
    #     self.entry_dialog.content_cls.ids["test"].text = f"Cost: {root.label_cost_text}"
    #     self.entry_dialog.open()


class RVDataTable(RecycleView):

    root_obj = ObjectProperty()

    def __init__(self, **kwargs):
        super(RVDataTable, self).__init__(**kwargs)

    def show_entries(self, row_data: list, root_obj):
        self.root_obj = root_obj

        labels = [
            "label_date",
            "label_item",
            "label_category",
            "label_cost",
            "label_delete",
        ]

        # add header to data
        self.data = [
            {
                labels[0]: {"text": "[b]Date[/b]"},
                labels[1]: {"text": "[b]Item[/b]"},
                labels[2]: {"text": "[b]Category[/b]"},
                labels[3]: {"text": "[b]Cost[/b]"},
                labels[4]: {"text": "[b]Delete[/b]"},
            }
        ]

        # add row data to table
        for row in row_data:
            d = {}
            for label_i, row_i in zip(labels, enumerate(row)):

                d[label_i] = {"text": str(row_i[1])}

                if row_i[0] == 4:
                    try:
                        d[label_i] = {
                            "text": "edit",
                            "rowid": int(row_i[1]),
                            "root_obj": self.root_obj,
                        }
                    except:
                        d[label_i] = {"text": str(row_i[1])}

            # print('d: ', d)
            self.data.append(d)


class RVEntryEditButton(MDIconButton):
    rowid = NumericProperty()
    show_entries_func = None

    icon = "delete"
    # icon_size = 16
    disabled_color = (255, 255, 255, 0)
    line_width = 1


# endregion
