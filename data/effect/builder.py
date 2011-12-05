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

from eos import const
from .info import EffectInfo

class Modifier(object):
    """
    Internal for eval object, stores meaningful elements of expression tree temporarily
    """
    def __init__(self):
        # Type of modification
        self.type = None
        self.operation = None
        self.targetAttributeId = None
        self.sourceAttributeId = None

class InfoBuilder(object):
    """
    EffectInfo is responsible for converting two trees (pre and post) of Expression objects (which
    aren't directly useful to us) into EffectInfo objects which can then be used as needed.
    """
    def __init__(self):
        self.infos = []

    def build(self, base):
        """
        Go through both trees and compose our EffectInfos
        """
        # Validation: detect stubs, if a stub is found, return an empty list
        infos = self.infos
        if base.operand == const.opndDefInt and int(base.value) == 1:
            return infos

        try:
            print("Building expression tree with base {}".format(base.id))
            self.__generic(base)
        except:
            del self.infos[:]
            print("Error building expression tree with base {}".format(base.id))

        for info in self.infos:
            if info.validate() is not True:
                del self.infos[:]
                print("Error validating one of the infos of expression tree with base {}".format(base.id))
                break

        return self.infos

    # Top-level methods - combining, routing, etc
    def __generic(self, element):
        """Generic entry point, used if we expect passed element to be meaningful"""
        if element.operand in const.opndInfoMap:
            self.__makeInfo(element)
        else:
            genericOpnds = {const.opndSplice: self.__splice}
            genericOpnds[element.operand](element)

    def __splice(self, element):
        """Reference two expressions from self"""
        self.__generic(element.arg1)
        self.__generic(element.arg2)

    def __makeInfo(self, element):
        """Make info according to passed data"""
        info = EffectInfo()
        info.type = const.opndInfoMap[element.operand]
        self.__optrTgt(element.arg1, info)
        info.sourceAttributeId = self.__getAttr(element.arg2)
        self.__applyLocation(info)
        self.infos.append(info)

    def __applyLocation(self, info):
        """Some info types have a fixed location they affect, apply it here"""
        pass

    def __optrTgt(self, element, info):
        """Join operator and target definition"""
        info.operation = self.__getOptr(element.arg1)
        tgtRouteMap = {const.opndItmAttr: self.__itmAttr,
                       const.opndGenAttr: self.__attr,
                       const.opndSrqAttr: self.__srqAttr,
                       const.opndGrpAttr: self.__grpAttr}
        tgtRouteMap[element.arg2.operand](element.arg2, info)

    def __itmAttr(self, element, info):
        """Join target item specification and target attribute"""
        itmGetterMap = {const.opndDefLoc: self.__loc,
                        const.opndLocGrp: self.__locGrp,
                        const.opndLocSrq: self.__locSrq}
        itmGetterMap[element.arg1.operand](element.arg1, info)
        info.targetAttributeId = self.__getAttr(element.arg2)

    def __attr(self, element, info):
        """Get attribute and stores it"""
        info.targetAttributeId = self.__getAttr(element.arg1)

    def __loc(self, element, info):
        """Get location and store it"""
        info.location = self.__getLoc(element)

    def __grpAttr(self, element, info):
        """Join target group and target attribute"""
        info.filter = self.__getGrp(element.arg1)
        info.targetAttributeId = self.__getAttr(element.arg2)

    def __srqAttr(self, element, info):
        """Join target skill requirement and target attribute"""
        info.filter = self.__getType(element.arg1)
        info.targetAttributeId = self.__getAttr(element.arg2)

    def __locGrp(self, element, info):
        """Join target location filter and group filter"""
        info.location = self.__getLoc(element.arg1)
        info.filter = self.__getGrp(element.arg2)

    def __locSrq(self, element, info):
        """Join target location filter and skill requirement filter"""
        info.location = self.__getLoc(element.arg1)
        info.filter = self.__getType(element.arg2)

    def __getOptr(self, element):
        """Helper for modifying expressions, defines operator"""
        return const.optrConvMap[element.value]

    def __getLoc(self, element):
        """Define location"""
        return const.locConvMap[element.value]

    def __getAttr(self, element):
        """Reference attribute via ID"""
        return element.attributeId

    def __getGrp(self, element):
        """Reference group via ID"""
        return element.groupId

    def __getType(self, element):
        """Reference type via ID"""
        return element.typeId
