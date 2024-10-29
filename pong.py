from rich.segment import Segment
from textual import events
from textual.app import App, ComposeResult, RenderResult
from textual.containers import Container
from textual.geometry import Offset
from textual.strip import Strip
from textual.widget import Widget
from textual.widgets import Static


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

    dx = 1

    def render(self) -> RenderResult:
        return ""


class Court(Container):
    DEFAULT_CSS = """
    Court {
        layout: horizontal;
        width: 48;
        height: 25;
        border: wide #C2C3C7;
    }
    """

    def render_line(self, y: int) -> Strip:
        if y % 2:
            return Strip.blank(self.size.width)
        segments = [Segment(" " * (self.size.width // 2 - 1)), Segment("┃")]
        return Strip(segments)


class Scoreboard(Container):
    DEFAULT_CSS = """
    Scoreboard {
        layout: horizontal;
        width: 48;
        height: 1;

        Static {
            width: 1fr;
            text-align: center;
        }

        #player-points {
            color: #29ADFF;
        }

        #computer-points {
            color: #FF004D;
        }
    }
    """

    def __init__(
        self,
        player_points: int,
        computer_points: int,
    ) -> None:
        super().__init__()
        self.player_points = player_points
        self.computer_points = computer_points

    def compose(self) -> ComposeResult:
        yield Static(str(self.player_points), id="player-points")
        yield Static(str(self.computer_points), id="computer-points")


class PongGame(App):
    CSS = """
    Screen {
        border: none;
    }
    """

    key: str | None = None

    player_points = 0
    computer_points = 0

    def compose(self) -> ComposeResult:
        yield Scoreboard(self.player_points, self.computer_points)
        with Court():
            yield Player()
            yield Ball()
            yield Computer()

    def on_mount(self) -> None:
        self.set_interval(1 / 30, self.update)

    async def update(self) -> None:
        court = self.query_one(Court)
        player = self.query_one(Player)
        ball = self.query_one(Ball)
        computer = self.query_one(Computer)

        # Player controls
        if self.key == "up" and player.offset.y > 0:
            player.offset -= Offset(0, 1)
        elif (
            self.key == "down"
            and (player.offset.y + player.size.height) < court.size.height
        ):
            player.offset += Offset(0, 1)

        # Collide with computer
        if ball.dx > 0 and ball.offset.x >= computer.offset.x:
            ball.dx = -(ball.dx)

        # Collide with player
        if (
            ball.dx < 0
            and ball.offset.x <= player.offset.x
            and ball.offset.y >= player.offset.y
            and (ball.offset.y + ball.size.height)
            <= (player.offset.y + player.size.height)
        ):
            ball.dx = -(ball.dx)

        # Score
        if ball.offset.x + ball.size.width < 0:
            self.computer_points += 1
            await self.recompose()

        # Ball movement
        ball.offset += Offset(ball.dx, 0)

        # Reset the key
        self.key = None

    def on_key(self, event: events.Key) -> None:
        self.key = event.key


if __name__ == "__main__":
    game = PongGame(ansi_color=True)
    game.run(inline=True)
