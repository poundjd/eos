# ==============================================================================
# Copyright (C) 2011 Diego Duclos
# Copyright (C) 2011-2017 Anton Vorobyov
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
# ==============================================================================


from eos.const.eos import State
from eos.const.eve import AttrId
from eos.fit.item import Drone
from eos.fit.item import Ship
from eos.fit.message import ItemLoaded
from eos.fit.message import ItemUnloaded
from eos.fit.message import StatesActivatedLoaded
from eos.fit.message import StatesDeactivatedLoaded
from .base import BaseResourceRegister


class DroneBandwidthRegister(BaseResourceRegister):

    def __init__(self, msg_broker):
        BaseResourceRegister.__init__(self)
        self.__current_ship = None
        self.__resource_users = set()
        msg_broker._subscribe(self, self._handler_map.keys())

    @property
    def used(self):
        return sum(
            item.attrs[AttrId.drone_bandwidth_used]
            for item in self.__resource_users)

    @property
    def output(self):
        try:
            return self.__current_ship.attrs[AttrId.drone_bandwidth]
        except (AttributeError, KeyError):
            return None

    @property
    def _users(self):
        return self.__resource_users

    def _handle_item_loaded(self, msg):
        if isinstance(msg.item, Ship):
            self.__current_ship = msg.item

    def _handle_item_unloaded(self, msg):
        if msg.item is self.__current_ship:
            self.__current_ship = None

    def _handle_states_activated_loaded(self, msg):
        if (
            isinstance(msg.item, Drone) and
            State.online in msg.states and
            AttrId.drone_bandwidth_used in msg.item._type_attrs
        ):
            self.__resource_users.add(msg.item)

    def _handle_states_deactivated_loaded(self, msg):
        if isinstance(msg.item, Drone) and State.online in msg.states:
            self.__resource_users.discard(msg.item)

    _handler_map = {
        ItemLoaded: _handle_item_loaded,
        ItemUnloaded: _handle_item_unloaded,
        StatesActivatedLoaded: _handle_states_activated_loaded,
        StatesDeactivatedLoaded: _handle_states_deactivated_loaded}
