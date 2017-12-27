# --*-- coding: utf-8 --*--
from re import sre_parse, error

from core.regexps.ops import deduce


def rand_reg(source, flag=0, pattern=None):
    """
    generates a random string (which may include utf-8 encoded unicode) as per a re pattern string
    :param source: re pattern string
    :param flag: 0 for ascii and 32 (re.UNICODE) for unicode
    :param pattern: not used parameter
    :return: generated string
    """
    result = []
    try:
        result.append(deduce(flag, *sre_parse.parse(source, flag, pattern)))
    except error:
        return u"" if flag == re.UNICODE else ""
    else:
        return ("".join(result)).decode('utf-8') if flag == re.UNICODE else "".join(result)


if __name__ == '__main__':
    import re
    p = [r'\w+\W?[ab0-9]{1,2}3{3}(\w|3?|ab){,2}', r'.*', r'3ab[1-2]?\W(?P<g>ab)']
    flag = 0
    for _p in p:
        rr = rand_reg(_p, flag=flag)
        print '"%s"' % rr
        print re.match(_p, rr, flags=flag) and True or (sre_parse.parse(_p), rr)
