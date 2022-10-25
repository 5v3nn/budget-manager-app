"""
This script handles the entry view where the entries are displayed.
"""
# import kivy modules
from kivy.properties import StringProperty
from kivy.uix.screenmanager import SlideTransition, NoTransition
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.scrollview import MDScrollView

# import scripts
import data_management
import loghandler
import re


# path to log file from main.pys view
LOG_FILE_ENTRY_VIEW = "./logs/entry_view.log"


class EntryView(MDScreen):
    """EntryView class"""

    # parent id of where to add the data table
    parent_id = StringProperty()  # will be assigned in the kv file in the _on_pre_entry method

    # default display month
    default_display_month = StringProperty()  # will be assigned in the kv file

    # select month dropdown menu
    select_display_month_caller_id = 'dropdown_select_month_button'
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
            err_msg = f"ERROR GET DEFAULT MONTH TO DISPLAY: {str(get_default_month_err)}"
            loghandler.write_log(LOG_FILE_ENTRY_VIEW, err_msg)
            print(err_msg)
            return 'Select Month'

    def show_data_table(self, display_month: str):
        """
        Show entries of given month in a MDDataTable widget,
        which will be added to the widget with the given parent_id.

        :param display_month: date of month to display in format YYYY-MM
        :return: None
        """

        # assign selected month
        self._selected_display_month = display_month

        def get_float(string):
            try:
                return float(string)
            except:
                return 0.0

        def get_row_index(possible_str):
            try:
                return int(possible_str)
            except:
                return -1

        def clear_parent_children(parent_widget):
            # delete parent children before adding new children
            if parent_widget.children:
                for child in parent_widget.children:
                    parent_widget.remove_widget(child)


        # get parent widget
        parent = self.ids[self.parent_id]

        # check if display_month has right format
        try:
            if not re.match(r'.{4}-.{2}', display_month):
                raise Exception(f"Invalid format for display_month = '{display_month}'")

        except Exception as format_err:
            err_msg = f"ERROR SHOW DATA TABLE FORMAT ERROR: {str(format_err)}"
            loghandler.write_log(LOG_FILE_ENTRY_VIEW, err_msg)
            print(err_msg)

            # add error label to parent
            clear_parent_children(parent)
            parent.add_widget(MDLabel(text=f"Could not retrieve entries from database.\n"
                                           f"You may have to add a new entry or select a month to display entries."))
            return None

        # define widths of columns
        widths = [(1.5 / 12, 1),
                  (4 / 12, 1),
                  (3 / 12, 1),
                  (1.8 / 12, 1),
                  (1.7 / 12, 1)]

        # define column data: ['<title>',...]
        column_data = [
            "[b]Date[/b]",
            "[b]Item[/b]",
            "[b]Category[/b]",
            "[b]Cost[/b]",
            "[b]Delete[/b]",
        ]

        # get row data: [['<date>', '<item>', '<category>', '<cost>', '<rowid for button>'],...]
        row_data = [
            [
                entry[0],
                entry[1],
                entry[2],
                f'{entry[3]}',
                entry[4],
            ] for entry in data_management.DataManagement().get_entries_by_date(display_month)
        ]
        # add total costs
        row_data = row_data + [
            ["", "", "[b]Total:[/b]", f"{(sum([get_float(d[3]) for d in row_data])):.2f}", '']
        ]

        # store here the data table
        scroll_view_container = MDScrollView()

        # create table widget shell
        grid_view_data_table = MDBoxLayout(
            orientation='vertical',
            adaptive_height=True,
            spacing=10,
            # padding=[0, 10, 0, 10],
        )

        # add column_data to grid table
        header_layout = MDBoxLayout(
            orientation='horizontal',
            adaptive_height=True,
            spacing=10,
        )
        for column_header, width_idx in zip(column_data, widths):
            header_layout.add_widget(EntryLabel(column_header, width_idx).entry_label)
        grid_view_data_table.add_widget(header_layout)

        # add row_data to grid table
        for row in row_data:
            row_text_align = ['left', 'left', 'left', 'right', 'right']

            # horizontal box layout for row
            row_layout = MDBoxLayout(
                orientation='horizontal',
                adaptive_height=True,
                spacing=15,
            )

            # add data, item, category, cost
            for column_id in range(len(column_data)-1):
                # print('add data', row[column_id], widths[column_id])
                row_layout.add_widget(EntryLabel(row[column_id], widths[column_id], halign=row_text_align[column_id]).entry_label)

            # add delete button if has del text
            if row[-1]:
                # del_b = MDRectangleFlatButton(text='-', size_hint=widths[-1])
                # del_b.bind(on_release=lambda x, i=get_row_index(row[-1]): self.delete_row(i))
                # del_b = MDFlatButton(text='Del', font_size=3, size_hint=widths[-1], on_release=lambda x: print(x))
                # del_b = MDTextButton(text='Del', font_size=3, size_hint=widths[-1], md_bg_color='#404040')
                del_b = MDIconButton(icon='delete', icon_size='16sp')
                del_b.bind(on_release=lambda x, i=get_row_index(row[-1]): self.delete_row(i))
                row_layout.add_widget(del_b)
            else:
                row_layout.add_widget(MDLabel(text='', size_hint=widths[-1]))

            grid_view_data_table.add_widget(row_layout)

        # clear parent
        clear_parent_children(parent)

        # add grid_view_data_table to scroll_view_container
        scroll_view_container.add_widget(grid_view_data_table)

        # add scroll_view_container to parent
        parent.add_widget(scroll_view_container)

    def delete_row(self, index: int):
        """
        Cal this function to delete an entry from the database.

        :param index: rowid of entry to delete
        :return:
        """

        if index < 0:
            return

        print(f'{index} deleted')
        # delete entry
        data_management.DataManagement().delete_entry(index)

        # refresh data table
        self.show_data_table(self.ids[self.select_display_month_caller_id].text)





        """
        def get_float(string):
            try:
                return float(string)
            except:
                return 0.0

        # get widget where the data table should be added
        parent = self.ids[self.parent_id]

        # set columns
        column_data = [
            ("Date", dp(20)),
            ("Item", dp(30)),
            ("Category", dp(17)),
            ("Cost", dp(15)),
        ]

        # get row data and add total costs
        row_data = data_management.DataManagement().get_entries_by_date(display_month)
        row_data = row_data + [
            ["", "", "Total:", str(sum([get_float(d[3]) for d in row_data])), '']
        ]

        # create data table widget
        data_table = MDDataTable(
            check=True,
            # anchor_y='center',
            use_pagination=False,
            column_data=column_data,
            row_data=row_data,
            sorted_on="Date",
            sorted_order="ASC",
            # elevation=20,
            rows_num=len(row_data),
        )
        data_table.bind(on_row_press=self.on_entry_press)

        # PARENT: remove existing child(ren) of parent widget -> 'update' table.
        # print(f'parent children: {parent.children}')
        if parent.children:
            for child in parent.children:
                parent.remove_widget(child)

        # add data table
        parent.add_widget(data_table)

        # logging
        loghandler.write_log(
            LOG_FILE_ENTRY_VIEW,
            f"Created DataTable; added to widget with id '{self.parent_id}'; column_data={column_data}; row_data={row_data};"
        )
        """

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
                width_mult=4,
                border_margin=10,
                position='bottom',
                ver_growth='down',
                elevation=10,
            )

        # update items
        # define dropdown menu items
        self.menu_select_display_month.items = [
            {
                "text": f"{month}",
                "viewclass": "OneLineListItem",
                "height": dp(54),
                "on_release": lambda x=month: self.on_menu_select_display_month(str(x)),
            } for month in data_management.DataManagement().get_available_dates()
        ]

        # logging
        loghandler.write_log(
            LOG_FILE_ENTRY_VIEW,
            f"Created dropdown menu; items: {self.menu_select_display_month.items};"
        )


    def on_menu_select_display_month(self, month: str):
        """
        This event is called when a dropdown item is selected.

        :param month: string of month of format 'yyyy-mm'
        :return:
        """

        self.menu_select_display_month.dismiss()  # close menu dropdown
        self.ids[self.select_display_month_caller_id].text = month  # assign value of item to button text
        self.default_display_month = month  # assign value to this variable, so the next time the screen changes it won't get reset.
        self.show_data_table(month)  # show/update the data table

    def open_settings_view(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'settings_view'
        self.manager.transition = SlideTransition()

    def open_dbsettings_view(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'dbsettings_view'
        self.manager.transition = SlideTransition()


class EntryLabel(MDLabel):
    def __init__(self, text, size_hint, **kwargs):
        super().__init__(**kwargs)
        self.entry_label = MDLabel(
            text=text,
            size_hint=size_hint,
            markup=True,
            shorten=True,
            valign='center',
            **kwargs
        )


