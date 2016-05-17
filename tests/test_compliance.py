import json
import logging
import os

import pytest

from msgpack import Packer, Unpacker

test_segment = None

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


def gen_compliance_suite():
    segments = []
    for suite in compliance['suites']:
        for segment in compliance['suites'][suite]['segments']:
            global test_segment
            test_segment = dict(b64=segment['b64'], suffix=segment['method_suffix'])
            segments.append(':'.join((suite, segment['name'])))
    return segments


@pytest.mark.parametrize('key', gen_compliance_suite())
def test_basic_segment(key):
    method_suffix = test_segment['suffix']
    read_bytes = test_segment['b64'].decode('base64', 'strict')
    unpacker = Unpacker(read_bytes)
    read_value = getattr(unpacker, 'unpack' + method_suffix)()
    logging.debug('[%s] read %s', key, read_value)
    packer = Packer()
    if read_value is None:
        getattr(packer, 'pack' + method_suffix)()
    else:
        getattr(packer, 'pack' + method_suffix)(read_value)

    write_bytes = packer.get_bytes()
    out_b64 = write_bytes.encode('base64', 'strict').replace('\n', '')

    if out_b64 != test_segment['b64']:
        compare_bytes(convert_bytes(write_bytes), convert_bytes(read_bytes))

    assert out_b64 == test_segment['b64']
