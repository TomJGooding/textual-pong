from rich.segment import Segment
from textual.app import App, ComposeResult, RenderResult
from textual.containers import Container
from textual.strip import Strip
from textual.widget import Widget


class Player(Widget):
    DEFAULT_CSS = """
    Player {
        width: 2;
        height: 4;
        background: #29ADFF;
        offset: 2 9;
    }
    """

    def render(self) -> RenderResult:
        return ""


class Computer(Widget):
    DEFAULT_CSS = """
    Computer {
        width: 2;
        height: 4;
        background: #FF004D;
        offset: 38 9;
    }
    """

    def render(self) -> RenderResult:
        return ""


class Ball(Widget):
    DEFAULT_CSS = """
    Ball {
        width: 2;
        height: 1;
        background: #FFF1E8;
        offset: 19 11;
    }
    """

    def render(self) -> RenderResult:
        return ""


class Court(Container):
    DEFAULT_CSS = """
    Court {
        layout: horizontal;
        width: 48;
        height: 25;
        border: inner #C2C3C7;
    }
    """

    def render_line(self, y: int) -> Strip:
        if y % 2:
            return Strip.blank(self.size.width)
        segments = [Segment(" " * (self.size.width // 2 - 1)), Segment("┃")]
        return Strip(segments)


class PongGame(App):
    CSS = """
    Screen {
        border: none;
    }
    """

    def compose(self) -> ComposeResult:
        with Court():
            yield Player()
            yield Ball()
            yield Computer()


if __name__ == "__main__":
    game = PongGame(ansi_color=True)
    game.run(inline=True)
