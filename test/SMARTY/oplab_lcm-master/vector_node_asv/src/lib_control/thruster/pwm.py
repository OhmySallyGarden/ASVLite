"""LCM type definitions
This file automatically generated by lcm.
DO NOT MODIFY BY HAND!!!!
"""

try:
    import cStringIO.StringIO as BytesIO
except ImportError:
    from io import BytesIO
import struct

class pwm(object):
    __slots__ = ["timestamp", "number", "label", "thrust_command", "pwm_command", "pwm_string"]

    def __init__(self):
        self.timestamp = 0.0
        self.number = 0
        self.label = []
        self.thrust_command = []
        self.pwm_command = []
        self.pwm_string = ""

    def encode(self):
        buf = BytesIO()
        buf.write(pwm._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        buf.write(struct.pack(">db", self.timestamp, self.number))
        for i0 in range(self.number):
            __label_encoded = self.label[i0].encode('utf-8')
            buf.write(struct.pack('>I', len(__label_encoded)+1))
            buf.write(__label_encoded)
            buf.write(b"\0")
        buf.write(struct.pack('>%dd' % self.number, *self.thrust_command[:self.number]))
        buf.write(struct.pack('>%dd' % self.number, *self.pwm_command[:self.number]))
        __pwm_string_encoded = self.pwm_string.encode('utf-8')
        buf.write(struct.pack('>I', len(__pwm_string_encoded)+1))
        buf.write(__pwm_string_encoded)
        buf.write(b"\0")

    def decode(data):
        if hasattr(data, 'read'):
            buf = data
        else:
            buf = BytesIO(data)
        if buf.read(8) != pwm._get_packed_fingerprint():
            raise ValueError("Decode error")
        return pwm._decode_one(buf)
    decode = staticmethod(decode)

    def _decode_one(buf):
        self = pwm()
        self.timestamp, self.number = struct.unpack(">db", buf.read(9))
        self.label = []
        for i0 in range(self.number):
            __label_len = struct.unpack('>I', buf.read(4))[0]
            self.label.append(buf.read(__label_len)[:-1].decode('utf-8', 'replace'))
        self.thrust_command = struct.unpack('>%dd' % self.number, buf.read(self.number * 8))
        self.pwm_command = struct.unpack('>%dd' % self.number, buf.read(self.number * 8))
        __pwm_string_len = struct.unpack('>I', buf.read(4))[0]
        self.pwm_string = buf.read(__pwm_string_len)[:-1].decode('utf-8', 'replace')
        return self
    _decode_one = staticmethod(_decode_one)

    _hash = None
    def _get_hash_recursive(parents):
        if pwm in parents: return 0
        tmphash = (0xa819b97b522e91c9) & 0xffffffffffffffff
        tmphash  = (((tmphash<<1)&0xffffffffffffffff)  + (tmphash>>63)) & 0xffffffffffffffff
        return tmphash
    _get_hash_recursive = staticmethod(_get_hash_recursive)
    _packed_fingerprint = None

    def _get_packed_fingerprint():
        if pwm._packed_fingerprint is None:
            pwm._packed_fingerprint = struct.pack(">Q", pwm._get_hash_recursive([]))
        return pwm._packed_fingerprint
    _get_packed_fingerprint = staticmethod(_get_packed_fingerprint)

