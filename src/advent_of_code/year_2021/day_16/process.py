import collections
import dataclasses
import itertools
import math
import operator


@dataclasses.dataclass
class Packet:
    version: int
    id_: int

    @property
    def version_sum(self):
        raise NotImplementedError

    @property
    def val(self):
        raise NotImplementedError

    @val.setter
    def val(self, value):
        raise NotImplementedError



@dataclasses.dataclass
class LiteralPacket(Packet):
    val: int
    _val: int = dataclasses.field(init=False, repr=False)

    @property
    def version_sum(self):
        return self.version

    @property
    def val(self):
        return self._val

    @val.setter
    def val(self, value):
        self._val = value


@dataclasses.dataclass
class OperatorPacket(Packet):
    subpackets: list

    @staticmethod
    def gt(args):
        return operator.gt(*args)

    @staticmethod
    def lt(args):
        return operator.lt(*args)

    @staticmethod
    def eq(args):
        return operator.eq(*args)

    @property
    def VAL_FNS(self):
        return {
            0: sum,
            1: math.prod,
            2: min,
            3: max,
            5: self.gt,
            6: self.lt,
            7: self.eq,
        }

    @property
    def version_sum(self):
        return self.version + sum(packet.version_sum for packet in self.subpackets)

    @property
    def val(self):
        return int(self.VAL_FNS[self.id_](packet.val for packet in self.subpackets))

    @val.setter
    def val(self, value):
        raise NotImplementedError



class PacketDecoder:

    def __init__(self, message):
        self.og_message = message
        self.message = collections.deque(self.og_message)

    @classmethod
    def from_hex(cls, message):
        bin_message = str(bin(int(message, 16))[2:]).zfill(len(message) * 4)
        return cls(bin_message)

    @classmethod
    def read_file(cls):
        with open('input.txt') as f:
            return cls.from_hex(f.read().strip())

    def _get_raw_bits(self, num):
        result = []
        for _ in range(num):
            try:
                result.append(self.message.popleft())
            except IndexError:
                break   # try and return as many bits as possible`
        return ''.join(result) if result else '0'       # if no bits, then return 0

    @staticmethod
    def _decimalise_raw_bits(result):
        return int(result, base=2)

    def _get_bits(self, num):
        raw_bits = self._get_raw_bits(num)
        return self._decimalise_raw_bits(raw_bits)

    def _decode_literal(self):
        lit_list = []
        while True:
            prefix = self._get_bits(1)
            bits = self._get_raw_bits(4)
            lit_list.append(bits)
            if not prefix:
                break
        lit_bits = ''.join(lit_list)
        literal = self._decimalise_raw_bits(lit_bits)
        return literal

    def decode(self, subpacket=False, run_no=None):
        packets = []

        for num in itertools.count():
            if not self.message:
                break
            version = self._get_bits(3)
            packet_id = self._get_bits(3)
            if packet_id == 4:    # literal packet
                literal = self._decode_literal()
                packets.append(LiteralPacket(version, packet_id, val=literal))
            else:   # operator packet
                length_type_id = self._get_bits(1)
                if length_type_id == 0:
                    bit_length = self._get_bits(15)
                    subpacket_decoder = PacketDecoder(self._get_raw_bits(bit_length))
                    subpackets = subpacket_decoder.decode(subpacket=True)
                elif length_type_id == 1:
                    bit_length = self._get_bits(11)
                    subpackets = self.decode(subpacket=True, run_no=bit_length)
                else:
                    raise Exception('Invalid packet')
                packets.append(OperatorPacket(version, packet_id, subpackets))
            if not subpacket:
                break
            if run_no and num == run_no - 1:
                break

        if not subpacket:
            packet, = packets
            return packet
        else:
            return packets


def main():
    packet_decoder = PacketDecoder.read_file()
    packet = packet_decoder.decode()
    print('Packet Version Sum:', packet.version_sum)
    print('Packet Val:', packet.val)


if __name__ == '__main__':
    import timeit
    print(timeit.timeit(main, number=1))
