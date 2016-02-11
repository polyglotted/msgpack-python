import struct
from io import BytesIO

from .prefix import Prefix


class Packer:
    def __init__(self):
        self.buf = BytesIO()

    def get_bytes(self):
        return self.buf.getvalue()

    def struct_pack(self, fmt, value):
        self.buf.write(struct.pack(fmt, value))

    def write_byte(self, value):
        self.struct_pack('B' if value >= 0 else 'b', value)

    def write_short(self, value, prefix=None):
        if prefix is None:
            prefix = Prefix.INT16 if value < 0 else Prefix.UINT16
            self.write_byte(prefix)
        else:
            assert prefix in [Prefix.INT16, Prefix.UINT16], 'write_short expects prefix %s or %s but received %s' % (
                Prefix.INT16, Prefix.UINT16, prefix)
        self.struct_pack('>H' if prefix == Prefix.UINT16 else '>h', value)

    def write_int(self, value, prefix=None):
        if prefix is None:
            prefix = Prefix.INT32 if value < 0 else Prefix.UINT32
            self.write_byte(prefix)
        else:
            assert prefix in [Prefix.INT32, Prefix.UINT32], 'write_int expects prefix %s or %s but received %s' % (
                Prefix.INT32, Prefix.UINT32, prefix)
        self.struct_pack('>I' if prefix == Prefix.UINT32 else '>i', value)

    def write_long(self, value, prefix=None):
        if prefix is None:
            prefix = Prefix.INT64 if value < 0 else Prefix.UINT64
            self.write_byte(prefix)
        else:
            assert prefix in [Prefix.INT64, Prefix.UINT64], 'write_long expects prefix %s or %s but received %s' % (
                Prefix.INT64, Prefix.UINT64, prefix)
        self.struct_pack('>Q' if prefix == Prefix.UINT64 else '>q', value)

    def write_float(self, value, prefix=None):
        if prefix is None:
            self.write_byte(Prefix.FLOAT32)
        else:
            assert prefix == Prefix.FLOAT32, 'write_float expects prefix %s but received %s' % (Prefix.FLOAT32, prefix)
        self.struct_pack('>f', value)

    def write_double(self, value, prefix=None):
        if prefix is None:
            self.write_byte(Prefix.FLOAT64)
        else:
            assert prefix == Prefix.FLOAT64, 'write_double expects prefix %s but received %s' % (Prefix.FLOAT64, prefix)
        self.struct_pack('>d', value)

    def write_payload(self, bytes):
        self.buf.write(bytes)

    def pack_nil(self):
        self.write_byte(Prefix.NIL)

    def pack_boolean(self, value):
        self.write_byte(Prefix.TRUE if value is True else Prefix.FALSE)

    def pack_int(self, value):
        if -0x20 <= value <= 0x7F:
            self.write_byte(value)
        elif -0x80 <= value <= 0xFF:
            self.write_byte(Prefix.INT8 if value < 0 else Prefix.UINT8)
            self.write_byte(value)
        elif -0x8000 <= value <= 0xFFFF:
            self.write_short(value)
        elif -0x80000000 <= value <= 0xFFFFFFFF:
            self.write_int(value)
        elif -0x8000000000000000 <= value <= 0xfffffffffffff000:
            self.write_long(value)
        else:
            raise ValueError('unable pack int with value %s' % value)

    def pack_float(self, value):
        self.write_float(value)

    def pack_double(self, value):
        self.write_double(value)

    def pack(self, value):
        if value is None:
            self.pack_nil()
        elif isinstance(value, bool):
            self.pack_boolean(value)
        elif isinstance(value, int) or isinstance(value, long):
            self.pack_int(value)
        elif isinstance(value, float) and abs(value) <= 3.4028234663852886e+38:
            self.pack_float(value)
        elif isinstance(value, float) and abs(value) > 3.4028234663852886e+38:
            self.pack_double(value)
        elif isinstance(value, str):
            self.pack_string(value)
        elif isinstance(value, list):
            self.pack_array(value)
        elif isinstance(value, dict):
            self.pack_map(value)
        elif isinstance(value, bytearray):
            self.pack_binary(value)
        else:
            raise ValueError('unhandled value %s' % value)

    def pack_string(self, value):
        ba = value.encode(encoding='UTF-8')
        self.pack_raw_string_header(len(ba))
        self.write_payload(ba)

    def pack_raw_string_header(self, length):
        if length < (1 << 5):
            self.write_byte(Prefix.FIXSTR_PREFIX | length)
        elif length < (1 << 8):
            self.write_byte(Prefix.STR8)
            self.write_byte(length)
        elif length < (1 << 16):
            self.write_byte(Prefix.STR16)
            self.write_short(length, Prefix.UINT16)
        else:
            self.write_byte(Prefix.STR32)
            self.write_int(length, Prefix.UINT32)

    def pack_array(self, value):
        self.pack_array_header(len(value))
        for item in value:
            self.pack(item)

    def pack_array_header(self, length):
        if length < (1 << 4):
            self.write_byte(Prefix.FIXARRAY_PREFIX | length)
        elif length < (1 << 16):
            self.write_byte(Prefix.ARRAY16)
            self.write_short(length, Prefix.UINT16)
        else:
            self.write_byte(Prefix.ARRAY32)
            self.write_int(length, Prefix.UINT32)

    def pack_map(self, value):
        self.pack_map_header(len(value))
        for value, key in value.iteritems():
            self.pack(key)
            self.pack(value)

    def pack_map_header(self, length):
        if length < (1 << 4):
            self.write_byte(Prefix.FIXMAP_PREFIX | length)
        elif length < (1 << 16):
            self.write_byte(Prefix.MAP16)
            self.write_short(length, Prefix.UINT16)
        else:
            self.write_byte(Prefix.MAP32)
            self.write_int(length, Prefix.UINT32)

    def pack_binary(self, value):
        self.pack_binary_header(len(value))
        self.write_payload(value)

    def pack_binary_header(self, length):
        if length < (1 << 8):
            self.write_byte(Prefix.BIN8)
            self.write_byte(length)
        elif length < (1 << 16):
            self.write_byte(Prefix.BIN16)
            self.write_short(length, Prefix.UINT16)
        else:
            self.write_byte(Prefix.BIN32)
            self.write_int(length, Prefix.UINT32)
