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


class HolderContainerBase:
    """
    Base class for any containers which are intended
    to ease management of holders. Hides fit-specific
    logic under its hood, letting real containers (which
    should inherit it) implement just container type-
    specific logic.

    Positional arguments:
    fit -- fit, to which container is attached
    holderClass -- class, which will be instantiated
    when new holders are generated by means of container.
    """

    __slots__ = ('__fit', '__holderClass')

    def __init__(self, fit, holderClass):
        self.__fit = fit
        self.__holderClass = holderClass

    def new(self, value):
        """
        Create instance of holder (if needed) and return it.

        Positional arguments:
        value -- if integer, item is fetched using it
        as ID, and holder is instantiated based on this
        item; else, should be holder instance.

        Return value:
        Holder instance.
        """
        if isinstance(value, int):
            type_ = self.__fit._eos._cacheHandler.getType(value)
            holder = self.__holderClass(type_)
        else:
            holder = value
        return holder

    def _handleAdd(self, holder):
        """Shortcut for registration of holder in fit."""
        self.__fit._addHolder(holder)

    def _handleRemove(self, holder):
        """Shortcut for unregistration of holder in fit."""
        self.__fit._removeHolder(holder)
