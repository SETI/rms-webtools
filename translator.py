################################################################################
# translator.py
#
# An abstract class and subclasses for mapping strings such as file paths to
# other information. It is implemented in several ways including Python
# dictionaries and regular expression/substitution pairs.
#
# Mark Showalter, PDS RMS Node, May 2017
################################################################################

import os
import re

class Translator(object):
    """Abstract class to define translators from a set of strings such as file
    names to associated information.
    """

    def __add__(self, other):
        return self.append(other)

    def __iadd__(self, other):
        return self.append(other)

################################################################################
################################################################################

class TranslatorBySequence(Translator):
    """Translator defined by a sequence of other translators."""

    TAG = 'SEQUENCE'

    def __init__(self, args):

        for arg in args:
            assert isinstance(arg, Translator)

        self.sequence = args

    def all(self, strings, strings_first=False):
        """Apply a translator to one or more strings, returning every unique
        result in priority order."""

        # Convert an individual string to a list
        if type(strings) == str:
            strings = [strings]

        # Initialize the set of results
        results = []

        # Two options for priority...

        if strings_first:                       # Try each string in order
            for string in strings:
                for translator in self.sequence:
                    partial_results = translator.all(string)
                    if partial_results:
                        for item in partial_results:
                            if item not in results:
                                results.append(item)

        else:                                   # Try each translator in order
            for translator in self.sequence:
                partial_results = translator.all(strings)
                if partial_results:
                    for item in partial_results:
                        if item not in results:
                            results.append(item)

        return results

    def first(self, strings, strings_first=False):
        """Apply a translator to one or more strings, returning the first
        result. Return None if no translation is found."""

        # Convert an individual string to a list
        if type(strings) == str:
            strings = [strings]

        # Two options for priority...

        if strings_first:                       # Try each string in order
            for string in strings:
                for translator in self.sequence:
                    result = translator.first(string)
                    if result is not None: return result

        else:                                   # Try each string in order
            for translator in self.sequence:
                result = translator.first(strings)
                if result is not None: return result

        return None

    def keys(self):
        """Return all of the keys."""

        key_list = []
        for translator in self.sequence:
            key_list.append(translator.keys())

        return key_list

    def values(self):
        """Return all of the values in the same order as keys()."""

        value_list = []
        for translator in self.sequence:
            value_list.append(translator.values())

        return value_list

    def prepend(self, translator):
        """Return a new translator with the given translator in front of this
        one."""

        if translator.TAG == 'NULL': return translator

        # If arg is also a sequence, merge
        if translator.TAG == self.TAG:
            return TranslatorBySequence(translator.sequence + self.sequence)

        # If arg matches class of first in sequence, merge
        if translator.TAG == self.sequence[0].TAG:
            new_translator = self.sequence[0].prepend(translator)
            if new_translator.TAG == translator.TAG:
                return TranslatorBySequence([new_translator] +
                                             self.sequence[1:])

        return TranslatorBySequence([translator, self])

    def append(self, translator):
        """Return a new translator with the given translator after this one.
        """

        if translator.TAG == 'NULL': return translator

        # If arg is also a sequence, merge
        if translator.TAG == 'SEQUENCE':
            return TranslatorBySequence(self.sequence + translator.sequence,
                                        self.key_priority)

        # If arg matches class of last in sequence, merge
        if translator.TAG == self.sequence[-1].TAG:
            new_translator = self.sequence[-1].append(translator)
            if new_translator.TAG == translator.TAG:
                return TranslatorBySequence(self.sequence[:-1] +
                                            [new_translator])

        return TranslatorBySequence([self, translator])

################################################################################
################################################################################

class TranslatorByDict(Translator):
    """Translator defined by a standard dictionary. Fast but inflexible.

    If the value is string containing "\1", that substring is replaced by the
    key.

    A second translator, if provided, translates strings into the keys used in
    the dictionary.
    """

    TAG = 'DICT'

    def __init__(self, arg, path_translator=None):

        assert isinstance(arg, dict)
        self.dict = arg
        self.path_translator = path_translator

    def all(self, strings, strings_first=False):
        """Apply a translator to one or more strings, returning every unique
        result in priority order.

        For this subclass, strings_first is ignored."""

        # Convert the strings to dictionary keys
        if self.path_translator is None:
            keys = strings
        else:
            keys = self.path_translator.all(strings)

        # Initialize the set of results
        results = []

        # Test keys in order
        for key in keys:
            if key in self.dict:
                result = self.dict[key]
                expanded = TranslatorByDict.expand(result, key)
                for result in expanded:
                    if result not in results:
                        results.append(result)

        return results

    def first(self, strings, strings_first=False):
        """Apply a translator to one or more strings, returning the first
        result. Return None if no translation is found."""

        # Convert the strings to dictionary keys, preserving order
        if self.path_translator is None:
            keys = strings
        else:
            keys = self.path_translator.all(strings)

        # Test keys in order
        for key in keys:
            if key in self.dict:
                result = self.dict[key]
                expanded = TranslatorByDict.expand(result, key)
                return expanded[0]

        return None

    @staticmethod
    def expand(results, key):

        if type(results) != list:
            results = [results]

        expanded = []
        for result in results:
            if type(result) == str:
                result = result.replace(r'\1', key)
            elif type(result) == tuple:
                items = []
                for item in result:
                    if type(item) == str:
                        item = item.replace(r'\1', key)
                    items.append(item)
                result = tuple(items)

            expanded.append(result)

        return expanded

    def keys(self):
        """Return all of the keys (in a vaguely sensible order)."""

        keylist = self.dict.keys()
        keylist.sort()
        return keylist

    def values(self):
        """Return all of the values in the same order as keys()."""

        keylist = self.keys()
        return [self.dict[k] for k in keylist]

    def prepend(self, translator):
        """Return a new translator with the given translator in front of this
        one."""

        if translator.TAG == 'NULL': return translator

        if translator.TAG == 'SEQUENCE':
            return translator.append(self)

        return TranslatorBySequence([translator, self])

    def append(self, translator):
        """Add a new translator after this one."""

        if translator.TAG == 'NULL': return translator

        if translator.TAG == 'SEQUENCE':
            return translator.prepend(self)

        return TranslatorBySequence([self, translator])

################################################################################
################################################################################

class TranslatorByRegex(Translator):
    """Translator defined by a list of (regex, value) tuples."""

    TAG = 'REGEX'

    def __init__(self, tuples):

        # Compile regular expressions if necessary
        compiled_tuples = []
        for items in tuples:
            if isinstance(items[0], str):
                if len(items) > 2:
                    regex = re.compile('^' + items[0] + '$', flags=items[1])
                else:
                    regex = re.compile('^' + items[0] + '$')

                compiled_tuples.append((regex, items[-1]))

            else:
                compiled_tuples.append(items)

        self.tuples = compiled_tuples

    def all(self, strings, strings_first=False):
        """Apply a translator to one or more strings, returning every unique
        value in priority order."""

        # Convert an individual string to a list
        if type(strings) == str:
            strings = [strings]

        # Initialize the list of results
        results = []

        # Two options for priority...
        if strings_first:                       # Try each string in order
            for string in strings:
                for (regex, replacement) in self.tuples:
                    expanded = TranslatorByRegex.expand(regex, string,
                                                               replacement)
                    for item in expanded:
                        if item not in results:
                            results.append(item)

        else:                                   # Try each regex in order
            for (regex, replacement) in self.tuples:
                for string in strings:
                    expanded = TranslatorByRegex.expand(regex, string,
                                                               replacement)
                    for item in expanded:
                        if item not in results:
                            results.append(item)

        return results

    def first(self, strings, strings_first=False):
        """Apply a translator to one or more strings, returning the first
        result. Return None if no translation is found."""

        # Convert an individual string to a list
        if type(strings) == str:
            strings = [strings]

        # Two options for priority...

        if strings_first:                       # Try each string in order
            for string in strings:
                for (regex, replacement) in self.tuples:
                    expanded = TranslatorByRegex.expand(regex, string,
                                                               replacement)
                    if expanded:
                        return expanded[0]

        else:                                   # Try each regex in order
            for (regex, replacement) in self.tuples:
                for string in strings:
                    expanded = TranslatorByRegex.expand(regex, string,
                                                               replacement)
                    if expanded:
                        return expanded[0]

        return None

    @staticmethod
    def expand(regex, string, replacements):
        """Handle substitutions in the cases where the replacement is a list, a
        string, or a tuple containing strings."""

        matchobj = regex.match(string)
        if matchobj is None: return []

        if type(replacements) != list:
            replacements = [replacements]

        results = []
        for replacement in replacements:

            # If replacement is a string, apply substitution
            if type(replacement) == str:
                results.append(matchobj.expand(replacement))

            # Deal with a tuple
            elif type(replacement) == tuple:
                items = []
                for item in replacement:
                    if type(item) == str:
                        items.append(matchobj.expand(item))
                    else:
                        items.append(item)

                results.append(tuple(items))

            # Anything else is unchanged
            else:
                results.append(replacement)

        return results

    def keys(self):
        """Return all of the keys."""

        return [t[0] for t in self.tuples]

    def values(self):
        """Return all of the values in the same order as keys()."""

        return [t[1] for t in self.tuples]

    def prepend(self, translator):
        """Return a new translator with the given translator in front of this
        one."""

        if translator.TAG == 'NULL': return translator

        if translator.TAG == self.TAG:
            return TranslatorByRegex(translator.tuples + self.tuples)

        if translator.TAG == 'SEQUENCE':
            return translator.append(self)

        return TranslatorBySequence([translator, self])

    def append(self, translator):
        """Add a new translator after this one."""

        if translator.TAG == 'NULL': return translator

        if translator.TAG == self.TAG:
            return TranslatorByRegex(self.tuples + translator.tuples)

        if translator.TAG == 'SEQUENCE':
            return translator.prepend(self)

        return TranslatorBySequence([self, translator])

################################################################################
################################################################################

class NullTranslator(Translator):
    """Translator that returns nothing."""

    TAG = 'NULL'

    def __init__(self):
        pass

    def all(self, strings, strings_first=False):
        """Apply a translator to one or more strings, returning every unique
        result."""

        return []

    def first(self, strings, strings_first=False):
        """Apply a translator to one or more strings, returning the first
        result. Return None if no translation is found."""

        return None

    def keys(self):
        """Return all of the keys."""

        return []

    def values(self):
        """Return all of the values in the same order as keys()."""

        return []

    def prepend(self, translator):
        """Return a new translator with the given translator in front of this
        one."""

        return translator

    def append(self, translator):
        """Return a new translator with the given translator after this one.
        """

        return translator

################################################################################
################################################################################

class SelfTranslator(Translator):
    """Translator that returns itself."""

    TAG = 'SELF'

    def __init__(self):
        pass

    def all(self, strings, strings_first=False):
        """Apply a translator to one or more strings, returning every unique
        result."""

        return strings

    def first(self, strings, strings_first=False):
        """Apply a translator to one or more strings, returning the first
        result. Return None if no translation is found."""

        return strings[0]

    def keys(self):
        """Return all of the keys."""

        return []

    def values(self):
        """Return all of the values in the same order as keys()."""

        return []

    def prepend(self, translator):
        """Return a new translator with the given translator in front of this
        one."""

        if translator.TAG == self.TAG: return self

        if translator.TAG == 'NULL': return self

        if translator.TAG == 'SEQUENCE':
            return translator.append(self)

        return TranslatorBySequence([translator, self])

    def append(self, translator):
        """Return a new translator with the given translator after this one.
        """

        if translator.TAG == self.TAG: return self

        if translator.TAG == 'NULL': return self

        if translator.TAG == 'SEQUENCE':
            return translator.prepend(self)

        return TranslatorBySequence([self, translator])

################################################################################
################################################################################
