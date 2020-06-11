
class Utils:

    @staticmethod
    def remove_empty_and_none_values(dict_value):
        return {k: v for k, v in dict_value.items() if v not in [None, [], {}]}