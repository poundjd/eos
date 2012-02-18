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


from eos.const import State
from .register.capitalItem import CapitalItemRegister
from .register.maxGroup import MaxGroupFittedRegister, MaxGroupOnlineRegister, MaxGroupActiveRegister
from .register.resource import CpuRegister, PowerGridRegister, CalibrationRegister, DroneBayVolumeRegister, \
DroneBandwidthRegister
from .register.shipTypeGroup import ShipTypeGroupRegister
from .register.skillRequirement import SkillRequirementRegister
from .register.slotIndex import SubsystemIndexRegister, ImplantIndexRegister, BoosterIndexRegister
from .register.slotNumber import HighSlotRegister, MediumSlotRegister, LowSlotRegister, RigSlotRegister, \
SubsystemSlotRegister, TurretSlotRegister, LauncherSlotRegister


class RestrictionTracker:
    def __init__(self, fit):

        self.__cpuRegister = CpuRegister(fit)
        self.__powerGridRegister = PowerGridRegister(fit)
        self.__calibrationRegister = CalibrationRegister(fit)
        self.__droneBayVolumeRegister = DroneBayVolumeRegister(fit)
        self.__droneBandwidthRegister = DroneBandwidthRegister(fit)

        self.__highSlotRegister = HighSlotRegister(fit)
        self.__mediumSlotRegister = MediumSlotRegister(fit)
        self.__lowSlotRegister = LowSlotRegister(fit)
        self.__rigSlotRegister = RigSlotRegister(fit)
        self.__subsystemSlotRegister = SubsystemSlotRegister(fit)
        self.__turretSlotRegister = TurretSlotRegister(fit)
        self.__launcherSlotRegister = LauncherSlotRegister(fit)

        self.__subsystemIndexRegister = SubsystemIndexRegister()
        self.__implantIndexRegister = ImplantIndexRegister()
        self.__boosterIndexRegister = BoosterIndexRegister()

        self.__shipTypeGroupRegister = ShipTypeGroupRegister(fit)

        self.__capitalItemRegister = CapitalItemRegister(fit)

        self.__maxGroupFittedRegister = MaxGroupFittedRegister()
        self.__maxGroupOnlineRegister = MaxGroupOnlineRegister()
        self.__maxGroupActiveRegister = MaxGroupActiveRegister()

        self.__skillRequirementRegister = SkillRequirementRegister()

    def addHolder(self, holder):
        self.__calibrationRegister.registerHolder(holder)
        #self.__droneBayVolumeRegister.registerHolder(holder)

        self.__highSlotRegister.registerHolder(holder)
        self.__mediumSlotRegister.registerHolder(holder)
        self.__lowSlotRegister.registerHolder(holder)
        self.__rigSlotRegister.registerHolder(holder)
        self.__subsystemSlotRegister.registerHolder(holder)
        self.__turretSlotRegister.registerHolder(holder)
        self.__launcherSlotRegister.registerHolder(holder)

        self.__subsystemIndexRegister.registerHolder(holder)
        self.__implantIndexRegister.registerHolder(holder)
        self.__boosterIndexRegister.registerHolder(holder)

        self.__shipTypeGroupRegister.registerHolder(holder)

        self.__capitalItemRegister.registerHolder(holder)

        self.__maxGroupFittedRegister.registerHolder(holder)

        self.__skillRequirementRegister.registerHolder(holder)

    def removeHolder(self, holder):
        self.__calibrationRegister.unregisterHolder(holder)
        #self.__droneBayVolumeRegister.unregisterHolder(holder)

        self.__highSlotRegister.unregisterHolder(holder)
        self.__mediumSlotRegister.unregisterHolder(holder)
        self.__lowSlotRegister.unregisterHolder(holder)
        self.__rigSlotRegister.unregisterHolder(holder)
        self.__subsystemSlotRegister.unregisterHolder(holder)
        self.__turretSlotRegister.unregisterHolder(holder)
        self.__launcherSlotRegister.unregisterHolder(holder)

        self.__subsystemIndexRegister.unregisterHolder(holder)
        self.__implantIndexRegister.unregisterHolder(holder)
        self.__boosterIndexRegister.unregisterHolder(holder)

        self.__shipTypeGroupRegister.unregisterHolder(holder)

        self.__capitalItemRegister.unregisterHolder(holder)

        self.__maxGroupFittedRegister.unregisterHolder(holder)

        self.__skillRequirementRegister.unregisterHolder(holder)

    def stateSwitch(self, holder, oldState, newState):
        if (oldState is None or oldState < State.online) and (newState is not None and newState >= State.online):
            self.__cpuRegister.registerHolder(holder)
            self.__powerGridRegister.registerHolder(holder)
            self.__droneBandwidthRegister.registerHolder(holder)
            self.__maxGroupOnlineRegister.registerHolder(holder)
        elif (newState is None or newState < State.online) and (oldState is not None and oldState >= State.online):
            self.__cpuRegister.unregisterHolder(holder)
            self.__powerGridRegister.unregisterHolder(holder)
            self.__droneBandwidthRegister.unregisterHolder(holder)
            self.__maxGroupOnlineRegister.unregisterHolder(holder)
        if (oldState is None or oldState < State.active) and (newState is not None and newState >= State.active):
            self.__maxGroupActiveRegister.registerHolder(holder)
        elif (newState is None or newState < State.active) and (oldState is not None and oldState >= State.active):
            self.__maxGroupActiveRegister.unregisterHolder(holder)

    def validate(self):
        self.__cpuRegister.validate()
        self.__powerGridRegister.validate()
        self.__calibrationRegister.validate()
        self.__droneBayVolumeRegister.validate()
        self.__droneBandwidthRegister.validate()

        self.__highSlotRegister.validate()
        self.__mediumSlotRegister.validate()
        self.__lowSlotRegister.validate()
        self.__rigSlotRegister.validate()
        self.__subsystemSlotRegister.validate()
        self.__turretSlotRegister.validate()
        self.__launcherSlotRegister.validate()

        self.__subsystemIndexRegister.validate()
        self.__implantIndexRegister.validate()
        self.__boosterIndexRegister.validate()

        self.__shipTypeGroupRegister.validate()

        self.__capitalItemRegister.validate()

        self.__maxGroupFittedRegister.validate()
        self.__maxGroupOnlineRegister.validate()
        self.__maxGroupActiveRegister.validate()

        self.__skillRequirementRegister.validate()
