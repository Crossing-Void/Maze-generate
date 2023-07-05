from Tkinter_template.Assets.soundeffect import play_sound
import time


class Move:
    def __init__(self, app) -> None:
        self.app = app
        self.__direction = 'right'
        self.arguments = {
            "speed": self.app.moveArgs_0.get(),
            "dt": self.app.moveArgs_1.get(),
            "acceleration": self.app.moveArgs_2.get()
        }

    def bind_direction(self):

        def left(e, c_=None):
            if self.__direction != 'left':
                self.change_direction('left')
                self.arguments['speed'] = self.app.moveArgs_0.get()
            else:
                self.acceleration()
            if not c_:
                c = self.arguments['speed'] * self.arguments['dt']
            else:
                c = c_
            self.app.canvas.move('player-image', -c, 0)
            self.app.canvas.move('obstacle-left', -c, 0)
            self.app.canvas.move('obstacle-right', -c, 0)
            self.collide(right, c)

        def right(e, c_=None):
            if self.__direction != 'right':
                self.change_direction('right')
                self.arguments['speed'] = self.app.moveArgs_0.get()
            else:
                self.acceleration()
            if not c_:
                c = self.arguments['speed'] * self.arguments['dt']
            else:
                c = c_
            self.app.canvas.move('player-image', c, 0)
            self.app.canvas.move('obstacle-left', c, 0)
            self.app.canvas.move('obstacle-right', c, 0)
            self.collide(left, c)

        def up(e, c_=None):
            if self.__direction != 'up':
                self.change_direction('up')
                self.arguments['speed'] = self.app.moveArgs_0.get()
            else:
                self.acceleration()
            if not c_:
                c = self.arguments['speed'] * self.arguments['dt']
            else:
                c = c_
            self.app.canvas.move('player-image', 0, -c)
            self.app.canvas.move('obstacle-up', 0, -c)
            self.app.canvas.move('obstacle-down', 0, -c)
            self.collide(down, c)

        def down(e, c_=None):
            if self.__direction != 'down':
                self.change_direction('down')
                self.arguments['speed'] = self.app.moveArgs_0.get()
            else:
                self.acceleration()
            if not c_:
                c = self.arguments['speed'] * self.arguments['dt']
            else:
                c = c_
            self.app.canvas.move('player-image', 0, c)
            self.app.canvas.move('obstacle-up', 0, c)
            self.app.canvas.move('obstacle-down', 0, c)
            self.collide(up, c)

        def release(e):
            self.arguments['speed'] = self.app.moveArgs_0.get()

        self.app.canvas.bind('<Left>', left)
        self.app.canvas.bind('<Right>', right)
        self.app.canvas.bind('<Up>', up)
        self.app.canvas.bind('<Down>', down)
        self.app.canvas.bind('<KeyRelease>', release)

    def unbind_direction(self):
        self.app.canvas.unbind('<Left>')
        self.app.canvas.unbind('<Right>')
        self.app.canvas.unbind('<Up>')
        self.app.canvas.unbind('<Down>')
        self.app.canvas.unbind('<KeyRelease>')

    def collide(self, feedback_function, *args):
        a, b = self.app.canvas.coords('player-image')
        w = self.app.Players.image_width
        objs = self.app.canvas.find_overlapping(
            a-0.5*w, b-0.5*w, a+0.5*w, b+0.5*w)
        if len(objs) != 1:
            objs = list(objs)
            for x in objs[:]:
                if 'player' in self.app.canvas.gettags(x):
                    objs.remove(x)

            if 'wall' in self.app.canvas.gettags(objs[0]):
                play_sound(self.app.collideWall.get())
                feedback_function(None, *args)

    def change_direction(self, args):
        self.__direction = args
        tags = self.app.canvas.gettags(
            self.app.canvas.find_withtag('player-image'))[-1]
        now = tags[tags.rfind('-')+1:]
        if args == now:
            return
        else:
            self.app.Players.create_image(
                args, self.app.canvas.coords(f'player-image-{now}'))
            self.app.canvas.delete(f'player-image-{now}')

    def acceleration(self):
        if self.arguments['speed'] > self.app.moveMaxSpeed.get():
            return
        final_yspeed = self.arguments['speed'] +\
            self.arguments['acceleration'] *\
            self.arguments['dt']
        self.arguments['speed'] = final_yspeed

    def sleep(self):
        time.sleep(self.arguments['dt'])
