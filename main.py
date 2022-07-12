# Problem 97:
#     Large Non-Mersenne Prime
#
# Description:
#     The first known prime found to exceed one million digits was discovered in 1999,
#       and is a Mersenne prime of the form 2^6972593−1;
#       it contains exactly 2,098,960 digits.
#     Subsequently other Mersenne primes, of the form 2^p−1,
#       have been found which contain more digits.
#
#     However, in 2004 there was found a massive non-Mersenne prime
#       which contains 2,357,207 digits: 28433 × 2^7830457 + 1.
#
#     Find the last ten digits of this prime number.

from typing import List


def int_to_ten_digits(n: int) -> List[int]:
    """
    Given an integer `n`,
      return the representation of [n](mod 10^10)
      as a list of reversed last 10 digits.

    Args:
        n (int): Integer

    Returns:
        (List[int]):
            Representation of [n](mod 10^10) as reversed list of 10 digits

    Raises:
        AssertError: if incorrect args are given
    """
    assert type(n) == int

    # Reduce to mod 10^10
    _, n = divmod(n, 10**10)

    # Convert to reversed list of digits
    d = list(map(int, list(str(n))))
    d = list(reversed(d)) + [0 for _ in range(10-len(d))]
    return d


def add_ten_digits(x: List[int], y: List[int]) -> List[int]:
    """
    Given two numbers `x` and `y` in mod 10^10,
      represented as lists of their reversed 10 digits,
      return the list representation of [x + y](mod 10^10).

    Args:
        x (List[int]): Length-10 list of reversed digits [0-9]
        y (List[int]): Length-10 list of reversed digits [0-9]

    Returns:
        (List[int]):
            Length-10 list of reversed digits of [x+y](mod 10^10)

    Raises:
        AssertError: if incorrect args are given
    """
    assert type(x) == list and len(x) == 10 and all(map(lambda j: type(j) == int and 0 <= j < 10, x))
    assert type(y) == list and len(y) == 10 and all(map(lambda j: type(j) == int and 0 <= j < 10, y))

    carry = 0
    z = int_to_ten_digits(0)
    for i in range(10):
        carry, z[i] = divmod(x[i] + y[i] + carry, 10)
    return z


def multiply_ten_digits_single(x: List[int], d: int) -> List[int]:
    """
    Given a number `x` in mod 10^10,
      represented as a list of its reversed 10 digits,
      and a single digit number `d`,
      return the list representation of [x*d](mod 10^10).

    Args:
        x (List[int]): Length-10 list of reversed digits [0-9]
        d (int): Single-digit number

    Returns:
        (List[int]):
            Length-10 list of reversed digits of [x*d](mod 10^10)

    Raises:
        AssertError: if incorrect args are given
    """
    assert type(x) == list and len(x) == 10 and all(map(lambda j: type(j) == int and 0 <= j < 10, x))
    assert type(d) == int and 0 <= d < 10

    if d == 1:
        return x
    else:
        z = int_to_ten_digits(0)
        if d != 0:
            carry = 0
            for i in range(10):
                carry, z[i] = divmod(x[i] * d + carry, 10)
        return z


def multiply_ten_digits(x: List[int], y: List[int]) -> List[int]:
    """
    Given two numbers `x` and `y` in mod 10^10,
      represented as lists of their reversed 10 digits,
      return the list representation of [x*y](mod 10^10).

    Args:
        x (List[int]): Length-10 list of reversed digits [0-9]
        y (List[int]): Length-10 list of reversed digits [0-9]

    Returns:
        (List[int]):
            Length-10 list of reversed digits of [x+y](mod 10^10)

    Raises:
        AssertError: if incorrect args are given
    """
    assert type(x) == list and len(x) == 10 and all(map(lambda j: type(j) == int and 0 <= j < 10, x))
    assert type(y) == list and len(y) == 10 and all(map(lambda j: type(j) == int and 0 <= j < 10, y))

    z = int_to_ten_digits(0)
    for i in range(10):
        d = multiply_ten_digits_single([0 for _ in range(i)] + x[:10-i], y[i])
        z = add_ten_digits(z, d)
    return z


def main() -> int:
    """
    Returns the last ten digits of the
      large non-Mersenne prime: 28433 × 2^7830457 + 1

    Returns:
        (int):
            Value of [28433 × 2^7830457 + 1](mod 10^10)
    """
    # Last 10 digits in reverse-order (ones-digit upwards)
    result = int_to_ten_digits(1)

    # First raise to 2 to power 7830457, in mod 10^10
    e = 7830457
    curr_pow = int_to_ten_digits(2)
    while e > 0:
        e, r = divmod(e, 2)
        if r == 1:
            result = multiply_ten_digits(result, curr_pow)
        else:
            pass
        curr_pow = multiply_ten_digits(curr_pow, curr_pow)

    # Multiply by 28433
    a = int_to_ten_digits(28433)
    result = multiply_ten_digits(result, a)

    # Add 1
    b = int_to_ten_digits(1)
    result = add_ten_digits(result, b)

    result.reverse()
    return int(''.join(map(str, result)))


if __name__ == '__main__':
    last_ten_digits = main()
    print('Last ten digits of 28433 × 2^7830457 + 1:')
    print('  {}'.format(last_ten_digits))
