from sure import expect
from msgpack import Packer, Unpacker, Prefix
from collections import OrderedDict


def test_pack_nil():
    packer = Packer()
    packer.pack_nil()
    unpacker = Unpacker(bytearray(packer.get_bytes()))
    expect(unpacker.unpack()).to.equal(None)


def test_min_short():
    packer = Packer()
    packer.pack_int(-0x8000)
    unpacker = Unpacker(bytearray(packer.get_bytes()))
    expect(unpacker.unpack()).to.equal(-0x8000)


def test_max_short():
    packer = Packer()
    packer.pack_int(0xFFFF)
    unpacker = Unpacker(bytearray(packer.get_bytes()))
    expect(unpacker.unpack()).to.equal(0xFFFF)


def test_string():
    packer = Packer()
    packer.pack_string('foo')
    unpacker = Unpacker(bytearray(packer.get_bytes()))
    expect(unpacker.unpack()).to.equal('foo')


def test_map():
    expected = OrderedDict([('foo', 1), ('bar', 2)])
    packer = Packer()
    packer.pack_map(expected)
    unpacker = Unpacker(bytearray(packer.get_bytes()))
    actual = unpacker.unpack()
    expect(actual['foo']).to.equal(expected['foo'])
