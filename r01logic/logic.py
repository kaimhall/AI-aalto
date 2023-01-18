#!/usr/bin/python3
import numpy as np
from itertools import *
import re

'''
Representation of propositional formulas in Python.

The basic connectives are NOT, AND and OR.
IMPL and EQVI are reduced to these through the obvious equivalences.
Separate classes represent each connective, atomic formulas, and
the constants TRUE and FALSE.

The methods supported are:
  f.vars(self)
    Set of all variables occurring in the formula f
  f.truthValue(self,v)  
    Compute truth-value of f under valuation 'v'
    Returns True if v |= f and False otherwise

Valuations are represented as sets/lists consisting of the Names of those atomic formulas that are True. For example, the empty set/list corresponds to the valuation in which all atomic formulas are False.
 
To test if the formula ATOM("a") is true in a valuation
V, one tests if "a" is an element of the set/list V.
'''

# Superclass to handle parts of AND and OR
class BinaryFormula:
  def __init__(self, subformula1, subformula2):
    self.subformula1 = subformula1
    self.subformula2 = subformula2

  # Both AND and OR will inherit __init__ and vars from BinaryFormula
  def vars(self):
    return self.subformula1.vars().union(self.subformula2.vars())

# AND - conjunction
class AND(BinaryFormula):
  def __repr__(self):
    return "(" + str(self.subformula1) + " AND " + str(self.subformula2) + ")"
  
  def truthValue(self, v):
    if not v and len(v) <2: return False
    elif type(v[0]) == str: return sorted(list(self.vars())) == v
    else: return list(self.vars()) in v
   
# OR - disjunction
class OR(BinaryFormula):
  def __repr__(self):
    return "(" + str(self.subformula1) + " OR " + str(self.subformula2) + ")"

  def truthValue(self, v):
    if v == []: return False
    else: return True

# NOT - negation
class NOT:
  def __init__(self, subformula):
    self.subformula = subformula

  def __repr__(self):
    return "(NOT " + str(self.subformula) + ")"

  def vars(self):
    return self.subformula.vars()

  def truthValue(self, v):
    print(v)
    if v == []: return True
    else: return False
 
# ATOM - atomic formulas
class ATOM:
  def __init__(self, name):
    self.name = name

  def __repr__(self):
    return self.name
  
  def vars(self):
    return {self.name}

  def truthValue(self, v):
    return self.name in [item for items in v for item in items]

# FALSE - the constant that represents the truth-value False
class FALSE:
  def __repr__(self, v):
    return "FALSE"

  def vars(self):
    return set()

  def truthValue(self,v):
    return False
   
# TRUE - the constant that represents the truth-value True
class TRUE:
  def __repr__(self):
    return "TRUE"

  def vars(self):
    return set()

  def truthValue(self,v):
    return True

    
# Implication and equivalence reduced to the primitive connectives
# A -> B is reduced to -A V B
def IMPL(f1,f2):
  return OR(NOT(f1),f2)

# A <-> B is reduced to (A -> B) & (B -> A)
def EQVI(f1,f2):
  return AND(IMPL(f1,f2),IMPL(f2,f1))

'''
Test for the satisfiability of a formula
This function should return False if the formula is unsatisfiable,

and otherwise it will return a valuation that satisfies the formula.
The valuation is a list of names of true atomic formulas.

A very simple implementation would first find the set of all
variables occurring in a formula, and then generate all possible
subsets of that set (or corresponding lists), which represent
all possible valuations, and then test if the given formula is
true in at least one of the valuations.

'satisfiable' returns False if the formula is NOT satisfiable,
and it returns the valuation that makes the formula true otherwise.
'''

def powerSet(atoms):
  if len(atoms) == 0:
    return [[]] # base case is empty list
  
  else:
    base = powerSet(atoms[:-1]) #  send smaller list as recursive call
    operator = atoms[-1:]
    return base + [(b + operator) for b in base] # communicate frame to future frames

def satisfiable(f:BinaryFormula):
  names = [*f.vars(),] # unpack vars to list
  v = powerSet(names)  #generate subsets
  print(f.subformula1.vars())
  print(f.subformula2.vars())
  print(f.vars())
  return f.truthValue(v)
  
'''
  Test logical consequence
  Returns True if f2 is a logical consequence of f1 (that is f1 |= f2). False otherwise
  for logical consequence f1 |= f2 check that for _every_ valuation, that f1 is False and f2 is True
'''

def consequence_helper(f1, f2):
  A = powerSet(list(f1.vars()))
  B = powerSet(list(f2.vars()))
  r =[v for v in B if v in A][1:]
  return r

def logicalConsequence(f1,f2):
  return len(consequence_helper(f1, f2)) > 0

if __name__ == "__main__":
  A = ATOM('A')
  B = ATOM('B')
  C = ATOM('C')
  f = AND(A,B)

  print(satisfiable(AND(A, NOT(A))))

  






