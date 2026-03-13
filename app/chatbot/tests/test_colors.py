from __future__ import annotations

from chatbot.colors import Color


class TestColor:
    def test_all_colors_are_ansi_escape_codes(self) -> None:
        for color in Color:
            assert color.value.startswith("\033[")

    def test_end_resets_formatting(self) -> None:
        assert Color.END.value == "\033[0m"

    def test_expected_members_exist(self) -> None:
        names = {c.name for c in Color}
        assert names == {"RED", "GREEN", "YELLOW", "BLUE", "MAGENTA", "CYAN", "END"}
