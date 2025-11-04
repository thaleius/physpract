from decimal import Decimal
from math import log
from .helpers import roundToSignificantFigures, to_non_scientific_string

class Value:
  pass

class Sum:
  pass
  
class Mul:
  pass
  
class Div:
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

  def set_unit(self, unit: str):
    self.unit = unit
    return self
  
  def __add__(self, other):
    a, b = check(self, other)
    return Value(a.value + b.value, a.uncertainty + b.uncertainty)
  
  def __radd__(self, other):
    return self.__add__(other)
  
  def __sub__(self, other):
    a, b = check(self, other)
    return Value(a.value - b.value, a.uncertainty + b.uncertainty)
    
  def __rsub__(self, other):
    a, b = check(self, other)
    return Value(b.value - a.value, a.uncertainty + b.uncertainty)
    
  def __mul__(self, other):
    a, b = check(self, other)
    return Value(a.value * b.value, a.value * b.uncertainty + b.value * a.uncertainty)
    
  def __rmul__(self, other):
    a, b = check(self, other)
    return Value(a.value * b.value, a.value * b.uncertainty + b.value * a.uncertainty)
    
  def __truediv__(self, other):
    a, b = check(self, other)
    return Value(a.value / b.value, (b.value * a.uncertainty - a.value * b.uncertainty) / (b.value ** 2))
  
  def __rtruediv__(self, other):
    a, b = check(self, other)
    return Value(b.value / a.value, (a.value * b.uncertainty - b.value * a.uncertainty) / (a.value ** 2))
  
  def __neg__(self):
    return Value(-self.value, self.uncertainty)
  
  def __str__(self):
    rounded_value, rounded_uncertainty = roundToSignificantFigures(self.value, self.uncertainty)

    return f"{to_non_scientific_string(rounded_value)}±{to_non_scientific_string(rounded_uncertainty)}{(' ' + self.unit) if self.unit else ''}"
  
  def __repr__(self):
    return f"Value({self.value}, {self.uncertainty}, unit={self.unit})"

  def __pow__(self, power):
    a, b = check(self, power)
    return Value(self.value ** b.value, a.value**b.value * (b.value/a.value*a.uncertainty + (Decimal(log(a.value))*b.uncertainty if b.uncertainty != 0 else 0)))

  def short(self):
    rounded_value, rounded_uncertainty = roundToSignificantFigures(self.value, self.uncertainty)

    return f"{to_non_scientific_string(rounded_value)}({''.join(map(str, rounded_uncertainty.as_tuple().digits)) if rounded_uncertainty.as_tuple().exponent < 0 else to_non_scientific_string(rounded_uncertainty)}){(' ' + self.unit) if self.unit else ''}"
  
def sqrt(value: Value):
  return value ** Value(0.5)