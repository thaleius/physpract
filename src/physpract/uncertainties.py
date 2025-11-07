from decimal import Decimal
import math as m
from .helpers import roundToSignificantFigures, to_non_scientific_string

class Value:
  pass

def check(a: Value, b):
  if not isinstance(b, Value):
    b = Value(b)
  return a, b

class Value:
  def __init__(self, value, uncertainty=0):
    # if type(value) == str or type(uncertainty) == str:
    #   value = Decimal(value)
    #   uncertainty = Decimal(uncertainty)
    
    self.value = Decimal(value)
    self.uncertainty = abs(Decimal(uncertainty))
    self.unit = None
    self.history = self

  def set_unit(self, unit: str):
    self.unit = unit
    return self
  
  def __add__(self, other):
    a, b = check(self, other)
    v = Value(a.value + b.value, a.uncertainty + b.uncertainty)
    v.history = (a.history, b.history, 'add')
    return v
  
  def __radd__(self, other):
    return self.__add__(other)
  
  def __sub__(self, other):
    a, b = check(self, other)
    v = Value(a.value - b.value, a.uncertainty + b.uncertainty)
    v.history = (a.history, b.history, 'sub')
    return v
    
  def __rsub__(self, other):
    a, b = check(self, other)
    v = Value(b.value - a.value, a.uncertainty + b.uncertainty)
    v.history = (b.history, a.history, 'rsub')
    return v

  def __mul__(self, other):
    a, b = check(self, other)
    v = Value(a.value * b.value, a.value * b.uncertainty + b.value * a.uncertainty)
    v.history = (a.history, b.history, 'mul')
    return v
    
  def __rmul__(self, other):
    a, b = check(self, other)
    v = Value(a.value * b.value, a.value * b.uncertainty + b.value * a.uncertainty)
    v.history = (b.history, a.history, 'rmul')
    return v
  
  def __truediv__(self, other):
    a, b = check(self, other)
    v = Value(a.value / b.value, (b.value * a.uncertainty - a.value * b.uncertainty) / (b.value ** 2))
    v.history = (a.history, b.history, 'div')
    return v
  
  def __rtruediv__(self, other):
    a, b = check(self, other)
    v = Value(b.value / a.value, (a.value * b.uncertainty - b.value * a.uncertainty) / (a.value ** 2))
    v.history = (b.history, a.history, 'rdiv')
    return v
  
  def __neg__(self):
    v = Value(-self.value, self.uncertainty)
    v.history = (self.history, 'neg')
    return v
  
  def __pow__(self, power):
    a, b = check(self, power)
    v = Value(self.value ** b.value, a.value**b.value * (b.value/a.value*a.uncertainty + (Decimal(m.log(a.value))*b.uncertainty if b.uncertainty != 0 else 0)))
    v.history = (a.history, b.history, 'pow')
    return v
  
  def __repr__(self):
    return f"Value({self.value}, {self.uncertainty}, unit={self.unit})"

  def __str__(self):
    rounded_value, rounded_uncertainty = roundToSignificantFigures(self.value, self.uncertainty)
    tuple = rounded_value.as_tuple()
    if abs(tuple.exponent) >= 3:
      # uncertainty = ''.join(map(str, rounded_uncertainty.as_tuple().digits))
      correct = tuple.exponent+len(tuple.digits)-1
      value = rounded_value.scaleb(-correct)
      uncertainty = rounded_uncertainty.scaleb(-correct)
      if uncertainty == 0:
        s = f"{value} ⋅ 10^{{{correct}}}"
      else:
        s = f"({value}±{uncertainty}) ⋅ 10^{{{correct}}}"
    else:
      s = f"{to_non_scientific_string(rounded_value)}" + f"±{to_non_scientific_string(rounded_uncertainty)}" if rounded_uncertainty != 0 else ""
    if self.unit:
      s = f"({s}) {self.unit}"
    return s

  def short(self, unit: bool = True) -> str:
    rounded_value, rounded_uncertainty = roundToSignificantFigures(self.value, self.uncertainty)
    tuple = rounded_value.as_tuple()
    value = to_non_scientific_string(rounded_value)
    s = ""
    correct = tuple.exponent+len(tuple.digits)-1
    if abs(tuple.exponent) >= 3 and correct > 1:
      if rounded_uncertainty == 0:
        s = f"{rounded_value.scaleb(-correct)}e{correct}"
      else:
        s = f"{rounded_value.scaleb(-correct)}({''.join(map(str, rounded_uncertainty.as_tuple().digits))})e{correct}"
    else:
      if rounded_uncertainty == 0:
        s = f"{value}"
      else:
        s = f"{value}({''.join(map(str, rounded_uncertainty.as_tuple().digits))})"
    if self.unit and unit:
      s = f"({s}) {self.unit}"
    return s