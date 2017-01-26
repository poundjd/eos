# ===============================================================================
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
# ===============================================================================


from unittest.mock import Mock, call

from eos.const.eos import State
from eos.fit.item import ModuleHigh, Implant
from tests.stats.stat_testcase import StatTestCase


class TestStatsDamageDps(StatTestCase):

    def test_empty(self):
        stats_dps = self.ss.get_nominal_dps()
        self.assertIsNone(stats_dps.em)
        self.assertIsNone(stats_dps.thermal)
        self.assertIsNone(stats_dps.kinetic)
        self.assertIsNone(stats_dps.explosive)
        self.assertIsNone(stats_dps.total)
        self.assertEqual(len(self.log), 0)
        self.assert_stat_buffers_empty()

    def test_single(self):
        eve_type = self.ch.type_(type_id=1, attributes={})
        holder = self.make_item_mock(ModuleHigh, eve_type, state=State.active)
        self.add_holder(holder)
        holder_dps = Mock(em=1.2, thermal=2.3, kinetic=3.4, explosive=4.5, total=5.6)
        holder.get_nominal_dps.return_value = holder_dps
        stats_dps = self.ss.get_nominal_dps()
        self.assertAlmostEqual(stats_dps.em, 1.2)
        self.assertAlmostEqual(stats_dps.thermal, 2.3)
        self.assertAlmostEqual(stats_dps.kinetic, 3.4)
        self.assertAlmostEqual(stats_dps.explosive, 4.5)
        self.assertAlmostEqual(stats_dps.total, 11.4)
        self.remove_holder(holder)
        self.assertEqual(len(self.log), 0)
        self.assert_stat_buffers_empty()

    def test_multiple(self):
        eve_type = self.ch.type_(type_id=1, attributes={})
        holder1 = self.make_item_mock(ModuleHigh, eve_type, state=State.active)
        holder2 = self.make_item_mock(ModuleHigh, eve_type, state=State.active)
        self.add_holder(holder1)
        self.add_holder(holder2)
        holder1_dps = Mock(em=1.2, thermal=2.3, kinetic=3.4, explosive=4.5, total=5.6)
        holder2_dps = Mock(em=0, thermal=4, kinetic=2, explosive=7.1, total=99)
        holder1.get_nominal_dps.return_value = holder1_dps
        holder2.get_nominal_dps.return_value = holder2_dps
        stats_dps = self.ss.get_nominal_dps()
        self.assertAlmostEqual(stats_dps.em, 1.2)
        self.assertAlmostEqual(stats_dps.thermal, 6.3)
        self.assertAlmostEqual(stats_dps.kinetic, 5.4)
        self.assertAlmostEqual(stats_dps.explosive, 11.6)
        self.assertAlmostEqual(stats_dps.total, 24.5)
        self.remove_holder(holder1)
        self.remove_holder(holder2)
        self.assertEqual(len(self.log), 0)
        self.assert_stat_buffers_empty()

    def test_not_damage_dealer(self):
        eve_type = self.ch.type_(type_id=1, attributes={})
        holder = self.make_item_mock(Implant, eve_type, state=State.active, strict_spec=False)
        holder_dps = Mock(em=1.2, thermal=2.3, kinetic=3.4, explosive=4.5, total=5.6)
        holder.get_nominal_dps = Mock()
        holder.get_nominal_dps.return_value = holder_dps
        self.add_holder(holder)
        stats_dps = self.ss.get_nominal_dps()
        self.assertIsNone(stats_dps.em)
        self.assertIsNone(stats_dps.thermal)
        self.assertIsNone(stats_dps.kinetic)
        self.assertIsNone(stats_dps.explosive)
        self.assertIsNone(stats_dps.total)
        self.remove_holder(holder)
        self.assertEqual(len(self.log), 0)
        self.assert_stat_buffers_empty()

    def test_arguments_custom(self):
        eve_type = self.ch.type_(type_id=1, attributes={})
        holder = self.make_item_mock(ModuleHigh, eve_type, state=State.active)
        self.add_holder(holder)
        holder_dps = Mock(em=1.2, thermal=2.3, kinetic=3.4, explosive=4.5, total=5.6)
        holder.get_nominal_dps.return_value = holder_dps
        arg_resistances = Mock()
        arg_reload = Mock()
        calls_before = len(holder.get_nominal_dps.mock_calls)
        self.ss.get_nominal_dps(target_resistances=arg_resistances, reload=arg_reload)
        calls_after = len(holder.get_nominal_dps.mock_calls)
        self.assertEqual(calls_after - calls_before, 1)
        self.assertEqual(holder.get_nominal_dps.mock_calls[-1],
                         call(target_resistances=arg_resistances, reload=arg_reload))
        self.remove_holder(holder)
        self.assertEqual(len(self.log), 0)
        self.assert_stat_buffers_empty()

    def test_arguments_default(self):
        eve_type = self.ch.type_(type_id=1, attributes={})
        holder = self.make_item_mock(ModuleHigh, eve_type, state=State.active)
        self.add_holder(holder)
        holder_dps = Mock(em=1.2, thermal=2.3, kinetic=3.4, explosive=4.5, total=5.6)
        holder.get_nominal_dps.return_value = holder_dps
        calls_before = len(holder.get_nominal_dps.mock_calls)
        self.ss.get_nominal_dps()
        calls_after = len(holder.get_nominal_dps.mock_calls)
        self.assertEqual(calls_after - calls_before, 1)
        self.assertEqual(holder.get_nominal_dps.mock_calls[-1], call(target_resistances=None, reload=False))
        self.remove_holder(holder)
        self.assertEqual(len(self.log), 0)
        self.assert_stat_buffers_empty()

    def test_single_none_em(self):
        eve_type = self.ch.type_(type_id=1, attributes={})
        holder = self.make_item_mock(ModuleHigh, eve_type, state=State.active)
        self.add_holder(holder)
        holder_dps = Mock(em=None, thermal=2.3, kinetic=3.4, explosive=4.5, total=5.6)
        holder.get_nominal_dps.return_value = holder_dps
        stats_dps = self.ss.get_nominal_dps()
        self.assertIsNone(stats_dps.em)
        self.assertAlmostEqual(stats_dps.thermal, 2.3)
        self.assertAlmostEqual(stats_dps.kinetic, 3.4)
        self.assertAlmostEqual(stats_dps.explosive, 4.5)
        self.assertAlmostEqual(stats_dps.total, 10.2)
        self.remove_holder(holder)
        self.assertEqual(len(self.log), 0)
        self.assert_stat_buffers_empty()

    def test_single_none_therm(self):
        eve_type = self.ch.type_(type_id=1, attributes={})
        holder = self.make_item_mock(ModuleHigh, eve_type, state=State.active)
        self.add_holder(holder)
        holder_dps = Mock(em=1.2, thermal=None, kinetic=3.4, explosive=4.5, total=5.6)
        holder.get_nominal_dps.return_value = holder_dps
        stats_dps = self.ss.get_nominal_dps()
        self.assertAlmostEqual(stats_dps.em, 1.2)
        self.assertIsNone(stats_dps.thermal)
        self.assertAlmostEqual(stats_dps.kinetic, 3.4)
        self.assertAlmostEqual(stats_dps.explosive, 4.5)
        self.assertAlmostEqual(stats_dps.total, 9.1)
        self.remove_holder(holder)
        self.assertEqual(len(self.log), 0)
        self.assert_stat_buffers_empty()

    def test_single_none_kin(self):
        eve_type = self.ch.type_(type_id=1, attributes={})
        holder = self.make_item_mock(ModuleHigh, eve_type, state=State.active)
        self.add_holder(holder)
        holder_dps = Mock(em=1.2, thermal=2.3, kinetic=None, explosive=4.5, total=5.6)
        holder.get_nominal_dps.return_value = holder_dps
        stats_dps = self.ss.get_nominal_dps()
        self.assertAlmostEqual(stats_dps.em, 1.2)
        self.assertAlmostEqual(stats_dps.thermal, 2.3)
        self.assertIsNone(stats_dps.kinetic)
        self.assertAlmostEqual(stats_dps.explosive, 4.5)
        self.assertAlmostEqual(stats_dps.total, 8)
        self.remove_holder(holder)
        self.assertEqual(len(self.log), 0)
        self.assert_stat_buffers_empty()

    def test_single_none_expl(self):
        eve_type = self.ch.type_(type_id=1, attributes={})
        holder = self.make_item_mock(ModuleHigh, eve_type, state=State.active)
        self.add_holder(holder)
        holder_dps = Mock(em=1.2, thermal=2.3, kinetic=3.4, explosive=None, total=5.6)
        holder.get_nominal_dps.return_value = holder_dps
        stats_dps = self.ss.get_nominal_dps()
        self.assertAlmostEqual(stats_dps.em, 1.2)
        self.assertAlmostEqual(stats_dps.thermal, 2.3)
        self.assertAlmostEqual(stats_dps.kinetic, 3.4)
        self.assertIsNone(stats_dps.explosive)
        self.assertAlmostEqual(stats_dps.total, 6.9)
        self.remove_holder(holder)
        self.assertEqual(len(self.log), 0)
        self.assert_stat_buffers_empty()

    def test_single_none_all(self):
        eve_type = self.ch.type_(type_id=1, attributes={})
        holder = self.make_item_mock(ModuleHigh, eve_type, state=State.active)
        self.add_holder(holder)
        holder_dps = Mock(em=None, thermal=None, kinetic=None, explosive=None, total=None)
        holder.get_nominal_dps.return_value = holder_dps
        stats_dps = self.ss.get_nominal_dps()
        self.assertIsNone(stats_dps.em)
        self.assertIsNone(stats_dps.thermal)
        self.assertIsNone(stats_dps.kinetic)
        self.assertIsNone(stats_dps.explosive)
        self.assertIsNone(stats_dps.total)
        self.remove_holder(holder)
        self.assertEqual(len(self.log), 0)
        self.assert_stat_buffers_empty()

    def test_single_zero_em(self):
        eve_type = self.ch.type_(type_id=1, attributes={})
        holder = self.make_item_mock(ModuleHigh, eve_type, state=State.active)
        self.add_holder(holder)
        holder_dps = Mock(em=0, thermal=None, kinetic=None, explosive=None, total=None)
        holder.get_nominal_dps.return_value = holder_dps
        stats_dps = self.ss.get_nominal_dps()
        self.assertAlmostEqual(stats_dps.em, 0)
        self.assertIsNone(stats_dps.thermal)
        self.assertIsNone(stats_dps.kinetic)
        self.assertIsNone(stats_dps.explosive)
        self.assertAlmostEqual(stats_dps.total, 0)
        self.remove_holder(holder)
        self.assertEqual(len(self.log), 0)
        self.assert_stat_buffers_empty()

    def test_single_zero_therm(self):
        eve_type = self.ch.type_(type_id=1, attributes={})
        holder = self.make_item_mock(ModuleHigh, eve_type, state=State.active)
        self.add_holder(holder)
        holder_dps = Mock(em=None, thermal=0, kinetic=None, explosive=None, total=None)
        holder.get_nominal_dps.return_value = holder_dps
        stats_dps = self.ss.get_nominal_dps()
        self.assertIsNone(stats_dps.em)
        self.assertAlmostEqual(stats_dps.thermal, 0)
        self.assertIsNone(stats_dps.kinetic)
        self.assertIsNone(stats_dps.explosive)
        self.assertAlmostEqual(stats_dps.total, 0)
        self.remove_holder(holder)
        self.assertEqual(len(self.log), 0)
        self.assert_stat_buffers_empty()

    def test_single_zero_kin(self):
        eve_type = self.ch.type_(type_id=1, attributes={})
        holder = self.make_item_mock(ModuleHigh, eve_type, state=State.active)
        self.add_holder(holder)
        holder_dps = Mock(em=None, thermal=None, kinetic=0, explosive=None, total=None)
        holder.get_nominal_dps.return_value = holder_dps
        stats_dps = self.ss.get_nominal_dps()
        self.assertIsNone(stats_dps.em)
        self.assertIsNone(stats_dps.thermal)
        self.assertAlmostEqual(stats_dps.kinetic, 0)
        self.assertIsNone(stats_dps.explosive)
        self.assertAlmostEqual(stats_dps.total, 0)
        self.remove_holder(holder)
        self.assertEqual(len(self.log), 0)
        self.assert_stat_buffers_empty()

    def test_single_zero_expl(self):
        eve_type = self.ch.type_(type_id=1, attributes={})
        holder = self.make_item_mock(ModuleHigh, eve_type, state=State.active)
        self.add_holder(holder)
        holder_dps = Mock(em=None, thermal=None, kinetic=None, explosive=0, total=None)
        holder.get_nominal_dps.return_value = holder_dps
        stats_dps = self.ss.get_nominal_dps()
        self.assertIsNone(stats_dps.em)
        self.assertIsNone(stats_dps.thermal)
        self.assertIsNone(stats_dps.kinetic)
        self.assertAlmostEqual(stats_dps.explosive, 0)
        self.assertAlmostEqual(stats_dps.total, 0)
        self.remove_holder(holder)
        self.assertEqual(len(self.log), 0)
        self.assert_stat_buffers_empty()

    def test_none_and_data(self):
        # As container for damage dealers is not ordered,
        # this test may be unreliable (even if there's issue,
        # it won't fail each run)
        eve_type = self.ch.type_(type_id=1, attributes={})
        holder1 = self.make_item_mock(ModuleHigh, eve_type, state=State.active)
        holder2 = self.make_item_mock(ModuleHigh, eve_type, state=State.active)
        self.add_holder(holder1)
        self.add_holder(holder2)
        holder1_dps = Mock(em=1.2, thermal=2.3, kinetic=3.4, explosive=4.5, total=5.6)
        holder2_dps = Mock(em=None, thermal=None, kinetic=None, explosive=None, total=None)
        holder1.get_nominal_dps.return_value = holder1_dps
        holder2.get_nominal_dps.return_value = holder2_dps
        stats_dps = self.ss.get_nominal_dps()
        self.assertAlmostEqual(stats_dps.em, 1.2)
        self.assertAlmostEqual(stats_dps.thermal, 2.3)
        self.assertAlmostEqual(stats_dps.kinetic, 3.4)
        self.assertAlmostEqual(stats_dps.explosive, 4.5)
        self.assertAlmostEqual(stats_dps.total, 11.4)
        self.remove_holder(holder1)
        self.remove_holder(holder2)
        self.assertEqual(len(self.log), 0)
        self.assert_stat_buffers_empty()

    def test_filter_success(self):
        eve_type = self.ch.type_(type_id=1, attributes={})
        holder = self.make_item_mock(ModuleHigh, eve_type, state=State.active)
        self.add_holder(holder)
        holder_dps = Mock(em=1.2, thermal=2.3, kinetic=3.4, explosive=4.5, total=5.6)
        holder.get_nominal_dps.return_value = holder_dps
        stats_dps = self.ss.get_nominal_dps(holder_filter=lambda h: True)
        self.assertAlmostEqual(stats_dps.em, 1.2)
        self.assertAlmostEqual(stats_dps.thermal, 2.3)
        self.assertAlmostEqual(stats_dps.kinetic, 3.4)
        self.assertAlmostEqual(stats_dps.explosive, 4.5)
        self.assertAlmostEqual(stats_dps.total, 11.4)
        self.remove_holder(holder)
        self.assertEqual(len(self.log), 0)
        self.assert_stat_buffers_empty()

    def test_filter_fail(self):
        eve_type = self.ch.type_(type_id=1, attributes={})
        holder = self.make_item_mock(ModuleHigh, eve_type, state=State.active)
        self.add_holder(holder)
        holder_dps = Mock(em=1.2, thermal=2.3, kinetic=3.4, explosive=4.5, total=5.6)
        holder.get_nominal_dps.return_value = holder_dps
        stats_dps = self.ss.get_nominal_dps(holder_filter=lambda h: False)
        self.assertIsNone(stats_dps.em)
        self.assertIsNone(stats_dps.thermal)
        self.assertIsNone(stats_dps.kinetic)
        self.assertIsNone(stats_dps.explosive)
        self.assertIsNone(stats_dps.total)
        self.remove_holder(holder)
        self.assertEqual(len(self.log), 0)
        self.assert_stat_buffers_empty()

    def test_filter_mixed(self):
        eve_type = self.ch.type_(type_id=1, attributes={})
        holder1 = self.make_item_mock(ModuleHigh, eve_type, state=State.active)
        holder2 = self.make_item_mock(ModuleHigh, eve_type, state=State.active)
        self.add_holder(holder1)
        self.add_holder(holder2)
        holder1_dps = Mock(em=1.2, thermal=2.3, kinetic=3.4, explosive=4.5, total=5.6)
        holder2_dps = Mock(em=0, thermal=4, kinetic=2, explosive=7.1, total=99)
        holder1.get_nominal_dps.return_value = holder1_dps
        holder2.get_nominal_dps.return_value = holder2_dps
        stats_dps = self.ss.get_nominal_dps(holder_filter=lambda h: h is holder2)
        self.assertAlmostEqual(stats_dps.em, 0)
        self.assertAlmostEqual(stats_dps.thermal, 4)
        self.assertAlmostEqual(stats_dps.kinetic, 2)
        self.assertAlmostEqual(stats_dps.explosive, 7.1)
        self.assertAlmostEqual(stats_dps.total, 13.1)
        self.remove_holder(holder1)
        self.remove_holder(holder2)
        self.assertEqual(len(self.log), 0)
        self.assert_stat_buffers_empty()
