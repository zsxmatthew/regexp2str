# --*-- coding: utf-8 --*--
from importlib import import_module
import random
from re import error, UNICODE

from core.regexps.constants import (
    CATEGORY_UNI_DIGIT, CATEGORY_UNI_SPACE, CATEGORY_UNI_NOT_WORD,
    CATEGORY_DIGIT, CATEGORY_SPACE, CATEGORY_NOT_WORD,
    OPCODES, UNICHR_RANGE, CHR_RANGE
)
from core.regexps import ops


def deduce(flag, *choices):
    """
    dispatch parsed re pattern
    :param flag: 0 for ascii and UNICODE (UNICODE) for unicode
    :param choices:
    :return:
    """
    result = []
    try:
        for choice in choices:
            code, value = choice
            if code is None:
                code = 'in'
            result.append(code_interpreters[code](flag, value))
    except KeyError as e:
        print "Code '%s' not supported." % e.args[0]
        raise error

    result = "".join(result)
    return result


def code_any(flag, value):
    uni = flag == UNICODE
    if value is None:
        result = uni and unichr(random.randrange(*UNICHR_RANGE)).encode('utf-8') or chr(random.randrange(*CHR_RANGE))
        return result
    else:
        raise error


def code_in(flag, choices):
    """
    [] or \ sequence escapes
    """
    choice = choices[random.randint(1, len(choices)) - 1]
    if isinstance(choice, tuple):
        result = deduce(flag, choice)
        return result
    else:
        result = deduce(flag, *choice)
        return result


def code_branch(flag, value):
    """
    |
    """
    result = deduce(flag, value)
    return result


def code_literal(flag, value):
    """
    literals
    """
    if flag == UNICODE:  # UNICODE
        result = unichr(value).encode('utf-8')
        return result
    else:
        result = chr(value)
        return result


def code_max_repeat(flag, value):
    """
    + * ? {}
    """
    start, stop, choices = value
    stop = 100 if stop > 100 else stop
    repeat = random.randrange(start, stop + 1)
    result = []
    for _ in xrange(repeat):
        result.append(deduce(flag, *choices))
    result = ''.join(result)
    return result


def code_category(flag, value):
    result = deduce(flag, (value, None))
    return result


def code_category_digit(flag, not_used):
    """
    \d
    """
    if flag == UNICODE:  # UNICODE
        result = unichr(random.choice(CATEGORY_UNI_DIGIT)).encode('utf-8')
        return result
    else:
        result = chr(random.choice(CATEGORY_DIGIT))
        return result


def code_category_not_digit(flag, not_used):
    """
    \D
    default to utf-8 encoding if UNICODE flag is specified
    """
    uni = flag == UNICODE
    while True:
        code = random.randrange(*UNICHR_RANGE) if uni else random.randrange(*CHR_RANGE)
        if code not in (CATEGORY_UNI_DIGIT if uni else CATEGORY_DIGIT):
            result = unichr(code).encode('utf-8') if uni else chr(code)
            return result


def code_category_space(flag, not_used):
    """
    \s
    """
    if flag == UNICODE:  # UNICODE
        result = unichr(random.choice(CATEGORY_UNI_SPACE)).encode('utf-8')
        return result
    else:
        result = chr(random.choice(CATEGORY_SPACE))
        return result


def code_category_not_space(flag, not_used):
    """
    \S
    default to utf-8 encoding if UNICODE flag is specified
    """
    uni = flag == UNICODE
    while True:
        code = random.randrange(*UNICHR_RANGE) if uni else random.randrange(*CHR_RANGE)
        if code not in (CATEGORY_UNI_SPACE if uni else CATEGORY_SPACE):
            result = unichr(code).encode('utf-8') if uni else chr(code)
            return result


def code_category_word(flag, not_used):
    """
    \w
    """
    uni = flag == UNICODE
    while True:
        code = random.randrange(*UNICHR_RANGE) if uni else random.randrange(*CHR_RANGE)
        if code not in (CATEGORY_UNI_NOT_WORD if uni else CATEGORY_NOT_WORD):
            result = unichr(code).encode('utf-8') if uni else chr(code)
            return result


def code_category_not_word(flag, not_used):
    """
    \W
    default to utf-8 encoding if UNICODE flag is specified
    """
    if flag == UNICODE:
        result = unichr(random.choice(CATEGORY_UNI_NOT_WORD)).encode('utf-8')
        return result
    else:
        result = chr(random.choice(CATEGORY_NOT_WORD))
        return result


def code_range(flag, value):
    """
    - within []
    """
    start, stop = value
    code = random.randrange(start, stop + 1)
    if flag == UNICODE:
        result = unichr(code).encode('utf-8')
        return result
    else:
        result = chr(code)
        return result


def code_subpattern(flag, value):
    """
    ()
    """
    result = deduce(flag, *value[1])
    return result


code_interpreters = {}

for op_code in OPCODES:
    if hasattr(ops, 'code_%s' % op_code):
        code_interpreters[op_code] = getattr(ops, 'code_%s' % op_code)
