# -*- coding: utf-8 -*-
"""
token.py

Copyright 2014 Andres Riancho

This file is part of w3af, http://w3af.org/ .

w3af is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

w3af is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with w3af; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""


class DataToken(object):
    def __init__(self, name, value):
        self._name = name
        self._value = self._original_value = value

    def get_name(self):
        return self._name

    def get_value(self):
        return self._value

    def get_original_value(self):
        return self._original_value

    def set_value(self, new_value):
        self._value = new_value

    def __str__(self):
        return str(self._value)

    def __unicode__(self):
        return unicode(self._value)

    def __eq__(self, other):
        if isinstance(other, DataToken):
            return self.get_name() == other.get_name() and\
                   self.get_value() == other.get_value()

        elif isinstance(other, basestring):
            return self.get_value() == other

        elif other is None:
            return False
        else:
            raise RuntimeError('Can not compare %s with DataToken.' % other)

    def __reduce__(self):
        return self.__class__, (self._name, self._value), {}

    def __getattr__(self, attr):
        # see if this object has attr
        # NOTE do not use hasattr, it goes into infinite recursion
        if attr in self.__dict__:
            # this object has it
            return getattr(self, attr)

        # proxy to the wrapped object
        return getattr(self._value, attr)