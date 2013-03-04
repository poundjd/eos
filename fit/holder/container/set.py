#===============================================================================
# Copyright (C) 2011 Diego Duclos
# Copyright (C) 2011-2013 Anton Vorobyov
#
# This file is part of Eos.
#
# Eos is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Eos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Eos. If not, see <http://www.gnu.org/licenses/>.
#===============================================================================


from .base import HolderContainerBase


class HolderSet(HolderContainerBase):
    """
    Orderless container for holders.

    Positional arguments:
    fit -- fit, to which container is attached
    holderClass - class, which will be instantiated
    when new holders are generated by means of container.
    """

    def __init__(self, fit, holderClass):
        self.__set = set()
        HolderContainerBase.__init__(self, fit, holderClass)

    def add(self, thing):
        if thing in self.__set:
            return thing
        holder = self.new(thing)
        self.__set.add(holder)
        self._handleAdd(holder)
        return holder

    def remove(self, holder):
        if holder not in self.__set:
            raise KeyError(holder)
        self._handleRemove(holder)
        self.__set.remove(holder)

    def __iter__(self):
        return iter(self.__set)

    def __contains__(self, holder):
        return holder in self.__set

    def __len__(self):
        return len(self.__set)

