"""Simple Pong game implemented using Python's turtle graphics module.

Run this module directly to start the game. Controls:
- Player A (left paddle): 'w' moves up, 's' moves down.
- Player B (right paddle): Up arrow moves up, Down arrow moves down.
"""

import turtle
from dataclasses import dataclass


@dataclass
class Paddle:
    """A paddle controlled by a player."""

    turtle: turtle.Turtle
    move_distance: int = 20

    def move_up(self) -> None:
        y = self.turtle.ycor() + self.move_distance
        if y > 250:
            y = 250
        self.turtle.sety(y)

    def move_down(self) -> None:
        y = self.turtle.ycor() - self.move_distance
        if y < -250:
            y = -250
        self.turtle.sety(y)


@dataclass
class Ball:
    """The ball that bounces between the paddles."""

    turtle: turtle.Turtle
    dx: float = 0.2
    dy: float = -0.2

    def move(self) -> None:
        self.turtle.setx(self.turtle.xcor() + self.dx)
        self.turtle.sety(self.turtle.ycor() + self.dy)

    def bounce_y(self) -> None:
        self.dy *= -1

    def bounce_x(self) -> None:
        self.dx *= -1

    def reset(self) -> None:
        self.turtle.goto(0, 0)
        self.bounce_x()


def create_paddle(position: tuple[int, int]) -> Paddle:
    paddle_turtle = turtle.Turtle()
    paddle_turtle.speed(0)
    paddle_turtle.shape("square")
    paddle_turtle.color("white")
    paddle_turtle.shapesize(stretch_wid=5, stretch_len=1)
    paddle_turtle.penup()
    paddle_turtle.goto(position)
    return Paddle(paddle_turtle)


def create_ball() -> Ball:
    ball_turtle = turtle.Turtle()
    ball_turtle.speed(0)
    ball_turtle.shape("circle")
    ball_turtle.color("white")
    ball_turtle.penup()
    ball_turtle.goto(0, 0)
    return Ball(ball_turtle)


def create_scoreboard() -> turtle.Turtle:
    scoreboard = turtle.Turtle()
    scoreboard.speed(0)
    scoreboard.color("white")
    scoreboard.penup()
    scoreboard.hideturtle()
    scoreboard.goto(0, 260)
    scoreboard.write("Player A: 0  Player B: 0", align="center", font=("Courier", 20, "normal"))
    return scoreboard


def main() -> None:
    # Set up the screen
    window = turtle.Screen()
    window.title("Pong by Turtle")
    window.bgcolor("black")
    window.setup(width=800, height=600)
    window.tracer(0)

    paddle_a = create_paddle((-350, 0))
    paddle_b = create_paddle((350, 0))
    ball = create_ball()
    scoreboard = create_scoreboard()

    score_a = 0
    score_b = 0

    # Keyboard bindings
    window.listen()
    window.onkeypress(paddle_a.move_up, "w")
    window.onkeypress(paddle_a.move_down, "s")
    window.onkeypress(paddle_b.move_up, "Up")
    window.onkeypress(paddle_b.move_down, "Down")

    while True:
        window.update()

        ball.move()

        # Border checking
        if ball.turtle.ycor() > 290:
            ball.turtle.sety(290)
            ball.bounce_y()

        if ball.turtle.ycor() < -290:
            ball.turtle.sety(-290)
            ball.bounce_y()

        if ball.turtle.xcor() > 390:
            ball.reset()
            score_a += 1
            scoreboard.clear()
            scoreboard.write(
                f"Player A: {score_a}  Player B: {score_b}",
                align="center",
                font=("Courier", 20, "normal"),
            )

        if ball.turtle.xcor() < -390:
            ball.reset()
            score_b += 1
            scoreboard.clear()
            scoreboard.write(
                f"Player A: {score_a}  Player B: {score_b}",
                align="center",
                font=("Courier", 20, "normal"),
            )

        # Paddle and ball collisions
        if (
            340 < ball.turtle.xcor() < 350
            and paddle_b.turtle.ycor() - 50 < ball.turtle.ycor() < paddle_b.turtle.ycor() + 50
        ):
            ball.turtle.setx(340)
            ball.bounce_x()

        if (
            -350 < ball.turtle.xcor() < -340
            and paddle_a.turtle.ycor() - 50 < ball.turtle.ycor() < paddle_a.turtle.ycor() + 50
        ):
            ball.turtle.setx(-340)
            ball.bounce_x()


if __name__ == "__main__":
    main()
