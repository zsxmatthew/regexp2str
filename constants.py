import os
import re

# operators
ANY = "any"
BRANCH = "branch"
CATEGORY = "category"
IN = "in"
IN_IGNORE = "in_ignore"
LITERAL = "literal"
LITERAL_IGNORE = "literal_ignore"
MAX_REPEAT = "max_repeat"
NEGATE = "negate"
NOT_LITERAL = "not_literal"
NOT_LITERAL_IGNORE = "not_literal_ignore"
RANGE = "range"
SUBPATTERN = "subpattern"

# categories
CATEGORY_DIGIT = "category_digit"
CATEGORY_NOT_DIGIT = "category_not_digit"
CATEGORY_SPACE = "category_space"
CATEGORY_NOT_SPACE = "category_not_space"
CATEGORY_WORD = "category_word"
CATEGORY_NOT_WORD = "category_not_word"

# codes of re pattern parsing
# NOTE: only those codes in below list can be processed
OPCODES = [
    ANY,
    BRANCH,
    CATEGORY,
    IN, IN_IGNORE,
    LITERAL, LITERAL_IGNORE,
    NOT_LITERAL, NOT_LITERAL_IGNORE,
    NEGATE,
    RANGE,
    SUBPATTERN,
    MAX_REPEAT,
    CATEGORY_DIGIT, CATEGORY_NOT_DIGIT,
    CATEGORY_SPACE, CATEGORY_NOT_SPACE,
    CATEGORY_WORD, CATEGORY_NOT_WORD
]

UNICHR_RANGE = (0, 65536)  # range of unicode code points
CHR_RANGE = (0, 256)  # range of ascii values

CATEGORY_DIGIT_PATTERN = r"\d"
CATEGORY_SPACE_PATTERN = r"\s"
CATEGORY_NOT_WORD_PATTERN = r"\W"

uni_re_map = dict(
    CATEGORY_UNI_DIGIT=CATEGORY_DIGIT_PATTERN,
    CATEGORY_UNI_SPACE=CATEGORY_SPACE_PATTERN,
    CATEGORY_UNI_NOT_WORD=CATEGORY_NOT_WORD_PATTERN
)

ascii_re_map = dict(
    CATEGORY_DIGIT=CATEGORY_DIGIT_PATTERN,
    CATEGORY_SPACE=CATEGORY_SPACE_PATTERN,
    CATEGORY_NOT_WORD=CATEGORY_NOT_WORD_PATTERN
)

codes = {}
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# code points / values for special collections of unicode and ascii
unilib_dir = os.path.join(BASE_DIR, 'regexps', 'unilib.ini')
# implicitly import variables
execfile(unilib_dir)

if any(map(lambda key: key not in locals(), uni_re_map.keys() + ascii_re_map.keys())):
    # fill in ini
    with open(unilib_dir, 'w') as f:
        for code in range(*UNICHR_RANGE):
            for k, v in uni_re_map.items():
                if re.match(v, unichr(code), re.UNICODE):
                    codes.setdefault(k, []).append(str(code))

        for code in range(*CHR_RANGE):
            for k, v in ascii_re_map.items():
                if re.match(v, chr(code)):
                    codes.setdefault(k, []).append(str(code))

        for k, v in uni_re_map.items():
            f.write('%s = (%s)' % (k, ','.join(codes[k])))
            f.write('\n')

        for k, v in ascii_re_map.items():
            f.write('%s = (%s)' % (k, ','.join(codes[k])))
            f.write('\n')

__all__ = ['CATEGORY_UNI_DIGIT', 'CATEGORY_UNI_SPACE', 'CATEGORY_UNI_NOT_WORD',
           'CATEGORY_DIGIT', 'CATEGORY_SPACE', 'CATEGORY_NOT_WORD',
           'OPCODES', 'UNICHR_RANGE', 'CHR_RANGE']
