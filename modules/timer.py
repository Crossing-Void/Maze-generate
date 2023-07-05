from Tkinter_template.Assets.project_management import making_widget
from Tkinter_template.Assets.image import tk_image
import math
import time


class Timer:
    def __init__(self, app) -> None:
        self.app = app
        self.__time = None
        self.__change_music = [1, 1]
        self.__create_canvas()

    def __create_canvas(self):
        self.canvas = making_widget("Canvas")(self.app.dashboard, width=self.app.dashboard_side[0], height=int(self.app.dashboard_side[0]//2*0.85*24//17)+10,
                                              )
        self.canvas.grid()

    def __create_time(self, remain):
        self.canvas.delete('numbers')
        time = str(math.ceil(remain))
        l = len(time)
        width = self.app.dashboard_side[0]
        size = (width // l) if l > 1 else (width // 2)
        try:
            for i in range(l):
                self.canvas.create_image(width * (i+1) / (l+1), 0, anchor='n', tags=('numbers'), image=tk_image(
                    f'{time[i]}.png' if self.app.timerType.get() == 'blue' else f'{time[i]}.png', int(size*0.85), int(size*24*0.85//17), dirpath='images\\numbers'))
        except:
            pass

    def set_timer(self, level):
        match level:
            case "Easy" | "easy":
                self.times = self.app.levelEasy_2
            case "Medium" | "medium":
                self.times = self.app.levelMedium_2
            case "Hard" | "hard":
                self.times = self.app.levelHard_2
        self.__create_time(self.times.get())
        self.__time = time.time()

    def flush(self):
        if self.__time is None:
            return
        remain = self.times.get() - time.time() + self.__time
        self.__create_time(remain)
        if remain < self.times.get() * 0.7:
            if self.__change_music[0]:
                self.__change_music[0] = 0
                self.app.Musics.music = self.app.gameMusics_1.get()
        if remain < self.times.get() * 0.3:
            if self.__change_music[1]:
                self.__change_music[1] = 0
                self.app.Musics.music = self.app.gameMusics_2.get()
