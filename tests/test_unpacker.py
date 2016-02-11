from sure import expect
from msgpack import Unpacker, Prefix


def test_read_byte():
    unpacker = Unpacker(bytearray([Prefix.BIN32]))
    expect(unpacker.read_byte()).to.equal(Prefix.BIN32)


def test_read_max_short():
    unpacker = Unpacker(bytearray([Prefix.UINT16, 255, 255]))
    expect(unpacker.read_short()).to.equal(0xFFFF)


def test_read_int():
    unpacker = Unpacker(bytearray([Prefix.UINT32, 255, 255, 255, 255]))
    expect(unpacker.read_int()).to.equal(0xFFFFFFFF)


def test_read_short_and_int():
    unpacker = Unpacker(bytearray([Prefix.UINT16, 255, 255, Prefix.UINT32, 255, 255, 255, 255]))
    expect(unpacker.read_short()).to.equal(0xFFFF)
    expect(unpacker.read_int()).to.equal(0xFFFFFFFF)


def test_read_short_int_compact():
    unpacker = Unpacker(bytearray([255, 255, 255, 255, 255, 255]))
    expect(unpacker.read_short(Prefix.UINT16)).to.equal(0xFFFF)
    expect(unpacker.read_int(Prefix.UINT32)).to.equal(0xFFFFFFFF)


def test_peek():
    unpacker = Unpacker(bytearray([Prefix.UINT16, 255, 255]))
    expect(unpacker.buf.tell()).to.equal(0)
    expect(unpacker.peek()).to.equal(Prefix.UINT16)
    expect(unpacker.buf.tell()).to.equal(0)


def test_unpack_short_and_int():
    unpacker = Unpacker(bytearray([Prefix.UINT16, 255, 255, Prefix.UINT32, 255, 255, 255, 255]))
    expect(unpacker.unpack_int()).to.equal(0xFFFF)
    expect(unpacker.unpack_int()).to.equal(0xFFFFFFFF)


def test_unpack_string():
    expected = [Prefix.FIXSTR_PREFIX | len('foo'), 102, 111, 111]
    unpacker = Unpacker(bytearray(expected))
    actual = unpacker.unpack_string()
    expect(actual).to.equal('foo')
