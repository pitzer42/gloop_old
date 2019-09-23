from gloop.web.server import (
    create_game_app,
    start_game_app
)

from examples.mtg.entities.loop import mtg_game_loop


if __name__ == '__main__':
    app = create_game_app(game_loop=mtg_game_loop)
    start_game_app(app)