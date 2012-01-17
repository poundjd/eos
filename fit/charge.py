#===============================================================================
# Copyright (C) 2011 Diego Duclos
# Copyright (C) 2011-2012 Anton Vorobyov
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


from eos.calc.info.info import InfoLocation
from eos.calc.mutableAttributeHolder import MutableAttributeHolder


class Charge(MutableAttributeHolder):
    """Represent ammo - crystals, probes, bombs, etc"""

    def __init__(self, invType):
        super().__init__(invType)
        # Holder-container, into which our charge holder is
        # "loaded"
        self.container = None

    @property
    def _location(self):
        return InfoLocation.space

    @property
    def _other(self):
        """Purely service property, used in fit registry"""
        return self.container
