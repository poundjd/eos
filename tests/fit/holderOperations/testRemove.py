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


from unittest.mock import Mock, call, patch

from eos.const.eos import State
from eos.fit import Fit
from eos.fit.exception import HolderRemoveError
from eos.tests.fit.fitTestCase import FitTestCase


@patch('eos.fit.fit.RestrictionTracker')
@patch('eos.fit.fit.LinkTracker')
class TestFitRemoveHolder(FitTestCase):

    def testNotAssigned(self, *args):
        fit = Fit()
        holder = Mock(_fit=None, state=State.active, spec_set=('_fit', 'state'))
        ltCallsBefore = len(fit._linkTracker.mock_calls)
        rtCallsBefore = len(fit._restrictionTracker.mock_calls)
        self.assertRaises(HolderRemoveError, fit._removeHolder, holder)
        ltCallsAfter = len(fit._linkTracker.mock_calls)
        rtCallsAfter = len(fit._restrictionTracker.mock_calls)
        self.assertEqual(ltCallsAfter - ltCallsBefore, 0)
        self.assertEqual(rtCallsAfter - rtCallsBefore, 0)
        self.assertFitBuffersEmpty(fit)

    def testOtherFit(self, *args):
        fit1 = Fit()
        fit2 = Fit()
        holder = Mock(_fit=None, state=State.active, spec_set=('_fit', 'state'))
        fit1._addHolder(holder)
        ltCallsBefore = len(fit1._linkTracker.mock_calls)
        rtCallsBefore = len(fit1._restrictionTracker.mock_calls)
        self.assertRaises(HolderRemoveError, fit2._removeHolder, holder)
        ltCallsAfter = len(fit1._linkTracker.mock_calls)
        rtCallsAfter = len(fit1._restrictionTracker.mock_calls)
        self.assertEqual(ltCallsAfter - ltCallsBefore, 0)
        self.assertEqual(rtCallsAfter - rtCallsBefore, 0)
        fit1._removeHolder(holder)
        self.assertFitBuffersEmpty(fit1)
        self.assertFitBuffersEmpty(fit2)

    def testEosLess(self, *args):
        fit = Fit()
        holder = Mock(_fit=None, state=State.active, spec_set=('_fit', 'state'))
        fit._addHolder(holder)
        ltCallsBefore = len(fit._linkTracker.mock_calls)
        rtCallsBefore = len(fit._restrictionTracker.mock_calls)
        fit._removeHolder(holder)
        ltCallsAfter = len(fit._linkTracker.mock_calls)
        rtCallsAfter = len(fit._restrictionTracker.mock_calls)
        self.assertEqual(ltCallsAfter - ltCallsBefore, 0)
        self.assertEqual(rtCallsAfter - rtCallsBefore, 0)
        self.assertFitBuffersEmpty(fit)

    def testEosLessCharge(self, *args):
        fit = Fit()
        holder = Mock(_fit=None, charge=None, state=State.active, spec_set=('_fit', 'charge', 'state'))
        charge = Mock(_fit=None, state=State.offline, spec_set=('_fit', 'state'))
        holder.charge = charge
        fit._addHolder(holder)
        ltCallsBefore = len(fit._linkTracker.mock_calls)
        rtCallsBefore = len(fit._restrictionTracker.mock_calls)
        fit._removeHolder(holder)
        ltCallsAfter = len(fit._linkTracker.mock_calls)
        rtCallsAfter = len(fit._restrictionTracker.mock_calls)
        self.assertEqual(ltCallsAfter - ltCallsBefore, 0)
        self.assertEqual(rtCallsAfter - rtCallsBefore, 0)
        self.assertFitBuffersEmpty(fit)

    def testWithEos(self, *args):
        eos = Mock(spec_set=())
        fit = Fit(eos)
        holder = Mock(_fit=None, state=State.active, spec_set=('_fit', 'state'))
        fit._addHolder(holder)
        ltCallsBefore = len(fit._linkTracker.mock_calls)
        rtCallsBefore = len(fit._restrictionTracker.mock_calls)
        fit._removeHolder(holder)
        ltCallsAfter = len(fit._linkTracker.mock_calls)
        rtCallsAfter = len(fit._restrictionTracker.mock_calls)
        self.assertEqual(ltCallsAfter - ltCallsBefore, 2)
        self.assertEqual(fit._linkTracker.mock_calls[-2], call.disableStates(holder, {State.offline, State.online, State.active}))
        self.assertEqual(fit._linkTracker.mock_calls[-1], call.removeHolder(holder))
        self.assertEqual(rtCallsAfter - rtCallsBefore, 1)
        self.assertEqual(fit._restrictionTracker.mock_calls[-1], call.disableStates(holder, {State.offline, State.online, State.active}))
        self.assertFitBuffersEmpty(fit)

    def testWithEosCharge(self, *args):
        eos = Mock(spec_set=())
        fit = Fit(eos)
        holder = Mock(_fit=None, charge=None, state=State.active, spec_set=('_fit', 'charge', 'state'))
        charge = Mock(_fit=None, state=State.offline, spec_set=('_fit', 'state'))
        holder.charge = charge
        fit._addHolder(holder)
        ltCallsBefore = len(fit._linkTracker.mock_calls)
        rtCallsBefore = len(fit._restrictionTracker.mock_calls)
        fit._removeHolder(holder)
        ltCallsAfter = len(fit._linkTracker.mock_calls)
        rtCallsAfter = len(fit._restrictionTracker.mock_calls)
        self.assertEqual(ltCallsAfter - ltCallsBefore, 4)
        self.assertEqual(fit._linkTracker.mock_calls[-4], call.disableStates(charge, {State.offline}))
        self.assertEqual(fit._linkTracker.mock_calls[-3], call.removeHolder(charge))
        self.assertEqual(fit._linkTracker.mock_calls[-2], call.disableStates(holder, {State.offline, State.online, State.active}))
        self.assertEqual(fit._linkTracker.mock_calls[-1], call.removeHolder(holder))
        self.assertEqual(rtCallsAfter - rtCallsBefore, 2)
        self.assertEqual(fit._restrictionTracker.mock_calls[-2], call.disableStates(charge, {State.offline}))
        self.assertEqual(fit._restrictionTracker.mock_calls[-1], call.disableStates(holder, {State.offline, State.online, State.active}))
        self.assertFitBuffersEmpty(fit)
