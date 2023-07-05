from Tkinter_template.Assets.image import tk_image
import os


class Player:
    def __init__(self, app) -> None:
        self.app = app

    def create_image(self, img, position: tuple = None):
        if img not in ['right', 'left', 'up', 'down']:
            raise ValueError(f'img shoulg be in: right, left, up, down')
        if position is None:
            a, b = self.app.number_position['numbers-0x0']
        else:
            a, b = position[0], position[1]

        x_diff = self.app.number_position['numbers-0x1'][0] - \
            self.app.number_position['numbers-0x0'][0]
        y_diff = self.app.number_position['numbers-1x0'][1] - \
            self.app.number_position['numbers-0x0'][1]

        filepath = self.app.playerImagePath.get()
        self.app.canvas.create_image(a, b, image=tk_image(
            f'{img}.png', int(min(x_diff*0.55, y_diff*0.55)), dirpath=filepath),
            tags=('player', 'player-image', f'player-image-{img}'))

        self.image_width = tk_image(
            f'{img}.png', int(min(x_diff*0.55, y_diff*0.55)), dirpath=filepath,
            get_object_only=True).width

    def create_obstacle(self):
        rate = self.app.obstacleInitialRate.get()
        a, b = self.app.number_position['numbers-0x0']
        self.app.canvas.create_rectangle(
            0, -5000, self.app.canvas_side[0], b-0.5 *
            self.image_width-rate*self.image_width,
            fill=self.app.obstacleColor.get(), outline=self.app.obstacleColor.get(),
            tags=('player', 'obstacle', 'obstacle-up'))
        self.app.canvas.create_rectangle(
            0, b+0.5*self.image_width+rate *
            self.image_width, self.app.canvas_side[0], self.app.canvas_side[1]+5000,
            fill=self.app.obstacleColor.get(), outline=self.app.obstacleColor.get(),
            tags=('player', 'obstacle', 'obstacle-down'))
        self.app.canvas.create_rectangle(
            -2000, 0, a-0.5*self.image_width-rate *
            self.image_width, self.app.canvas_side[1],
            fill=self.app.obstacleColor.get(), outline=self.app.obstacleColor.get(),
            tags=('player', 'obstacle', 'obstacle-left'))
        self.app.canvas.create_rectangle(
            a+0.5*self.image_width+rate *
            self.image_width, 0, self.app.canvas_side[0] +
            5000, self.app.canvas_side[1],
            fill=self.app.obstacleColor.get(), outline=self.app.obstacleColor.get(),
            tags=('player', 'obstacle', 'obstacle-right'))
