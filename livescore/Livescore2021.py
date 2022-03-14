from .LivescoreCommon import LivescoreCommon


class Livescore2021(LivescoreCommon):
    def __init__(self, **kwargs):
        super(Livescore2021, self).__init__(2021, **kwargs)
