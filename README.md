# Description
This is a package primarily created to help with writing the protocols for the physical practicals at the TU Berlin, created by a student, who was tired of writing the long equations to show the calculation of uncertainties. To calculate the uncertainties, the package uses the gaussian error propagation.

The package is still in development and will be updated with more features in the future.

# Features
## Calculation of uncertainties
Core feature of this package is the rounding of the uncertainties to the correct number of significant figures. Suggested by the physical practicals of the TU Berlin is the following rule:
- If the first non zero digit of the uncertainty is 1 or 2, round to 2 significant non zero figures.
- Else round to 1 non zero significant figure.
- The significant figure is alway rounded up.

## Get values in LaTeX format
The package also provides a function to get the function to calculate the uncertainty in LaTeX format without and with substitution of the variables with the values.

# Installation
To install the package, simply download the newest release from the [releases page](https://github.com/thaleius/physpract/releases) page and install it with pip:
```bash
pip install physpract-{version}-py3-none-any.whl
```

# Usage
To use the package, simply import it and use the functions provided by the package. The package is still in development and will be updated with more features in the future.
## Example
### Basic usage
To define a value with an uncertainty, simply create a new `Value` object with the value and the uncertainty as arguments. The value can be accessed with the `value` attribute and the uncertainty with the `uncertainty` attribute. The value can be printed with the `print` function.
```python
from physpract.uncertainties import Value

a = Value(1, 0.1)
b = Value(2, 0.2)

c = a + b

# Print the value
print(c)
# Output: 3.00 ± 0.23

# Print the value and the uncertainty
print(c.value, c.uncertainty)
# or
print(c.v, c.u)
# Output: 3.00 0.23

# Print the not rounded value and the uncertainty
print(c.value_not_rounded, c.uncertainty_not_rounded)
# or
print(c.vnr, c.unr)
# Output: 3.0 0.223606797749979
```

### Usage with variable names
To use the variable names in the LaTeX output, simply pass the variable names as a string to the `Value` object.
```python
from physpract.uncertainties import Value

a = Value(1, 0.1, "a")
b = Value(2, 0.2, "b")

c = a + b
print(c)
# Output: a + b = 3.00 ± 0.23
```

### Usage with variable names and units
To use the variable names and units in the LaTeX output, simply pass the variable names and units as a string to the `Value` object. For the units, `sympy.physics.units` must be used.
```python
from physpract.uncertainties import Value
from sympy.physics.units import meter, second

a = Value(1, 0.1, "a", meter)
b = Value(2, 0.2, "b", second)

c = a/b

# Print the value
print(c)
# Output: a/b = 0.50 ± 0.08 meter/second
```

### Print the LaTeX output
To print the LaTeX output of the equation, use the `latex` function.
```python
from physpract.uncertainties import Value
from sympy.physics.units import meter, second

a = Value(1, 0.1, "a", meter)
b = Value(2, 0.2, "b", second)

c = a/b

# Print the LaTeX output
print(c.latex())
# Output: \SI{0.50(8)}{\meter\per\second}

# Print the LaTeX output with equation
print(c.latex(equation=True))
# Output: \frac{a}{b}=\SI{0.50(8)}{\meter\per\second}
```
#### LaTeX output
$$\frac{a}{b} = \left(0.50 \pm 0.08\right)\frac{\text{m}}{\text{s}}$$

### Print the equation
To print the equation to calculate the uncertainty, use the `get_equation` function of either the `Value.value` or `Value.uncertainty` attribute. The equation is returned as a string and can be printed with the `print` function. To print the equation in LaTeX format, use the `latex` function of `get_equation`.
```python
from physpract.uncertainties import Value
from sympy.physics.units import meter, second

a = Value(1, 0.1, "a", meter)
b = Value(2, 0.2, "b", second)

c = a/b

# Print the equation of the value
print(c.value.get_equation())
# Output: a/b

# Print the LaTeX equation of the value
print(c.value.get_equation().latex())
# Output: \frac{a}{b}=\frac{\SI{1.0(0.1)}{\meter}}{\SI{2.0(0.2)}{\second}}

# Print the equation of the uncertainty
print(c.uncertainty.get_equation())
# Output: sqrt(\Delta a**2/b**2 + \Delta b**2*a**2/b**4)

# Print the LaTeX equation of the uncertainty
print(c.uncertainty.get_equation().latex())
# Output: \Delta\left(\frac{a}{b}\right)=\sqrt{\frac{\Delta a^{2}}{b^{2}} + \frac{\Delta b^{2} a^{2}}{b^{4}}}=\sqrt{\frac{\left(\SI{0.1}{\meter}\right)^{2}}{\left(\SI{2.0}{\second}\right)^{2}} + \frac{\left(\SI{0.2}{\second}\right)^{2} \left(\SI{1.0}{\meter}\right)^{2}}{\left(\SI{2.0}{\second}\right)^{4}}}
```
#### LaTeX output
*Value:*

$$\frac{a}{b}=\frac{\left(1.0 \pm 0.1\right)~\text{m}}{\left(2.0 \pm 0.2\right)~\text{s}}$$

*Uncertainty:*

$$\Delta\left(\frac{a}{b}\right)=\sqrt{\frac{\Delta a^{2}}{b^{2}} + \frac{\Delta b^{2} a^{2}}{b^{4}}}=\sqrt{\frac{\left(0.1~\text{m}\right)^{2}}{\left(2.0~\text{s}\right)^{2}} + \frac{\left(0.2~\text{s}\right)^{2} \left(1.0~\text{m}\right)^{2}}{\left(2.0~\text{s}\right)^{4}}}$$