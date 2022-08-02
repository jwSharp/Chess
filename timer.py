from winsound import MB_ICONQUESTION
import pygame
from config import *
import pygame
import sys
from config import *
from accessories import *
from player import *
from board import *


class Timer:
    def __init__(self, minute, extra):
        self.minute = minute
        self.second = 0
        self.format_time()

    def time_mechanics(self):
        self.minute = int(self.minute)
        self.second = int(self.second)
        if self.minute > 0:
            if self.second > 0:
                self.second -= 1
                return (self.minute, self.second)
            self.minute -= 1
            self.second = 59
            return (self.minute, self.second)
        if self.second > 0:
            self.second -= 1
            return (self.minute, self.second)
        return (0, 0)

    def format_time(self):
        if (self.minute, self.second) == (0, 0):
            self.timer = "Time's Up!"
            return
        if self.minute < 10:
            self.minute = str(0) + str(self.minute)
        if self.second < 10:
            self.second = str(0) + str(self.second)
        self.timer = f"{self.minute}:{self.second}"

    def update(self):
        self.time_mechanics()
        self.format_time()


    def draw(self, pos, size, screen):
        font = GET_FONT("Timer", size)
        timer = font.render(self.timer, True, (255, 215, 0))
        timer_rect = timer.get_rect()
        timer_rect.center = pos
        screen.blit(timer, timer_rect)
        
