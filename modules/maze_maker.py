from Tkinter_template.Assets.extend_widget import EffectButton
from Tkinter_template.Assets.font import font_get, font_span
from tkinter.messagebox import showinfo
import random
import re


class MazeMaker:
    def __init__(self, app) -> None:
        self.app = app
        self.c = self.app.canvas
        self.cs = self.app.canvas_side

        self.numbers = {}  # for store number and position, use this judge done
        self.tags = []  # random choice tags

    def __vis_nums(self):
        '''
        for visulize number
        '''
        self.c.delete('numbers')
        maxS = max(self.numbers.values())
        si = font_span(str(maxS), self.width//2,
                       upper_bound=int(self.height*0.9))
        for cor, num in self.numbers.items():
            self.c.create_text(
                int(10 + self.width*(cor[1]+0.5)), int(10 + self.height*(cor[0]+0.5)), text=num, font=font_get(si),
                tags=('numbers', f'numbers-{cor[0]}x{cor[1]}'))

    def __execute(self):
        self.c.delete('start-btn')
        while True:
            # done
            if len(set(self.numbers.values())) == 1:
                showinfo('Done', 'It"s done')
                break

            t = random.choice(self.tags)
            self.c.itemconfig(t, fill=self.app.lineColor_1.get())
            self.c.update()
            # algorithm
            v = t.startswith('ver')
            tt = re.search(
                'vertical(\d+)x(\d+)' if v else 'horizontal(\d+)x(\d+)', t)
            x, y = int(tt.group(1)), int(tt.group(2))
            tN = self.numbers[(x, y)], self.numbers[(
                x, y+1) if v else (x+1, y)]
            if tN[0] == tN[1]:
                self.c.itemconfig(t, fill=self.app.lineColor_0.get())
                continue
            self.tags.remove(t)
            self.c.delete(t)
            res = random.randint(0, 1)
            if res == 0:
                for cor, num in self.numbers.copy().items():
                    if num == tN[1]:
                        self.numbers[cor] = tN[0]
            if res == 1:
                for cor, num in self.numbers.copy().items():
                    if num == tN[0]:
                        self.numbers[cor] = tN[1]
            # algorithm
            self.__vis_nums()

        self.app.game_start()

    def set(self, level):
        self.app.level = level
        match level:
            case "Easy" | "easy":
                row, column = self.app.levelEasy_0.get(), self.app.levelEasy_1.get()
            case "Medium" | "medium":
                row, column = self.app.levelMedium_0.get(), self.app.levelMedium_1.get()
            case "Hard" | "hard":
                row, column = self.app.levelHard_0.get(), self.app.levelHard_1.get()

        self.c.delete('all')
        self.numbers = {}
        self.tags = []
        self.app.Musics.music = None

        self.app.Moves.unbind_direction()

        self.width = (self.cs[0]) // row
        self.height = (self.cs[1]) // column

        # boundary
        self.c.create_rectangle(0, 0, *self.cs, tags=('wall'))
        for r in range(column):
            for c in range(row-1):
                self.c.create_line(self.width*(c+1), self.height*r,
                                   self.width*(c+1), self.height*(r+1), tags=(f'vertical{r}x{c}', 'wall'),
                                   fill=self.app.lineColor_0.get(), width=self.app.lineWidth.get())
                self.tags.append(f'vertical{r}x{c}')
        for r in range(column-1):
            for c in range(row):
                self.c.create_line(self.width*c, self.height*(r+1),
                                   self.width*(c+1), self.height*(r+1), tags=(f'horizontal{r}x{c}', 'wall'),
                                   fill=self.app.lineColor_0.get(), width=self.app.lineWidth.get())
                self.tags.append(f'horizontal{r}x{c}')

        count = 0
        for r in range(column):
            for c in range(row):
                count += 1
                self.numbers[(r, c)] = count

        self.__vis_nums()

        self.c.create_window(self.cs[0]//2, self.cs[1]//2,
                             window=EffectButton(('gold', 'black'), self.c,
                                                 text="Start", command=self.__execute, font=font_get(30)),
                             tags=('start-btn'))
