# ==============================================================================
# Copyright (C) 2011 Diego Duclos
# Copyright (C) 2011-2018 Anton Vorobyov
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


import logging

from eos import Rig
from eos.const.eos import ModAffecteeFilter
from eos.const.eos import ModDomain
from eos.const.eos import ModOperator
from eos.const.eve import EffectCategoryId
from tests.integration.calculator.testcase import CalculatorTestCase


class TestAffectorAttr(CalculatorTestCase):

    def test_absent_attr_combination(self):
        # Check how calculator reacts to affector attribute which is absent
        tgt_attr = self.mkattr()
        abs_attr = self.mkattr()
        src_attr = self.mkattr()
        invalid_modifier = self.mkmod(
            affectee_filter=ModAffecteeFilter.item,
            affectee_domain=ModDomain.self,
            affectee_attr_id=tgt_attr.id,
            operator=ModOperator.post_percent,
            affector_attr_id=abs_attr.id)
        valid_modifier = self.mkmod(
            affectee_filter=ModAffecteeFilter.item,
            affectee_domain=ModDomain.self,
            affectee_attr_id=tgt_attr.id,
            operator=ModOperator.post_mul,
            affector_attr_id=src_attr.id)
        effect = self.mkeffect(
            category_id=EffectCategoryId.passive,
            modifiers=(invalid_modifier, valid_modifier))
        item_type = self.mktype(
            attrs={src_attr.id: 1.5, tgt_attr.id: 100}, effects=[effect])
        item = Rig(item_type.id)
        # Action
        self.fit.rigs.add(item)
        # Verification
        # Invalid source value shouldn't screw whole calculation process
        self.assertAlmostEqual(item.attrs[tgt_attr.id], 150)
        self.assert_log_entries(1)
        log_record = self.log[0]
        self.assertEqual(log_record.name, 'eos.calculator.map')
        self.assertEqual(log_record.levelno, logging.INFO)
        self.assertEqual(
            log_record.msg,
            'unable to find base value for attribute {} '
            'on item type {}'.format(abs_attr.id, item_type.id))
        # Cleanup
        self.assert_solsys_buffers_empty(self.fit.solar_system)
