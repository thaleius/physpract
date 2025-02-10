import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from physpract.uncertainties import Value
from physpract.math import *

from sympy.physics import units

values: list[tuple[Value, str]] = [
  (Value(34, 0.0522), "34.00 ± 0.06"),
  (Value(0.554, 0.0002), "0.5540 ± 0.0002"),
  (Value(1.234, 0.0123), "1.234 ± 0.013"),
  (Value(1234, 225), "1230 ± 230"),
  (Value(0.0001234, 0.000000225), "0.00012340 ± 0.00000023"),
  (Value(1.201, 0.1), "1.2 ± 0.1"),
  (Value(1.201, 0.3), "1.2 ± 0.3"),
]

for value, expected in values:
  print(str(value) == expected, str(value), expected)

a = Value(34, 0.0522, variable="a", unit=units.meter)
b = Value(2, 0.2, "b", units.second)
c = Value(0.554, 0.0002, variable="c", unit=units.rad)
d = Value(1.234, 0.0123, "d", units.kilogram)

c = a/b/d*sin(c)

print(c.latex())
