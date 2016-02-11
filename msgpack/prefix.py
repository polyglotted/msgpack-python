class Prefix:
    def __init__(self):
        pass

    @staticmethod
    def is_fix_int(b):
        v = b & 0xFF
        return v <= 0x7f or v >= 0xe0

    @staticmethod
    def is_pos_fix_int(b):
        return (b & Prefix.POSFIXINT_MASK) == 0

    @staticmethod
    def is_neg_fix_nt(b):
        return (b & Prefix.NEGFIXINT_PREFIX) == Prefix.NEGFIXINT_PREFIX

    @staticmethod
    def is_fix_str(b):
        return (b & 0xe0) == Prefix.FIXSTR_PREFIX

    @staticmethod
    def is_fixed_array(b):
        return (b & 0xf0) == Prefix.FIXARRAY_PREFIX

    @staticmethod
    def is_fixed_map(b):
        return (b & 0xe0) == Prefix.FIXMAP_PREFIX

    @staticmethod
    def is_fixed_raw(b):
        return (b & 0xe0) == Prefix.FIXSTR_PREFIX

    POSFIXINT_MASK = 0x80
    FIXMAP_PREFIX = 0x80
    FIXARRAY_PREFIX = 0x90
    FIXSTR_PREFIX = 0xa0
    NIL = 0xc0
    NEVER_USED = 0xc1
    FALSE = 0xc2
    TRUE = 0xc3
    BIN8 = 0xc4
    BIN16 = 0xc5
    BIN32 = 0xc6
    EXT8 = 0xc7
    EXT16 = 0xc8
    EXT32 = 0xc9
    FLOAT32 = 0xca
    FLOAT64 = 0xcb
    UINT8 = 0xcc
    UINT16 = 0xcd
    UINT32 = 0xce
    UINT64 = 0xcf
    INT8 = 0xd0
    INT16 = 0xd1
    INT32 = 0xd2
    INT64 = 0xd3
    FIXEXT1 = 0xd4
    FIXEXT2 = 0xd5
    FIXEXT4 = 0xd6
    FIXEXT8 = 0xd7
    FIXEXT16 = 0xd8
    STR8 = 0xd9
    STR16 = 0xda
    STR32 = 0xdb
    ARRAY16 = 0xdc
    ARRAY32 = 0xdd
    MAP16 = 0xde
    MAP32 = 0xdf
    NEGFIXINT_PREFIX = 0xe0
