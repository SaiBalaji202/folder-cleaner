import functools
import operator


class Utils(object):
    @staticmethod
    def get_dict_value(d, keys):
        """
        Get value of a dictionary from a list of keys

        d => Dictionary
        keys => list of keys.  E.g. ['Program', 'Python'] = d['Program']['Python']
        """
        return functools.reduce(operator.getitem, keys, d)

    @staticmethod
    def set_dict(d, keys, value):
        """
            Set Value for a Dictionary

            d => Dictionary
            keys => list of keys
            value => Value to set
            E.g. set_dict(d, ['Program', 'Python'], '.py') => d['Program']['Python'] = '.py'
        """
        Utils.get_dict_value(d, keys[:-1])[keys[-1]] = value

    @staticmethod
    def replace_white_space(word, replace_word='_'):
        """
            Replace all white space within a string to a replace_word

            word => string to replace
            replace_word => replacement string.  Default replacement string is '_'
        """
        return word.replace(' ', replace_word)

    @staticmethod
    def fetch_substring(word, upto):
        """
            Fetch substring of a word upto some string.  If the specified upto string is not there inside the string, returns the whole string

            word => string to get a sub-string
            upto => string, which sets a upto limit for sub-string

            E.g. fetch_substring('Balaji', 'l') => 'Ba'
                fetch_substring('Balaji', 'z') => 'Balaji'
        """
        index = word.find(upto)
        if index != -1:
            word = word[:index]
        return word
