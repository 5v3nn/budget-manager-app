"""
Date Selector script, inspired by the MDDatePicker
"""

import datetime
from datetime import date
import calendar
import os

from kivy.lang import Builder
from kivy.properties import NumericProperty, ObjectProperty, ColorProperty, ListProperty, StringProperty, \
    BooleanProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.behaviors import FocusBehavior, ButtonBehavior
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivymd.theming import ThemableBehavior
from kivymd.uix import SpecificBackgroundColorBehavior
from kivymd.uix.behaviors import FakeRectangularElevationBehavior, CircularRippleBehavior
from kivymd.uix.button import MDIconButton
from kivymd.uix.dialog import BaseDialog
from kivymd.uix.label import MDLabel

with open(
        os.path.join("./assets/date_selector/date_selector.kv"), encoding="utf-8"
) as kv_file:
    Builder.load_string(kv_file.read())


class BaseDateSelector(
    BaseDialog,
    FakeRectangularElevationBehavior,
    SpecificBackgroundColorBehavior,
):
    """
    Base class for :class:`~kivymd.uix.picker.MDDatePicker` and
    :class:`~kivymd.uix.picker.MDTimePicker` classes.

    :Events:
        `on_save`
            Events called when the "OK" dialog box button is clicked.
        `on_cancel`
            Events called when the "CANCEL" dialog box button is clicked.
    """

    title_input = StringProperty("INPUT DATE")
    """
    Dialog title fot input date.

    .. code-block:: python

        MDDatePicker(title_input="INPUT DATE")

    .. image:: https://github.com/HeaTTheatR/KivyMD-data/raw/master/gallery/kivymddoc/md-date-picker-input-date.png
        :align: center

    :attr:`title_input` is an :class:`~kivy.properties.StringProperty`
    and defaults to `INPUT DATE`.
    """

    title = StringProperty("SELECT DATE")
    """
    Dialog title fot select date.

    .. code-block:: python

        MDDatePicker(title="SELECT DATE")

    .. image:: https://github.com/HeaTTheatR/KivyMD-data/raw/master/gallery/kivymddoc/md-date-picker-select-date.png
        :align: center

    :attr:`title` is an :class:`~kivy.properties.StringProperty`
    and defaults to `SELECT DATE`.
    """

    radius = ListProperty([7, 7, 7, 7])
    """
    Radius list for the four corners of the dialog.

    .. code-block:: python

        MDDatePicker(radius=[7, 7, 7, 26])

    .. image:: https://github.com/HeaTTheatR/KivyMD-data/raw/master/gallery/kivymddoc/md-date-picker-radius.png
        :align: center

    :attr:`radius` is an :class:`~kivy.properties.ListProperty`
    and defaults to `[7, 7, 7, 7]`.
    """

    primary_color = ColorProperty(None)
    """
    Background color of toolbar in (r, g, b, a) format.

    .. code-block:: python

        MDDatePicker(primary_color=get_color_from_hex("#72225b"))

    .. image:: https://github.com/HeaTTheatR/KivyMD-data/raw/master/gallery/kivymddoc/primary-color-date.png
        :align: center

    :attr:`primary_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    """

    accent_color = ColorProperty(None)
    """
    Background color of calendar/clock face in (r, g, b, a) format.

    .. code-block:: python

        MDDatePicker(
            primary_color=get_color_from_hex("#72225b"),
            accent_color=get_color_from_hex("#5d1a4a"),
        )

    .. image:: https://github.com/HeaTTheatR/KivyMD-data/raw/master/gallery/kivymddoc/accent-color-date.png
        :align: center

    :attr:`accent_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    """

    selector_color = ColorProperty(None)
    """
    Background color of the selected day of the month or hour in (r, g, b, a) format.

    .. code-block:: python

        MDDatePicker(
            primary_color=get_color_from_hex("#72225b"),
            accent_color=get_color_from_hex("#5d1a4a"),
            selector_color=get_color_from_hex("#e93f39"),
        )

    .. image:: https://github.com/HeaTTheatR/KivyMD-data/raw/master/gallery/kivymddoc/selector-color-date.png
        :align: center

    :attr:`selector_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    """

    text_weekday_color = ColorProperty(None)
    """
    Text color of weekday names in (r, g, b, a) format.

    .. image:: https://github.com/HeaTTheatR/KivyMD-data/raw/master/gallery/kivymddoc/md-date-picker-text-weekday-color.png
        :align: center

    :attr:`text_weekday_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    """

    text_toolbar_color = ColorProperty(None)
    """
    Color of labels for text on a toolbar in (r, g, b, a) format.

    .. code-block:: python

        MDDatePicker(
            primary_color=get_color_from_hex("#72225b"),
            accent_color=get_color_from_hex("#5d1a4a"),
            selector_color=get_color_from_hex("#e93f39"),
            text_toolbar_color=get_color_from_hex("#cccccc"),
        )

    .. image:: https://github.com/HeaTTheatR/KivyMD-data/raw/master/gallery/kivymddoc/text-toolbar-color-date.png
        :align: center

    :attr:`text_toolbar_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    """

    text_color = ColorProperty(None)
    """
    Color of text labels in calendar/clock face in (r, g, b, a) format.

    .. code-block:: python

        MDDatePicker(
            primary_color=get_color_from_hex("#72225b"),
            accent_color=get_color_from_hex("#5d1a4a"),
            selector_color=get_color_from_hex("#e93f39"),
            text_toolbar_color=get_color_from_hex("#cccccc"),
            text_color=("#ffffff"),
        )

    .. image:: https://github.com/HeaTTheatR/KivyMD-data/raw/master/gallery/kivymddoc/text-color-date.png
        :align: center

    :attr:`text_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    """

    text_current_color = ColorProperty(None)
    """
    Color of the text of the current day of the month/hour in (r, g, b, a) format.

    .. code-block:: python

        MDDatePicker(
            primary_color=get_color_from_hex("#72225b"),
            accent_color=get_color_from_hex("#5d1a4a"),
            selector_color=get_color_from_hex("#e93f39"),
            text_toolbar_color=get_color_from_hex("#cccccc"),
            text_color=("#ffffff"),
            text_current_color=get_color_from_hex("#e93f39"),
        )

    .. image:: https://github.com/HeaTTheatR/KivyMD-data/raw/master/gallery/kivymddoc/text-current-color-date.png
        :align: center

    :attr:`text_current_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    """

    text_button_color = ColorProperty(None)
    """
    Text button color in (r, g, b, a) format.

    .. code-block:: python

        MDDatePicker(
            primary_color=get_color_from_hex("#72225b"),
            accent_color=get_color_from_hex("#5d1a4a"),
            selector_color=get_color_from_hex("#e93f39"),
            text_toolbar_color=get_color_from_hex("#cccccc"),
            text_color=("#ffffff"),
            text_current_color=get_color_from_hex("#e93f39"),
            text_button_color=(1, 1, 1, .5),
        )

    .. image:: https://github.com/HeaTTheatR/KivyMD-data/raw/master/gallery/kivymddoc/text-button-color-date.png
        :align: center

    :attr:`text_button_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    """

    input_field_background_color = ColorProperty(None)
    """
    Background color of input fields in (r, g, b, a) format.

    .. code-block:: python

        MDDatePicker(
            primary_color=get_color_from_hex("#72225b"),
            accent_color=get_color_from_hex("#5d1a4a"),
            selector_color=get_color_from_hex("#e93f39"),
            text_toolbar_color=get_color_from_hex("#cccccc"),
            text_color=("#ffffff"),
            text_current_color=get_color_from_hex("#e93f39"),
            input_field_background_color=(1, 1, 1, 0.2),
        )

    .. image:: https://github.com/HeaTTheatR/KivyMD-data/raw/master/gallery/kivymddoc/input-field-background-color-date.png
        :align: center

    :attr:`input_field_background_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    """

    input_field_text_color = ColorProperty(None)
    """
    Text color of input fields in (r, g, b, a) format.

    Background color of input fields.

    .. code-block:: python

        MDDatePicker(
            primary_color=get_color_from_hex("#72225b"),
            accent_color=get_color_from_hex("#5d1a4a"),
            selector_color=get_color_from_hex("#e93f39"),
            text_toolbar_color=get_color_from_hex("#cccccc"),
            text_color=("#ffffff"),
            text_current_color=get_color_from_hex("#e93f39"),
            input_field_background_color=(1, 1, 1, 0.2),
            input_field_text_color=(1, 1, 1, 1),
        )

    .. image:: https://github.com/HeaTTheatR/KivyMD-data/raw/master/gallery/kivymddoc/input-field-background-color-date.png
        :align: center

    :attr:`input_field_text_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    """

    font_name = StringProperty("Roboto")
    """
    Font name for dialog window text.

    .. code-block:: python

        MDDatePicker(
            primary_color=get_color_from_hex("#72225b"),
            accent_color=get_color_from_hex("#5d1a4a"),
            selector_color=get_color_from_hex("#e93f39"),
            text_toolbar_color=get_color_from_hex("#cccccc"),
            text_color=("#ffffff"),
            text_current_color=get_color_from_hex("#e93f39"),
            input_field_background_color=(1, 1, 1, 0.2),
            input_field_text_color=(1, 1, 1, 1),
            font_name="Weather.ttf",

        )

    .. image:: https://github.com/HeaTTheatR/KivyMD-data/raw/master/gallery/kivymddoc/font-name-date.png
        :align: center

    :attr:`font_name` is an :class:`~kivy.properties.StringProperty`
    and defaults to `'Roboto'`.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type("on_save")
        self.register_event_type("on_cancel")

    def on_save(self, *args) -> None:
        """Events called when the "OK" dialog box button is clicked."""

        self.dismiss()

    def on_cancel(self, *args) -> None:
        """Events called when the "CANCEL" dialog box button is clicked."""

        self.dismiss()


class DateSelector(BaseDateSelector):
    """ Date Picker dialog widget

    # Inspired by the kivymd MDDatePicker class

    auto_dismiss=False,
    """

    day = NumericProperty()
    month = NumericProperty()
    year = NumericProperty()

    current_month = None

    _calendar_layout = ObjectProperty()
    _calendar_list = None
    _sel_day_widget = None
    # _sel_day_widget = ObjectProperty()

    _scale_calendar_layout = NumericProperty(1)
    _scale_year_layout = NumericProperty(0)
    _shift_dialog_height = NumericProperty(0)
    _input_date_dialog_open = BooleanProperty(False)
    _select_year_dialog_open = False
    _last_on_save_value = None

    def __init__(self, year=None, month=None, day=None, firstweekday=0, **kwargs):

        self.today = date.today()
        self.calendar = calendar.Calendar(firstweekday)
        self.year = year if year else self.today.year
        self.month = month if month else self.today.month
        self.day = day if day else self.today.day
        self._current_selected_date = (
            self.day,
            self.month,
            self.year,
        )

        # print(self.year, self.month, self.day)
        self._last_on_save_value = date(self.year, self.month, self.day)

        super(DateSelector, self).__init__(auto_dismiss=False, **kwargs)
        # self.theme_cls.bind(device_orientation=self.on_device_orientation)

        self.generate_list_widgets_days()
        self.update_calendar(self.year, self.month)

    def generate_list_widgets_days(self) -> None:
        """ Generate list of day widgets """

        calendar_list = []

        # generate weekday labels
        for day in self.calendar.iterweekdays():
            weekday_label = DateSelectorWeekdayLabel(
                text=calendar.day_name[day][0].upper(),
                owner=self,
            )
            weekday_label.font_name = self.font_name
            self._calendar_layout.add_widget(weekday_label)

        # generate selectable day widgets
        for i, j in enumerate(range(6 * 7)):  # 6 weeks, 7 days a week
            day_selectable_item = DateSelectorDaySelectableItem(
                index=i,
                owner=self,
                current_month=int(self.month),
                current_year=int(self.year),
            )
            calendar_list.append(day_selectable_item)
            self._calendar_layout.add_widget(day_selectable_item)

        # save calendar_list to the class scope variable
        self._calendar_list = calendar_list

    def set_select_widget(self, widget) -> None:
        """ Select DateSelectorDaySelectableItem

        :param widget: DateSelectorDaySelectableItem widget
        """

        # deselect already selected widget
        if self._sel_day_widget:
            self._sel_day_widget.is_selected = False

        # select this widget
        widget.is_selected = True
        self.day = int(widget.text)
        self._current_selected_date = (
            self.day,
            self.month,
            self.year
        )
        self._sel_day_widget = widget

    def set_select_widget_to_day(self, day: int):
        """ Set select widget to day and select it.

        :param day: set to day
        """

        # find and select the widget with the passed day
        try:
            dates = [x for x in self.calendar.itermonthdates(self.year, self.month)]
        except ValueError as e:
            if str(e) == "year is out of range":
                pass
        else:
            # for every date in the 6x7 month list
            for idx in range(len(self._calendar_list)):
                if idx <= len(dates) and dates[idx].month == self.month:
                    # find the one where the date is today
                    if dates[idx].day == day:
                        # select it
                        self.set_select_widget(self._calendar_list[idx])
                        break

    def reset_select_widget(self, day: int):
        """ Reset the select widget

        :param day: set to day
        """

        # reset the _sel_day_widget
        if self._sel_day_widget:
            self._sel_day_widget.is_selected = False
        self._sel_day_widget = None

        # reassign day
        self.set_select_widget_to_day(day)

        self._last_on_save_value = date(self.year, self.month, day)

    def change_month(self, operation: str) -> None:
        """
        Called when "chevron-left" and "chevron-right" buttons are pressed.
        Switches the calendar to the previous/next month.
        """

        operation = 1 if operation == "next" else -1
        month = (
            12
            if self.month + operation == 0
            else 1
            if self.month + operation == 13
            else self.month + operation
        )
        year = (
            self.year - 1
            if self.month + operation == 0
            else self.year + 1
            if self.month + operation == 13
            else self.year
        )
        self.update_calendar(year, month)

        # make sure to update the selected day doesn't show on a different month
        # it should be selected only on the month, where it's selected
        if self._current_selected_date[1] == self.month:
            # select right day item button
            self.set_select_widget_to_day(self.day)
        else:
            # deselect all date items
            for date_item in self._calendar_list:
                date_item.is_selected = False

    def update_calendar(self, year, month, set_default=False) -> None:
        """ Update the calendar for the given year and month. """

        # get dates
        try:
            dates = [x for x in self.calendar.itermonthdates(year, month)]
        except ValueError as e:
            if str(e) == "year is out of range":
                pass
        else:
            self.year, self.month = year, month

            # for every date in the 6x7 month list
            for idx in range(len(self._calendar_list)):

                # set current_month and _year
                self._calendar_list[idx].current_month = int(self.month)
                self._calendar_list[idx].current_year = int(self.year)

                # for the selectable items not in the month, make them empty, but keep the space of them
                if idx >= len(dates) or dates[idx].month != month:
                    self._calendar_list[idx].disabled = True
                    self._calendar_list[idx].text = ""
                # dates in the month
                else:
                    self._calendar_list[idx].disabled = False
                    self._calendar_list[idx].text = str(dates[idx].day)             # set the text to the day
                    self._calendar_list[idx].is_today = dates[idx] == self.today    # mark this icon as today if so

    def on_ok_button_pressed(self) -> None:
        """
        Called when the 'OK' button is pressed to confirm the date entered.
        """

        values = date(self.year, self.month, self.day)

        # save values
        self._last_on_save_value = values

        # subscribe to event
        self.dispatch(
            "on_save",
            values,
        )

    def on_cancel(self, *args) -> None:

        super().on_cancel(*args)

        # reset the calendar to the default
        if self._last_on_save_value:

            # update month if needed
            if self._last_on_save_value.month != self.month:
                # reset month to the month of the last selected date
                self.update_calendar(self._last_on_save_value.year, self._last_on_save_value.month)

            # reset day to the last selected day
            self.set_select_widget_to_day(self._last_on_save_value.day)


class DateSelectorWeekdayLabel(MDLabel):

    owner = ObjectProperty()


class DateSelectorDaySelectableItem(
    ThemableBehavior, CircularRippleBehavior, ButtonBehavior, AnchorLayout
):
    """A class that implements a list for choosing a day."""

    text = StringProperty()
    owner = ObjectProperty()
    is_today = BooleanProperty(False)
    is_selected = BooleanProperty(False)
    current_month = NumericProperty()
    current_year = NumericProperty()
    index = NumericProperty(0)

    def on_release(self):
        # if not other dialog boxes are open
        if not self.owner._input_date_dialog_open and not self.owner._select_year_dialog_open:
            # mark this date as selected
            self.owner.set_select_widget(self)


class SelectYearList(FocusBehavior, LayoutSelectionBehavior, RecycleGridLayout):
    """A class that implements a list for choosing a year."""


class DateSelectorIconButton(MDIconButton):
    pass
