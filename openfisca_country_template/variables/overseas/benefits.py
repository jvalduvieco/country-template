# -*- coding: utf-8 -*-

# This file defines the variables of our legislation.
# A variable is property of a person, or an entity (e.g. a household).
# See http://openfisca.org/doc/variables.html

# Import from openfisca-core the common python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the entities specifically defined for this tax and benefit system
from openfisca_country_template.entities import *


class abroad_benefits(Variable):
    value_type = float
    entity = Person
    definition_period = MONTH
    label = "Basic income provided to adults"
    reference = "https://law.gov.example/basic_income"  # Always use the most official source

    # Since Dec 1st 2016, the basic income is provided to any adult, without considering their income.
    def formula_2016_12(person, period, parameters):
        age_condition = person('age', period) >= parameters(period).general.age_of_majority
        return age_condition * parameters(period).benefits.basic_income  # This '*' is a vectorial 'if'. See http://openfisca.org/doc/coding-the-legislation/30_case_disjunction.html#simple-multiplication

    # From Dec 1st 2015 to Nov 30 2016, the basic income is provided to adults who have no income.
    # Before Dec 1st 2015, the basic income does not exist in the law, and calculating it returns its default value, which is 0.
    def formula_2015_12(person, period, parameters):
        age_condition = person('age', period) >= parameters(period).general.age_of_majority
        salary_condition = person('salary', period) == 0
        return age_condition * salary_condition * parameters(period).benefits.basic_income  # The '*' is also used as a vectorial 'and'. See http://openfisca.org/doc/coding-the-legislation/25_vectorial_computing.html#forbidden-operations-and-alternatives
