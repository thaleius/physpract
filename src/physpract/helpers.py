from decimal import Decimal, DecimalTuple

def increment_digit(digits: list[int]) -> tuple[int]:
    if len(digits) == 0:
        return (1,)
    if digits[-1] == 9:
        digits[-1] = 0
        return increment_digit(digits[:-1]) + (0,)
    else :
        digits[-1] += 1
        return tuple(digits)

def getSignificantFigures(uncertainty):
    _, digits, exp = abs(uncertainty if type(uncertainty) == Decimal else Decimal(uncertainty)).as_tuple()
    digits = list(digits)

    # remove trailing zeros and adjust exponent
    # while len(digits) > 0 and digits[-1] == 0:
    #     digits.pop()
    #     exp += 1

    unc = None
    if len(digits) == 1 or sum(digits[1:]) == 0:
        unc = Decimal(DecimalTuple(sign=0, digits=digits, exponent=exp))
    else:
        if digits[0] == 1 or digits[0] == 2:
            exp = exp+(len(digits)-2)
            if len(digits) > 2:
                digits = increment_digit(digits[:2])
                # TODO: if rounding down is more than 5% different, round up instead
            unc = Decimal(DecimalTuple(sign=0, digits=(digits), exponent=exp)).quantize(Decimal('1e{}'.format(exp)))
        else:
            exp = exp+(len(digits)-1)
            unc = Decimal(DecimalTuple(sign=0, digits=(increment_digit(digits[:1])), exponent=exp))
    return unc, exp

def roundToSignificantFigures(value, uncertainty) -> tuple[Decimal, Decimal]:
    print(value, uncertainty)
    if uncertainty == 0:
        return value, uncertainty
    unc, pos = getSignificantFigures(uncertainty)
    if type(value) != Decimal:
        value = Decimal(value)
    rounded_uncertainty = unc
    print(value, pos)
    rounded_value = value.quantize(Decimal('1e{}'.format(pos)))
    return rounded_value, rounded_uncertainty

def to_non_scientific_string(value: Decimal) -> str:
    exp = value.as_tuple().exponent
    return f'{value:.{abs(exp) if exp < 0 else 0}f}'

def bracket_notation(value: Decimal, uncertainty: Decimal) -> str:
    vt = value.as_tuple()
    ut = uncertainty.as_tuple()
    return to_non_scientific_string(uncertainty.scaleb(-ut.exponent) if len(ut.digits) < len(vt.digits) or len(ut.digits) <= -ut.exponent else uncertainty)