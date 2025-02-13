from decimal import Decimal
from typing import Literal
from numpy import double
from uncertainties import ufloat, umath as u
from uncertainties.core import AffineScalarFunc
import sympy as sp
from sympy.physics import units
import re

def string_processing(string: str) -> str:
  # replace double parentheses with single parentheses
  p = re.compile(r"(\\left\(){2}(.*?)(\\right\) ?){2}")
  new_string = p.sub(r"\\left(\2\\right)", string)

  # replace trigonometric functions with angular units
  p = re.compile(r" *(\\sin|\\cos|\\tan|\\sinh|\\cosh|\\tanh)\{.*?(\{.+?\}).*?\} *")
  new_string = p.sub("", new_string)

  u = units.__all__

  # replace units with siunitx units
  replacer = lambda x: "\\" + u[u.index(x.group(1))+1]
  new_string = re.sub(r"\\text\{(.+?)\} ?", replacer, new_string)

  # replace \frac with \per
  get = lambda x: x if x is not None else ''
  replacer = lambda x: r"\SI{" + x.group(1) + "}{" + get(x.group(2)) + get(x.group(4)) + (x.group(5).replace("\\", "\\per\\") if x.group(5) is not None else '') + "}"
  new_string = re.sub(r"\\SI\{(.+?)\}\{(.*?)(\\frac\{(.+?)\}\{(.+?)\})*\}", replacer, new_string)

  return new_string

class Value:
  pass

class Variable:
  pass

used_variables: list[str] = []

class Variable:
  def __init__(self, name: sp.Symbol | sp.Function | Variable = None, unit: units.Quantity | None = None, value = None, variables: list[Variable] | None = None):
    # unit
    if unit is None:
      self.unit = None
    elif isinstance(unit, str):
      raise TypeError("Unit must be a sympy.physics.units.Quantity")
    else:
      self.unit = unit

    self.variables = [self] if variables is None else variables
    for variable in self.variables:
      if hasattr(variable, "name") and variable.name is not None and variable.name not in used_variables:
        used_variables.append(str(variable.name))
    
    # variable
    if name is None:
      # generate a new variable
      i = 0
      while True:
        if f"x_{i}" in used_variables:
          i += 1
        else:
          break
      name = f"x_{i}"
      used_variables.append(name)   
      self.name = sp.Symbol(name)   
    elif type(name) == str:
      used_variables.append(name)
      self.name = sp.Symbol(name)
    elif type(name) == Variable:
      self.name = name.name
      self.unit = name.unit
      self.variables = name.variables
    else:
      self.name = name

    if self.name not in used_variables:
      used_variables.append(str(self.name))

    self.value = value

  def __str__(self):
    return str(self.name)
  
  def checkIfNone(self, *args):
    for arg in args:
      if type(arg) == Variable:
        return arg.name is not None
      return arg is not None
  
  def __add__(self, other: Variable) -> Variable:
    if self.unit != other.unit:
      raise ValueError("Units do not match")
    if self.checkIfNone(self, other) is False:
      return None

    if type(other) == Variable:
      return Variable(self.name + other.name, self.unit, variables=self.variables + other.variables)
    return Variable(self.name + other, self.unit, variables=self.variables)
  
  def __sub__(self, other: Variable) -> Variable:
    if self.unit != other.unit:
      raise ValueError("Units do not match")
    if self.checkIfNone(self, other) is False:
      return None

    if type(other) == Variable:
      return Variable(self.name - other.name, self.unit, variables=self.variables + other.variables)
    return Variable(self.name - other, self.unit, variables=self.variables)
  
  def __mul__(self, other: Variable) -> Variable:
    if self.checkIfNone(self, other) is False:
      return None

    if type(other) == Variable:
      unit = self.unit * other.unit if self.unit is not None and other.unit is not None else None
      return Variable(self.name * other.name, unit, variables=self.variables + other.variables)
    return Variable(self.name * other, self.unit, variables=self.variables)
  
  def __truediv__(self, other: Variable) -> Variable:
    if self.checkIfNone(self, other) is False:
      return None

    if type(other) == Variable:
      unit = self.unit / other.unit if self.unit is not None and other.unit is not None else None
      return Variable(self.name / other.name, unit, variables=self.variables + other.variables)
    return Variable(self.name / other, self.unit, variables=self.variables)
  
  def __pow__(self, other: int | float) -> Variable:
    if self.checkIfNone(self, other) is False:
      return None

    if type(other) == Variable:
      return Variable(self.name ** other, self.unit ** other if self.unit is not None else None, variables=self.variables + other.variables)
    return Variable(self.name ** other, self.unit ** other if self.unit is not None else None, variables=self.variables)
  
  def __radd__(self, other: Variable) -> Variable:
    if self.unit != other.unit:
      raise ValueError("Units do not match")
    if self.checkIfNone(self, other) is False:
      return None

    if type(other) == Variable:
      return Variable(other.name + self.name, self.unit, variables=self.variables + other.variables)
    return Variable(other + self.name, self.unit, variables=self.variables)
  
  def __rsub__(self, other: Variable) -> Variable:
    if self.unit != other.unit:
      raise ValueError("Units do not match")
    if self.checkIfNone(self, other) is False:
      return None

    if type(other) == Variable:
      return Variable(other.name - self.name,self.unit, variables=self.variables + other.variables)
    return Variable(other - self.name, self.unit, variables=self.variables)
  
  def __rmul__(self, other: Variable) -> Variable:
    if self.checkIfNone(self, other) is False:
      return None

    if type(other) == Variable:
      unit = self.unit * other.unit if self.unit is not None and other.unit is not None else None
      return Variable(other.name * self.name, unit, variables=self.variables + other.variables)
    return Variable(other * self.name, self.unit, variables=self.variables)
  
  def __rtruediv__(self, other: Variable) -> Variable:
    if self.checkIfNone(self, other) is False:
      return None

    if type(other) == Variable:
      unit = self.unit / other.unit if self.unit is not None and other.unit is not None else None
      return Variable(other.name / self.name, unit, variables=self.variables + other.variables)
    return Variable(other / self.name, self.unit, variables=self.variables)
  
  def __abs__(self) -> Variable:
    return Variable(abs(self.name), self.unit, variables=self.variables)
  
  def __neg__(self) -> Variable:
    return Variable(-self.name, self.unit, variables=self.variables)
  
  def __pos__(self) -> Variable:
    return Variable(+self.name, self.unit, variables=self.variables)
  
  def __eq__(self, other: Variable) -> bool:
    return self.name == other.name
  
  def __ne__(self, other: Variable) -> bool:
    return self.name != other.name
  
  def __lt__(self, other: Variable) -> bool:
    return self.name < other.name
  
  def __le__(self, other: Variable) -> bool:
    return self.name <= other.name
  
  def __gt__(self, other: Variable) -> bool:
    return self.name > other.name
  
  def __ge__(self, other: Variable) -> bool:
    return self.name >= other.name
  
  def sin(self):
    return Variable(sp.sin(self.name), sp.sin(self.unit) if self.unit is not None else None, variables=self.variables)
  
  def cos(self):
    return Variable(sp.cos(self.name), sp.cos(self.unit) if self.unit is not None else None, variables=self.variables)
  
  def tan(self):
    return Variable(sp.tan(self.name), sp.tan(self.unit) if self.unit is not None else None, variables=self.variables)
  
  def asin(self):
    return Variable(sp.asin(self.name), sp.asin(self.unit) if self.unit is not None else None, variables=self.variables)
  
  def acos(self):
    return Variable(sp.acos(self.name), sp.acos(self.unit) if self.unit is not None else None, variables=self.variables)
  
  def atan(self):
    return Variable(sp.atan(self.name), sp.atan(self.unit) if self.unit is not None else None, variables=self.variables)
  
  def sinh(self):
    return Variable(sp.sinh(self.name), sp.sinh(self.unit) if self.unit is not None else None, variables=self.variables)
  
  def cosh(self):
    return Variable(sp.cosh(self.name), sp.cosh(self.unit) if self.unit is not None else None, variables=self.variables)
  
  def tanh(self):
    return Variable(sp.tanh(self.name), sp.tanh(self.unit) if self.unit is not None else None, variables=self.variables)
  
  def asinh(self):
    return Variable(sp.asinh(self.name), sp.asinh(self.unit) if self.unit is not None else None, variables=self.variables)
  
  def acosh(self):
    return Variable(sp.acosh(self.name), sp.acosh(self.unit) if self.unit is not None else None, variables=self.variables)
  
  def atanh(self):
    return Variable(sp.atanh(self.name), sp.atanh(self.unit) if self.unit is not None else None, variables=self.variables)
  
  def sqrt(self):
    return Variable(sp.sqrt(self.name), sp.sqrt(self.unit) if self.unit is not None else None, variables=self.variables)
  
  def exp(self):
    return Variable(sp.exp(self.name), sp.exp(self.unit) if self.unit is not None else None, variables=self.variables)
  
  def log(self):
    return Variable(sp.log(self.name), sp.log(self.unit) if self.unit is not None else None, variables=self.variables)

class Value:
  def __add__(self, other) -> Value:
    if type(other) == Value:
      return Value(self.ufloat + other.ufloat, variable=self.variable + other.variable)
    return Value(self.ufloat + other, variable=self.variable + other)

  def __sub__(self, other) -> Value:
    if type(other) == Value:
      return Value(self.ufloat - other.ufloat, variable=self.variable - other.variable)
    return Value(self.ufloat - other, variable=self.variable - other)
  
  def __mul__(self, other) -> Value:
    if type(other) == Value:
      return Value(self.ufloat * other.ufloat, variable=self.variable * other.variable)
    return Value(self.ufloat * other, variable=self.variable * other)
  
  def __truediv__(self, other) -> Value:
    if type(other) == Value:
      return Value(self.ufloat / other.ufloat, variable=self.variable / other.variable)
    return Value(self.ufloat / other, variable=self.variable / other)
  
  def __pow__(self, other) -> Value:
    if type(other) == Value:
      return Value(self.ufloat ** other.ufloat, variable=self.variable ** other.variable)
    return Value(self.ufloat ** other, variable=self.variable ** other)
  
  def __radd__(self, other) -> Value:
    if type(other) == Value:
      return Value(other.ufloat + self.ufloat, variable=other.variable + self.variable)
    return Value(other + self.ufloat, variable=other + self.variable)
  
  def __rsub__(self, other) -> Value:
    if type(other) == Value:
      return Value(other.ufloat - self.ufloat, variable=other.variable - self.variable)
    return Value(other - self.ufloat, variable=other - self.variable)
  
  def __rmul__(self, other) -> Value:
    if type(other) == Value:
      return Value(other.ufloat * self.ufloat, variable=other.variable * self.variable)
    return Value(other * self.ufloat, variable=other * self.variable)
  
  def __rtruediv__(self, other) -> Value:
    if type(other) == Value:
      return Value(other.ufloat / self.ufloat, variable=other.variable / self.variable)
    return Value(other / self.ufloat, variable=other / self.variable)
  
  def __rpow__(self, other) -> Value:
    if type(other) == Value:
      return Value(other.ufloat ** self.ufloat, variable=other.variable ** self.variable)
    return Value(other ** self.ufloat, variable=other ** self.variable)
  
  def __abs__(self) -> Value:
    return Value(u.abs(self.ufloat), variable=abs(self.variable))
  
  def __neg__(self) -> Value:
    return Value(-self.ufloat, variable=-self.variable)
  
  def __pos__(self) -> Value:
    return Value(+self.ufloat, variable=+self.variable)
  
  def __eq__(self, other: Value) -> bool:
    return self.ufloat == other.ufloat
  
  def __ne__(self, other: Value) -> bool:
    return self.ufloat != other.ufloat
  
  def __lt__(self, other: Value) -> bool:
    return self.ufloat < other.ufloat
  
  def __le__(self, other: Value) -> bool:
    return self.ufloat <= other.ufloat
  
  def __gt__(self, other: Value) -> bool:
    return self.ufloat > other.ufloat
  
  def __ge__(self, other: Value) -> bool:
    return self.ufloat >= other.ufloat  

  def getSignificantFigures(self):
    _, unc, exp = abs(Decimal(self.ufloat.std_dev)).as_tuple()
    uncStr = str(''.join(map(str, unc)))

    sigPos = -1

    for i in range(len(uncStr)):
      char = uncStr[i]
      if char != '0':
        if not i == len(uncStr)-1 and char == '1' or char == '2':
          sigPos = i+1
        else:
          sigPos = i
        break

    decPos = len(uncStr) + exp
    s = list(map(int, uncStr[sigPos:16]))
    if len(s) > 0 and sum(s)/len(s) in [0., 9.]:
      n = sum(s)/len(s)
      if n == 0.:
        uncStr = uncStr[:sigPos]
      if n == 9.:
        uncStr = uncStr[:sigPos-1] + str(int(uncStr[sigPos-1])+1)
      sigPos -= 1
    else:
      uncStr = uncStr[:sigPos] + str(int(uncStr[sigPos])+1)
    
    uncStrS = uncStr
    if decPos <= 0:
      uncStr = '0.' + (-decPos)*'0' + uncStr
    elif decPos > len(uncStr):
      uncStr += (decPos-len(uncStr))*'0'
      uncStrS = uncStr
    else:
      uncStr = uncStr[:decPos] + '.' + uncStr[decPos:]

    rndPos = sigPos - decPos
    
    return uncStr, uncStrS, rndPos
  
  class V:
    class E:
      def __init__(self, context, type: Literal["value", "uncertainty"], variables):
        self.context = context
        self.type = type
        self.variables = variables

      def __str__(self):
        if self.type == "value":
          return str(self.context.context.variable.name)
        elif self.type == "uncertainty":
          return str(self.context.func)
      
      def __repr__(self):
        return str(self)
      
      def latex(self):
        values = self.context.get_values(self.variables)
        if self.type == "value":
          subs = {
            value.name: sp.Symbol(f"\\SI{{{value.value.value}({value.value.uncertainty_b})}}{{{sp.latex(value.unit)}}}" if value.unit is not None else f"\\num{{{value.value.value}({value.value.uncertainty_b})}}") for value in values
          }
          parts = sp.latex(self.context.context.variable.name), sp.latex(self.context.context.variable.name.subs(subs)), r"\SI{" + self.context.context.value.value + "(" + self.context.context.uncertainty_b + ")" + r"}{" + sp.latex(self.context.context.variable.unit) + r"}"
        elif self.type == "uncertainty":
          subs = {}
          for value in values:
            subs[value.name] = sp.Symbol(f"\\left(\\SI{{{value.value.value}}}{{{sp.latex(value.unit)}}}\\right)" if value.unit is not None else f"\\left(\\num{{{value.value.value}}}\\right)")
            subs[sp.Symbol("\\Delta " + str(value.name))] = sp.Symbol(f"\\left(\\SI{{{value.value.uncertainty}}}{{{sp.latex(value.unit)}}}\\right)" if value.unit is not None else f"\\left(\\num{{{value.value.uncertainty}}}\\right)")
          parts = r"\Delta\left(" + sp.latex(self.context.context.variable.name) + r"\right)", sp.latex(self.context.func), sp.latex(self.context.func.subs(subs)), (r"\SI{" + self.context.context.uncertainty.value + r"}{" + sp.latex(self.context.context.variable.unit) + r"}" if self.context.context.variable.unit is not None else r"\num{" + self.context.context.uncertainty.value + r"}")
        
        p = re.compile(r"(\\left\(){2}(.*?)(\\right\) ?){2}")
        return string_processing(p.sub(r"\\left(\2\\right)", "=".join(parts)))

    def __init__(self, value: str, context: Value, type: Literal["value", "uncertainty"]):
      self.value = value
      self.context = context
      self.type = type

    def __str__(self):
      return self.value
    
    def __repr__(self):
      return str(self)

    def get_values(self, variables):
      if len(variables) == 0:
        return {}

      return list(filter(lambda x: x.name in variables, self.context.variable.variables))
    
    def get_value_equation(self):
      return self.E(self, "value", self.context.variable.name.free_symbols)

    def get_uncertainty_equation(self):
      variables = self.context.variable.name.free_symbols
      f = self.context.variable.name

      if len(variables) == 0:
        return 0
      
      func = sp.sqrt(sum([sp.diff(f, variable)**2 * sp.Symbol(f"\\Delta {str(variable)}")**2 for variable in variables]))

      values = list(filter(lambda x: x.name in variables, self.context.variable.variables))

      self.func = func
      self.values = values

      variables = self.func.free_symbols
      for variable in variables:
        new_variable = sp.Symbol(str(variable).replace('(', '\\left(').replace(')', '\\right)'))
        self.func = self.func.replace(variable, new_variable)

      return self.E(self, "uncertainty", variables)
    
    def get_equation(self):
      if self.type == "value":
        return self.get_value_equation()
      elif self.type == "uncertainty":
        return self.get_uncertainty_equation()
  
  def round(self):
    uncertainty, self.uncertainty_b, rndPos = self.getSignificantFigures()
    self.uncertainty = self.V(uncertainty, self, "uncertainty")
    self.u = self.uncertainty
    value = str(round(self.vnr, rndPos+1))
    decPos = value.find('.')
    pos = rndPos + (0 if rndPos < 0 else 1)
    if decPos == -1:
      decPos = len(value)
    value = value.replace('.', '')
    value = value[:decPos+pos+1]
    value += ((decPos if (rndPos < 0) else decPos + pos)-len(value))*'0'

    if rndPos >= 0:
      value = value[:decPos] + '.' + value[decPos:]
    self.value = self.V(value, self, "value")
    self.v = self.value
  
  def __init__(self, value: double | Value, uncertainty: double | None = None, variable: str | None = None, unit: None  = None):
    self.noUnc = False
    if type(value) in [float, int] and type(uncertainty) in [float, int]:
      self.ufloat = ufloat(value, uncertainty)
    elif type(value) == AffineScalarFunc:
      self.ufloat = value
    else:
      self.ufloat = value
      self.noUnc = True
      # raise TypeError("Uncertainty must be specified if the value is of type float, otherwise it must be None if the value is of type ufloat")
    
    if not self.noUnc:
      self.value_not_rounded = self.ufloat.nominal_value
      self.vnr = self.value_not_rounded
      self.uncertainty_not_rounded = self.ufloat.std_dev
      self.unr = self.uncertainty_not_rounded

      self.round()

    self.variable = Variable(variable, unit, self)

  def __str__(self):
    if self.noUnc:
      return f"{self.value}" + (f" {self.variable.unit}" if self.variable.unit is not None else "")
    return f"{self.value} ± {self.uncertainty}" + (f" {self.variable.unit}" if self.variable.unit is not None else "")
  
  def eq(self):
    if self.noUnc:
      return f"{self.variable.name} = " + f"{self.value}" + (f" {self.variable.unit}" if self.variable.unit is not None else "")
    return f"{self.variable.name} = " + f"{self.value} ± {self.uncertainty}" + (f" {self.variable.unit}" if self.variable.unit is not None else "")
  
  def latex(self, equation=False):
    e = ""
    unc = "" if self.noUnc else f"({self.uncertainty_b})"
    if equation:
      e = f"{sp.latex(self.variable.name)}=" + (f"\\SI{{{self.value}{unc}}}{{{sp.latex(self.variable.unit)}}}" if self.variable.unit is not None else f"\\num{{{self.value}{unc}}}")
    else:
      e = f"\\SI{{{self.value}{unc}}}{{{sp.latex(self.variable.unit)}}}" if self.variable.unit is not None else f"\\num{{{self.value}{unc}}}"
    return string_processing(e)

  def __repr__(self):
    return str(self)
  
  def __float__(self):
    return self.ufloat