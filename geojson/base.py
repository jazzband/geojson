

class GeoJSON(object):

    def __init__(self, **extra):
        super(GeoJSON, self).__init__()
        self.type = type(self).__name__
        self.extra = extra

    @property
    def __geo_interface__(self):
        d = dict(**self.extra)
        if self.type != "GeoJSON":
            d.update(type=self.type)
        return d
