#===============================================================================
# Copyright (C) 2011 Anton Vorobyov
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

import math

# Attributes
attrSkillRq1 = 182
attrSkillRq2 = 183
attrSkillRq3 = 184
attrSkillRq1Lvl = 277
attrSkillRq2Lvl = 278
attrSkillRq3Lvl = 279
attrSkillRq4 = 1285
attrSkillRq4Lvl = 1286
attrSkillRq5Lvl = 1287
attrSkillRq6Lvl = 1288
attrSkillRq5 = 1289
attrSkillRq6 = 1290
# Dictionary which holds skill requirement attribute IDs
# and their corresponding level attribute IDs
attrSkillRqMap = {attrSkillRq1: attrSkillRq1Lvl,
                  attrSkillRq2: attrSkillRq2Lvl,
                  attrSkillRq3: attrSkillRq3Lvl,
                  attrSkillRq4: attrSkillRq4Lvl,
                  attrSkillRq5: attrSkillRq5Lvl,
                  attrSkillRq6: attrSkillRq6Lvl}

# Item categories
catShip = 6
catCharge = 8
catSkill = 16
catImplant = 20
catSubsystem = 32

# Item categories immune to stacking penalty
penaltyImmuneCats = (catShip, catCharge, catSkill,
                     catImplant, catSubsystem)
# Stacking penalty base constant
penaltyBase = 1 / math.exp((1 / 2.67) ** 2)

# Dogma operands section
opndAddItmMod = 6  # Applies modification directly to some item, format: ((location->targetAttribute).(operator)).AIM(sourceAttribute)
opndAddLocGrpMod = 7  # Applies modification to items belonging to some location, filtered by group, format: ((location..groupFilter->targetAttribute).(operator)).ALGM(sourceAttribute)
opndAddLocMod = 8  # Applies modification to all items belonging to some location, format: ((location->targetAttribute).(operator)).ALM(sourceAttribute)
opndAddLocSkrqMod = 9  # Applies modification to items belonging to some location, filtered by skill requirement, format: ((location[skillRequirement]->targetAttribute).(operator)).ALRSM(sourceAttribute)
opndAddOwnSkrqMod = 11  # Applies modification to items belonging to some location, filtered by owner of source, format: ((location[skillRequirement]->targetAttribute).(operator)).AORSM(sourceAttribute)
opndItmAttr = 12  # Joins target items and attribute into target definition, format: location->targetAttribute
opndCombine = 17  # Executes two statements, format: expression1; expression2
opndDefOptr = 21  # Define operator, text in expressionValue field
opndDefAttr = 22  # Define attribute, integer in expressionAttributeID field
opndDefLoc = 24  # Define location, text in expressionValue field
opndDefGrp = 26  # Define group, integer in expressionGroupID field
opndDefInt = 27  # Defines an integer constant, integer in expressionValue field
opndDefType = 29  # Define a type, integer in expressionTypeID field
opndTgtOptr = 31  # Joins target (attribute of possibly filtered items) and operator definitions, format: (location->targetAttribute).(operator)
opndLocGrp = 48  # Joins location and group definitions into single filter, format: location..group
opndLocSkrq = 49  # Joins location and skillRequirement definitions into single filter, format: location[skillRequirement]


### Custom Eos stuff, doesn't depend on database IDs ###

# Dogma operators section, here we deliberately assign IDs,
# but make sure IDs are assigned to keep operations in
# proper order
optrPreAssignment = 1
optrPreMul = 2
optrPreDiv = 3
optrModAdd = 4
optrModSub = 5
optrPostMul = 6
optrPostDiv = 7
optrPostPercent = 8
optrPostAssignment = 9

# Database name: ID map for Dogma operators
optrConvMap = {"PreAssignment": optrPreAssignment,
               "PreMul": optrPreMul,
               "PreDiv": optrPreDiv,
               "ModAdd": optrModAdd,
               "ModSub": optrModSub,
               "PostMul": optrPostMul,
               "PostDiv": optrPostDiv,
               "PostPercent": optrPostPercent,
               "PostAssignment": optrPostAssignment}

# Target location IDs
locSelf = 0
locChar = 1
locShip = 2
locTgt = 4
locCont = 5
locArea = 6
# Database name: ID map for target locations
locConvMap = {"Self": locSelf,
              "Char": locChar,
              "Ship": locShip,
              "Target": locTgt,
              "Other": locCont,
              "Area": locArea}

# Filter IDs section
filLocGrp = 0  # Filter by location and group
filLoc = 1  # Filter by location
filLocSkrq = 2  # Filter by location and skill requirement
filterOwnSkrq = 3  # Filter by owner and skill requirement
