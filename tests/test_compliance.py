import json
import logging
import os

from sure import expect

from msgpack import Packer, Unpacker

with open(os.path.join(os.path.dirname(__file__)) + "/compliance.json", 'r') as f:
    compliance = json.loads(f.read())


def compare_bytes(act, exp):
    print act
    print exp
    print 'idx', 'exp', 'act'
    print '---', '---', '---'
    for i, ne in enumerate((x != y for x, y in zip(exp, act))):
        print '%03d' % i, '%03d' % exp[i], '%03d' % act[i] if i in range(0, len(act)) else '-', 'X' if ne else ''


def convert_bytes(in_bytes):
    out_bytes = []
    for b in in_bytes:
        out_bytes.append(int(hex(ord(b)), 16))
    return out_bytes


def test_compliance():
    for suite in compliance['suites']:
        for segment in compliance['suites'][suite]['segments']:
            global test_segment
            test_segment = {
                'base64': segment['b64']
            }
            yield check_basic_segment, ':'.join((suite, segment['name']))


def check_basic_segment(key):
    read_bytes = test_segment['base64'].decode('base64', 'strict')
    read_value = Unpacker(read_bytes).unpack()
    logging.debug('read %s', read_value)
    packer = Packer()
    packer.pack(read_value)
    write_bytes = packer.get_bytes()
    out_b64 = write_bytes.encode('base64', 'strict').replace('\n', '')

    if out_b64 != test_segment['base64']:
        compare_bytes(convert_bytes(write_bytes), convert_bytes(read_bytes))

    expect(out_b64).to.equal(test_segment['base64'])
