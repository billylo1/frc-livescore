from .LivescoreCommon import LivescoreCommon


class Livescore2022(LivescoreCommon):
    def __init__(self, **kwargs):
        super(Livescore2022, self).__init__(2022, **kwargs)
