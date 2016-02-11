import struct
from collections import OrderedDict
from io import BufferedReader, BytesIO

from .prefix import Prefix


class Unpacker:
    def __init__(self, initial_bytes=None):
        self.initial_bytes = initial_bytes
        self.buf = BufferedReader(raw=BytesIO(initial_bytes))

    def struct_unpack(self, fmt):
        return struct.unpack(fmt, self.buf.read(struct.calcsize(fmt)))

    def read_byte(self):
        return self.struct_unpack('B')[0]

    def read_signed_byte(self):
        return self.struct_unpack('b')[0]

    def read_short(self, prefix=None):
        if prefix is None:
            prefix = self.read_byte()
        assert prefix in [Prefix.INT16, Prefix.UINT16], 'read_short expects prefix %s or %s but read %s' % (
            Prefix.INT16, Prefix.UINT16, prefix)
        return self.struct_unpack('>H' if prefix == Prefix.UINT16 else '>h')[0]

    def read_int(self, prefix=None):
        if prefix is None:
            prefix = self.read_byte()
        assert prefix in [Prefix.INT32, Prefix.UINT32], 'read_int expects prefix %s or %s but read %s' % (
            Prefix.INT32, Prefix.UINT32, prefix)
        return self.struct_unpack('>I' if prefix == Prefix.UINT32 else '>i')[0]

    def read_long(self, prefix=None):
        if prefix is None:
            prefix = self.read_byte()
        assert prefix in [Prefix.INT64, Prefix.UINT64], 'read_long expects prefix %s or %s but read %s' % (
            Prefix.INT64, Prefix.UINT64, prefix)
        return self.struct_unpack('>Q' if prefix == Prefix.UINT64 else '>q')[0]

    def read_float(self, prefix=None):
        if prefix is None:
            prefix = self.read_byte()
        assert prefix == Prefix.FLOAT32, 'read_float expects prefix %s but read %s' % (Prefix.FLOAT32, prefix)
        return self.struct_unpack('>f')[0]

    def read_double(self, prefix=None):
        if prefix is None:
            prefix = self.read_byte()
        assert prefix == Prefix.FLOAT64, 'read_double expects prefix %s but read %s' % (Prefix.FLOAT64, prefix)
        return self.struct_unpack('>d')[0]

    def read_payload(self, length):
        return self.buf.read(length)

    def peek(self):
        return struct.unpack('B', self.buf.peek()[0])[0]

    def unpack_nil(self):
        assert self.read_byte() == Prefix.NIL, 'unpack_nil expects to read %s' % Prefix.NIL

    def unpack_boolean(self):
        prefix = self.read_byte()
        assert prefix in [Prefix.TRUE, Prefix.FALSE], 'unpack_boolean expects prefix %s or %s but read %s' % (
            Prefix.TRUE, Prefix.FALSE, prefix)
        return prefix == Prefix.TRUE

    def unpack_int(self):
        prefix = self.peek()

        if Prefix.is_fix_int(prefix):
            return self.read_byte() if Prefix.is_pos_fix_int(prefix) else self.read_signed_byte()

        if prefix == Prefix.INT8:
            self.read_byte()
            return self.read_signed_byte()
        elif prefix == Prefix.UINT8:
            self.read_byte()
            return self.read_byte()
        elif prefix in [Prefix.UINT16, Prefix.INT16]:
            return self.read_short()
        elif prefix in [Prefix.UINT32, Prefix.INT32]:
            return self.read_int()
        elif prefix in [Prefix.UINT64, Prefix.INT64]:
            return self.read_long()
        else:
            raise ValueError('unexpected int prefix %s' % prefix)

    def unpack_float(self):
        return self.read_float()

    def unpack_double(self):
        return self.read_double()

    def unpack(self):
        prefix = self.peek()

        if Prefix.is_fix_int(prefix) or prefix in [Prefix.INT8, Prefix.UINT8, Prefix.INT16, Prefix.UINT16, Prefix.INT32,
                                                   Prefix.UINT32, Prefix.INT64, Prefix.UINT64]:
            return self.unpack_int()
        elif Prefix.is_fixed_array(prefix) or prefix in [Prefix.ARRAY16, Prefix.ARRAY32]:
            return self.unpack_array()
        elif Prefix.is_fixed_map(prefix) or prefix in [Prefix.MAP16, Prefix.MAP32]:
            return self.unpack_map()
        elif Prefix.is_fix_str(prefix) or prefix in [Prefix.STR8, Prefix.STR16, Prefix.STR32]:
            return self.unpack_string()
        elif prefix in [Prefix.TRUE, Prefix.FALSE]:
            return self.unpack_boolean()
        elif prefix == Prefix.NIL:
            return self.unpack_nil()
        elif prefix == Prefix.FLOAT32:
            return self.unpack_float()
        elif prefix == Prefix.FLOAT64:
            return self.unpack_double()
        elif prefix in [Prefix.BIN8, Prefix.BIN16, Prefix.BIN32]:
            return self.unpack_binary()
        else:
            raise ValueError('unknown prefix %s' % prefix)

    def unpack_string(self):
        return str(bytearray(self.read_payload(self.unpack_raw_string_header())))

    def unpack_raw_string_header(self):
        prefix = self.read_byte()

        if Prefix.is_fixed_raw(prefix):
            return prefix & 0x1f
        elif prefix == Prefix.STR8:
            return self.read_byte()
        elif prefix == Prefix.STR16:
            return self.read_short(Prefix.UINT16)
        elif prefix == Prefix.STR32:
            return self.read_int(Prefix.UINT32)
        else:
            raise ValueError('unexpected raw string header prefix %s' % prefix)

    def unpack_array(self):
        size = self.unpack_array_header()
        array = []

        for i in range(0, size):
            array.append(self.unpack())

        return array

    def unpack_array_header(self):
        prefix = self.read_byte()

        if Prefix.is_fixed_array(prefix):
            return prefix & 0x0f
        elif prefix == Prefix.ARRAY16:
            return self.read_short(Prefix.UINT16)
        elif prefix == Prefix.ARRAY32:
            return self.read_int(Prefix.UINT32)
        else:
            raise ValueError('unexpected array header prefix %s' % prefix)

    def unpack_map(self):
        size = self.unpack_map_header()
        map = OrderedDict()

        for i in range(0, size):
            map[self.unpack()] = self.unpack()

        return map

    def unpack_map_header(self):
        prefix = self.read_byte()

        if Prefix.is_fixed_map(prefix):
            return prefix & 0x1f
        elif prefix == Prefix.MAP16:
            return self.read_short(Prefix.UINT16)
        elif prefix == Prefix.MAP32:
            return self.read_int(Prefix.UINT32)
        else:
            raise ValueError('unexpected map header prefix %s' % prefix)

    def unpack_binary(self):
        return self.read_payload(self.unpack_binary_header())

    def unpack_binary_header(self):
        prefix = self.read_byte()

        if prefix == Prefix.BIN8:
            return self.read_byte()
        elif prefix == Prefix.BIN16:
            return self.read_short(Prefix.UINT16)
        elif prefix == Prefix.BIN32:
            return self.read_int(Prefix.UINT32)
        else:
            raise ValueError('unexpected binary header prefix %s' % prefix)
