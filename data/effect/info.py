#===============================================================================
# Copyright (C) 2011 Diego Duclos
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

class EffectInfo(object):
    """
    The EffectInfo objects are the actual "Core" of eos,
    they are what eventually applies an effect onto a fit.
    Which causes modules to actually do useful(tm) things.
    They are typically generated by the InfoBuild class
    but nothing prevents a user from making some of his own and running them onto a fit
    """
    def __init__(self):
        self.type = None
        """
        Describes type of modification. Can be modification applied for some duration
        or modification applied single time in the beginning/end of the cycle.
        """

        self.gang = False
        """
        Flag identifying local/gang change.
        """

        self.location = None
        """
        Target location to change.
        """

        self.filterType = None
        """
        The filterType of the modification, is either filterAll, filterSkill or filterGroup
        """

        self.filterValue = None
        """
        The filter value of the modification. None for filterAll.
        Corresponding skill typeID or groupID for filterSkill & filterGroup respectively
        """

        self.operation = None
        """
        Which operation should be applied.
        """

        self.targetAttributeId = None
        """
        Which attribute will be affected by the operation on the target.
        """

        self.sourceAttributeId = None
        """
        Which source attribute will be used as modification value for the operation.
        """
