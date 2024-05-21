from .uncertainties import Value
from uncertainties import umath
import sympy as sp

def sin(value: Value) -> Value:
  return Value(umath.sin(value.ufloat), variable=value.variable.sin())

def cos(value: Value) -> Value:
  return Value(umath.cos(value.ufloat), variable=value.variable.cos())

def tan(value: Value) -> Value:
  return Value(umath.tan(value.ufloat), variable=value.variable.tan())

def asin(value: Value) -> Value:
  return Value(umath.asin(value.ufloat), variable=value.variable.asin())

def acos(value: Value) -> Value:
  return Value(umath.acos(value.ufloat), variable=value.variable.acos())

def atan(value: Value) -> Value:
  return Value(umath.atan(value.ufloat), variable=value.variable.atan())

def sinh(value: Value) -> Value:
  return Value(umath.sinh(value.ufloat), variable=value.variable.sinh())

def cosh(value: Value) -> Value:
  return Value(umath.cosh(value.ufloat), variable=value.variable.cosh())

def tanh(value: Value) -> Value:
  return Value(umath.tanh(value.ufloat), variable=value.variable.tanh())

def asinh(value: Value) -> Value:
  return Value(umath.asinh(value.ufloat), variable=value.variable.asinh())

def acosh(value: Value) -> Value:
  return Value(umath.acosh(value.ufloat), variable=value.variable.acosh())

def atanh(value: Value) -> Value:
  return Value(umath.atanh(value.ufloat), variable=value.variable.atanh())

def sqrt(value: Value) -> Value:
  return Value(umath.sqrt(value.ufloat), variable=value.variable.sqrt())

def exp(value: Value) -> Value:
  return Value(umath.exp(value.ufloat), variable=value.variable.exp())

def log(value: Value) -> Value:
  return Value(umath.log(value.ufloat), variable=value.variable.log())