from .uncertainties import Value
from uncertainties import umath
import sympy as sp

def sin(value: Value) -> Value:
  if type(value) == Value:
    return Value(umath.sin(value.ufloat), variable=value.variable.sin())
  return Value(umath.sin(value), variable=sp.sin(value))

def cos(value: Value) -> Value:
  if type(value) == Value:
    return Value(umath.cos(value.ufloat), variable=value.variable.cos())
  return Value(umath.cos(value), variable=sp.cos(value))

def tan(value: Value) -> Value:
  if type(value) == Value:
    return Value(umath.tan(value.ufloat), variable=value.variable.tan())
  return Value(umath.tan(value), variable=sp.tan(value))

def asin(value: Value) -> Value:
  if type(value) == Value:
    return Value(umath.asin(value.ufloat), variable=value.variable.asin())
  return Value(umath.asin(value), variable=sp.asin(value))

def acos(value: Value) -> Value:
  if type(value) == Value:
    return Value(umath.acos(value.ufloat), variable=value.variable.acos())
  return Value(umath.acos(value), variable=sp.acos(value))

def atan(value: Value) -> Value:
  if type(value) == Value:
    return Value(umath.atan(value.ufloat), variable=value.variable.atan())
  return Value(umath.atan(value), variable=sp.atan(value))

def sinh(value: Value) -> Value:
  if type(value) == Value:
    return Value(umath.sinh(value.ufloat), variable=value.variable.sinh())
  return Value(umath.sinh(value), variable=sp.sinh(value))

def cosh(value: Value) -> Value:
  if type(value) == Value:
    return Value(umath.cosh(value.ufloat), variable=value.variable.cosh())
  return Value(umath.cosh(value), variable=sp.cosh(value))

def tanh(value: Value) -> Value:
  if type(value) == Value:
    return Value(umath.tanh(value.ufloat), variable=value.variable.tanh())
  return Value(umath.tanh(value), variable=sp.tanh(value))

def asinh(value: Value) -> Value:
  if type(value) == Value:
    return Value(umath.asinh(value.ufloat), variable=value.variable.asinh())
  return Value(umath.asinh(value), variable=sp.asinh(value))

def acosh(value: Value) -> Value:
  if type(value) == Value:
    return Value(umath.acosh(value.ufloat), variable=value.variable.acosh())
  return Value(umath.acosh(value), variable=sp.acosh(value))

def atanh(value: Value) -> Value:
  if type(value) == Value:
    return Value(umath.atanh(value.ufloat), variable=value.variable.atanh())
  return Value(umath.atanh(value), variable=sp.atanh(value))

def sqrt(value: Value) -> Value:
  if type(value) == Value:
    return Value(umath.sqrt(value.ufloat), variable=value.variable.sqrt())
  return Value(umath.sqrt(value), variable=sp.sqrt(value))

def exp(value: Value) -> Value:
  if type(value) == Value:
    return Value(umath.exp(value.ufloat), variable=value.variable.exp())
  return Value(umath.exp(value), variable=sp.exp(value))

def log(value: Value) -> Value:
  if type(value) == Value:
    return Value(umath.log(value.ufloat), variable=value.variable.log())
  return Value(umath.log(value), variable=sp.log(value))