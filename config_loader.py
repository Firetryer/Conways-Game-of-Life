import pygame
import configparser


class ConfigEditor:
    def __init__(self):
        self.config = configparser.RawConfigParser()
        self.ConfigVideo = "video.ini"

    def video_config_load(self):
        videoDict = {}
        self.config.read(self.ConfigVideo)
        resolutionX = self.config.getint("video", 'resolution_x')
        resolutionY = self.config.getint("video", 'resolution_y')

        videoDict["resolution"] = (resolutionX, resolutionY)

        videoDict["fullscreen"] = self.config.getboolean("video", 'fullscreen')
        return videoDict

    def video_config_writer(self, reso, fs):
        self.config.read(self.ConfigVideo)
        self.config.set("video", 'resolution_x', reso[0])
        self.config.set("video", 'resolution_y', reso[1])
        self.config.set("video", 'fullscreen', fs)
        print(reso, fs)
        with open('config/video.ini', 'wb') as configfile:
            self.config.write(configfile)