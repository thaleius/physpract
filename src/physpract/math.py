from decimal import Decimal
from .uncertainties import Value
import scipy.special as spec
import math as m

def sqrt(value: Value):
  v = value ** Value(0.5)
  v.history = (value.history, 'sqrt')
  return v

def lambertw(v: Value):
  lam = Decimal(spec.lambertw(float(v.value)).real)
  v = Value(Decimal(lam), v.uncertainty*lam/(v.value*(lam + 1)) if v.uncertainty != 0 else 0)
  v.history = (v.history, 'lambertw')
  return v

def exp(v: Value):
  v = Value(Decimal(m.exp(v.value)), Decimal(m.exp(v.value))*v.uncertainty if v.uncertainty != 0 else 0)
  v.history = (v.history, 'exp')
  return v