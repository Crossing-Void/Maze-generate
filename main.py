from Tkinter_template.Assets.universal import parse_json_to_property
from Tkinter_template.Assets.project_management import create_menu
from Tkinter_template.Assets.music import Music
from Tkinter_template.base import Interface
from modules.maze_maker import MazeMaker
from modules.player import Player
from modules.timer import Timer
from modules.move import Move


class Main(Interface):
    def __init__(self, title: str, icon=None, default_menu=True):
        Interface.rate = 0.9
        super().__init__(title, icon, default_menu)
        parse_json_to_property(self, 'modules\\setting\main_setting.json')
        parse_json_to_property(self, 'modules\\setting\music.json')
        parse_json_to_property(self, 'modules\\setting\game.json')
        self.MazeMakers = MazeMaker(self)
        self.Players = Player(self)
        self.Moves = Move(self)
        self.Timers = Timer(self)
        self.Musics = Music()
        self.Musics.set_volume(self.volume.get())

        self.level = None
        self.number_position = {}

        self.__build_menu()

    def __build_menu(self):
        start_menu = create_menu(self.top_menu)
        self.top_menu.add_cascade(label="Start", menu=start_menu)
        select_level_menu = create_menu(start_menu)
        start_menu.add_cascade(label="Level", menu=select_level_menu)
        for level in ['Easy', 'Medium', 'Hard']:
            select_level_menu.add_command(
                label=level, command=lambda args=level: self.MazeMakers.set(args))
        self.top_menu.add_command(
            label='Focus', command=lambda: self.canvas.focus_set())

    def game_initialize(self):
        pass

    def game_start(self):
        # store postion here
        for id_ in self.canvas.find_withtag('numbers'):
            tags = self.canvas.gettags(id_)[1]
            self.number_position[tags] = self.canvas.coords(tags)
        self.canvas.delete('numbers')
        self.Musics.music = self.gameMusics_0.get()
        self.Players.create_image('right')
        self.Players.create_obstacle()
        self.Moves.bind_direction()
        self.Timers.set_timer(self.level)


if __name__ == '__main__':
    main = Main('Maze', 'maze.ico', False)
    main.dashboard['height'] = int(main.dashboard['height']) - 20
    main.dashboard_side = int(main.dashboard['width']), int(
        main.dashboard['height'])
    main.canvas['height'] = int(main.canvas['height']) - 20
    main.canvas_side = int(main.canvas['width']), int(main.canvas['height'])

    while True:
        main.canvas.update()
        main.Musics.judge()
        main.Timers.flush()
        main.Moves.sleep()
