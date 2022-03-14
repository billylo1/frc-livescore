from .LivescoreCommon import LivescoreCommon


class Livescore2020(LivescoreCommon):
    def __init__(self, **kwargs):
        super(Livescore2020, self).__init__(2020, **kwargs)
