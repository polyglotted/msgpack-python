import json
import os
from collections import OrderedDict

from msgpack import Packer


def generate():
    compliance = OrderedDict([('name', 'msgpack compliance test'), ('version', '1.0.0'), ('suites', OrderedDict())])

    compliance['suites']['INTEGER'] = OrderedDict(segments=[
        gen_segment('fixnum min', 'pack_int', -0x20),
        gen_segment('fixnum max', 'pack_int', 0x7F),
        gen_segment('byte min', 'pack_int', -0x80),
        gen_segment('byte max', 'pack_int', 0xFF),
        gen_segment('short min', 'pack_int', -0x8000),
        gen_segment('short max', 'pack_int', 0xFFFF),
        gen_segment('int min', 'pack_int', -0x80000000),
        gen_segment('int max', 'pack_int', 0xFFFFFFFF),
        gen_segment('long min', 'pack_int', -0x8000000000000000),
        gen_segment('long max', 'pack_int', 0xfffffffffffff000)
    ])

    compliance['suites']['NIL'] = OrderedDict(segments=[
        gen_segment('nil', 'pack_nil', None)
    ])

    compliance['suites']['BOOLEAN'] = OrderedDict(segments=[
        gen_segment('bool true', 'pack_boolean', True),
        gen_segment('bool false', 'pack_boolean', False)
    ])

    compliance['suites']['FLOAT'] = OrderedDict(segments=[
        gen_segment('float32 min', 'pack_float', 1.4e-45),
        gen_segment('float32 max', 'pack_float', 3.4028234663852886e+38),
        # gen_segment('float64 min', 'pack_double', 4.9e-324),
        gen_segment('float64 max', 'pack_double', 1.7976931348623157e+308)
    ])

    out = json.dumps(compliance, indent=2, separators=(',', ': '))

    with open(os.path.join(os.path.dirname(__file__)) + "/compliance.json", 'w') as f:
        f.write(out)


def gen_segment(name, method, arg=None, append_arg_to_name=True):
    packer = Packer()
    if arg is None:
        getattr(packer, method)()
    else:
        getattr(packer, method)(arg)

    if append_arg_to_name:
        name = name + ' (' + str(arg) + ')'
    return OrderedDict([('name', name), ('b64', packer.get_bytes().encode('base64', 'strict').replace('\n', ''))])


if __name__ == '__main__':
    generate()
