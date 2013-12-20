from clld.web.maps import ParameterMap, Map


class FeatureMap(ParameterMap):
    def get_options(self):
        return {'icon_size': 20, 'hash': True}


class LanguagesMap(Map):
    def get_options(self):
        return {'icon_size': 20, 'hash': True}


def includeme(config):
    config.register_map('parameter', FeatureMap)
    config.register_map('languages', LanguagesMap)
