# -*- coding: utf-8 -*-
"""
    lantz_core.features.util
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Tools to customize feature and help in their writings.

    :copyright: 2015 by Lantz Authors, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.

"""
from __future__ import (division, unicode_literals, print_function,
                        absolute_import)


# --- Methods composers -------------------------------------------------------

class MethodComposer(object):
    """Function like object used to compose feature methods calls.

    All methods to call are kept in an ordered dict ensuring that they will
    be called in the right order while allowing fancy insertion based on method
    id.

    """
    __slots__ = ('_names', '_methods')

    def __init__(self):
        self._methods = []
        self._names = []

    def prepend(self, name, method):
        """Prepend a method to existing ones.

        Parameters
        ----------
        name : unicode
            Id of the method. Used to find it when performing more complex
            operations on the list of methods.
        method : MethodType
            Method bound to a feature which will be called when this object
            will be called.

        """
        self._names.insert(0, name)
        self._methods.insert(0, method)

    def append(self, name, method):
        """Append a method to existing ones.

        Parameters
        ----------
        name : unicode
            Id of the method. Used to find it when performing more complex
            operations on the list of methods.
        method : MethodType
            Method bound to a feature which will be called when this object
            will be called.

        """
        self._names.append(name)
        self._methods.append(method)

    def add_after(self, anchor, name, method):
        """Add the given method after a given one.

        Parameters
        ----------
        anchor : unicode
            Id of the method after which to insert the given one.
        name : unicode
            Id of the method. Used to find it when performing more complex
            operations on the list of methods.
        method : MethodType
            Method bound to a feature which will be called when this object
            will be called.

        """
        i = self._names.index(anchor)
        self._names.insert(i+1, name)
        self._methods.insert(i+1, method)

    def add_before(self, anchor, name, method):
        """Add the given method before the specified one.

        Parameters
        ----------
        anchor : unicode
            Id of the method before which to insert the given one.
        name : unicode
            Id of the method. Used to find it when performing more complex
            operations on the list of methods.
        method : MethodType
            Method bound to a feature which will be called when this object
            will be called.

        """
        i = self._names.index(anchor)
        self._names.insert(i, name)
        self._methods.insert(i, method)

    def replace(self, name, method):
        """Replace an existing method by a new one.

        Parameters
        ----------
        name : unicode
            Id of the method of the method to replace.
        method : MethodType
            Method bound to a feature which will be called when this object
            will be called.

        """
        i = self._names.index(name)
        self._names[i] = name
        self._methods[i] = method

    def remove(self, name):
        """Remove a method.

        Parameters
        ----------
        name : unicode
            Id of the method to remove.

        """
        i = self._names.index(name)
        del self._names[i]
        del self._methods[i]

    def reset(self):
        """Empty the composer.

        """
        self._names = []
        self._methods = []


class PreGetComposer(MethodComposer):
    """Composer used for pre_get methods.

    """

    def __call__(self, driver):
        """Call mimicking a pre_get method and calling all assigned methods
        in order with the driver as only argument.

        """
        for m in self._methods:
            m(driver)


class PostGetComposer(MethodComposer):
    """Composer for post_get methods.

    """

    def __call__(self, driver, value):
        """Call mimicking a post_get method and calling all assigned methods
        in order. The value returned by each method is passed to the next one.

        """
        for m in self._methods:
            value = m(driver, value)
        return value


class PreSetComposer(MethodComposer):
    """Composer for pre_set methods.

    """

    def __call__(self, driver, value):
        """Call mimicking a pre_set method and calling all assigned methods
        in order. The value returned by each method is passed to the next one.

        """
        for m in self._methods:
            value = m(driver, value)
        return m


class PostSetComposer(MethodComposer):
    """Composer for post_set methods.

    """

    def __call__(self, driver, value, d_value, response):
        """Call mimicking a post_set method and calling all assigned methods
        in order.

        """
        for m in self._methods:
            value = m(driver, value, d_value, response)


# --- Customisation decorators ------------------------------------------------

def append(function):
    """
    """
    pass


def prepend(function):
    """
    """
    pass


def add_after(name):
    """
    """
    pass


def add_before(name):
    """
    """
    pass


def replace(name):
    """
    """
    pass
