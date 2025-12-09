from termitype.adapters.base import Adapter
from termitype.app.context import AppContext
from termitype.models.inputevent import InputEvent, InputEventType as IET
from termitype.models.presentation.presentation import Bar, Line, LineStyle, Presentation, Slide
from termitype.models.settings import SettingType, Settings
from termitype.screens.base import Screen
from typing import Dict, List, Optional, override, Self
from termitype.utils.color import Bg, Color, color

from termitype.utils.visuals import TOP_BAR_MENU
from termitype.utils.words import chunk_words, pad

class SettingsScreen(Screen):

    def __init__(self, context: AppContext):
        self.context = context
        self.adapter: Adapter = context.adapter

    @property
    def descs(self) -> Dict:
        return self.context.settings.descriptions()

    def update_setting(self, setting_index: int, setting_value: str) -> None:
        updated_descs = self.descs
        for t, values in self.descs.items():
            for k, setting in values.items():
                if setting["index"] == setting_index:
                    updated_descs[t][k]["value"] = setting_value

        self.context.settings = Settings.from_descriptions(updated_descs, self.context.settings)

    def get_setting(self, setting_index: int) -> Dict:
        for t, values in self.descs.items():
            for k, setting in values.items():
                if setting["index"] == setting_index:
                    tmp = self.descs[t][k]
                    tmp["name"] = k
                    return tmp
        return {}

    def get_first_setting_index_starting_with(self, prefix: str) -> int:
        for _, values in self.descs.items():
            for name, setting in values.items():
                if name.startswith(prefix):
                    return setting["index"]
        return self.setting_index

    @property
    def current_setting(self) -> Dict:
        return self.get_setting(self.setting_index)

    @override
    def restart(self) -> Self:
        self.__next_screen: Optional[Screen] = self
        self.setting_index = 0
        self.max_index = self.context.settings.max_setting_index
        self.setting_selected = False
        self.current_updating_text = ""
        self.has_typed_first_character = False
        self.searching = False
        self.searching_text = ""
        return self

    def render(self) -> Presentation:
        if not self.setting_selected:
            return self.render_settings_list() 
        else:
            return self.render_selecting_setting()

    def get_presentation(self, slide: Slide) -> Presentation:
        return Presentation(
            slide=slide,
            width=self.context.settings.width,
            height=self.context.settings.height,
            top_bar=TOP_BAR_MENU if self.context.settings.show_logo else Bar.EMPTY(),
            bottom_bar=Bar.MULTIPLE([
                ["[ESC] search", "[ENTER] select", "[k] up", "[d] down"],
                ["[p] profile", "[TAB] run", "[q] quit"]
            ], style=LineStyle.ALIGNED_RIGHT(gap=4, padding_right=2)),
            show_outline=self.context.settings.display_outline

        )

    def render_settings_list(self) -> Presentation:
        return self.get_presentation(Slide.ALIGNED_TOP(self.get_settings_lines(), padding=1))

    def render_selecting_setting(self) -> Presentation:
        return self.get_presentation(Slide.CENTERED(self.get_current_setting_updating_lines()))

    def get_current_setting_updating_lines(self) -> List[Line]:
        current_setting = self.current_setting
        value = self.current_updating_text
        if value == current_setting["value"]:
            value = color(value, fg=Color.BRIGHT_BLACK)
        options_line = Line.EMPTY()
        if current_setting["type"] == SettingType.OPTIONS:
            options_line = Line.CENTER([f"Available: {", ".join(current_setting["options"])}"])
        return [
            Line.CENTER([f"{current_setting["name"].upper()}: {current_setting["desc"]}"], padding=10),
            options_line,
            Line.EMPTY(),
            Line.CENTER([f"{value}│"], outlined=True)
        ]

    def get_settings_lines(self) -> List[Line]:
        lines = []
        if self.searching:
            lines.append(Line.CENTER([color("Search...", fg=Color.BRIGHT_BLACK) if self.searching_text == "" else self.searching_text], outlined=True))
            lines.append(Line.EMPTY())
        for t in self.descs:
            lines.append(Line.ALIGNED_LEFT([char for char in f"[{t.upper()}]"], 10, 1))

            for key, setting in self.descs[t].items():
                if key.lower().startswith(self.searching_text):
                    if self.setting_index == setting["index"]:
                        lines.append(Line.CENTER([f"{key}:", str(setting["value"])], padding=15, color=Color.WHITE, bg=Bg.BRIGHT_BLACK))
                        [
                            lines.append(
                                Line.ALIGNED_LEFT([pad(l, l=3, r=self.context.settings.width - 33 - len(l))], gap=0, padding_left=15, color=Color.WHITE, bg=Bg.BRIGHT_BLACK)
                            )
                            for l in chunk_words(setting["desc"], self.context.settings.width - 35)
                        ]
                    else:
                        lines.append(Line.CENTER([f"{key}:", str(setting["value"])], padding=15))

            lines.append(Line.EMPTY())

        return lines


    def handle_input(self, input_event: InputEvent):
        if not self.setting_selected:
            return self.no_setting_selected_handler(input_event)
        else:
            return self.setting_selected_handler(input_event)

    def no_setting_selected_handler(self, input_event: InputEvent):
        match input_event.type:
            case IET.ESCAPE:
                self.searching = not self.searching
                self.searching_text = ""
            case IET.TAB:
                self.__next_screen = self.context.run_screen.restart()
            case IET.ENTER:
                self.setting_selected = not self.setting_selected
                self.current_updating_text = self.current_setting["value"]

            case IET.BACKSPACE:
                self.searching_text = self.searching_text[:-1]

            case IET.CHAR: 
                if not self.searching:
                    match input_event.char:
                        case "q": self.__next_screen = None
                        case "j":
                            self.setting_index = min(self.setting_index + 1, self.max_index)
                        case "k":
                            self.setting_index = max(self.setting_index - 1, 0)
                        case "p":
                            self.__next_screen = self.context.dashboard_screen.restart()
                else:
                    self.searching_text += input_event.char
                    self.setting_index = self.get_first_setting_index_starting_with(self.searching_text)
            case _:
                pass

    def setting_selected_handler(self, input_event: InputEvent):
        match input_event.type:
            case IET.ESCAPE:
                self.setting_selected = False
            case IET.TAB:
                self.__next_screen = self.context.run_screen.restart()
            case IET.ENTER:
                self.update_setting(self.setting_index, self.current_updating_text)
                self.setting_selected = False
                self.has_typed_first_character = False
                self.searching = False
                self.searching_text = ""
            case IET.BACKSPACE:
                self.current_updating_text = self.current_updating_text[:-1]
            case IET.CHAR:
                if not self.has_typed_first_character:
                    self.has_typed_first_character = True
                    self.current_updating_text = ""
                self.current_updating_text += input_event.char


    def next_screen(self) -> Optional[Screen]:
        return self.__next_screen

