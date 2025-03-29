from src.advent_of_code.year_2021.day_16 import process


def test_packet_decoder_literal_packet():
    message = 'D2FE28'
    decoder = process.PacketDecoder.from_hex(message)
    assert decoder.decode() == process.LiteralPacket(version=6, id_=4, val=2021)


def test_packet_decoder_operator_packet_total_bit_length():
    message = '38006F45291200'
    decoder = process.PacketDecoder.from_hex(message)
    assert decoder.decode() == process.OperatorPacket(
        version=1,
        id_=6,
        subpackets=[
            process.LiteralPacket(version=6, id_=4, val=10),
            process.LiteralPacket(version=2, id_=4, val=20),
        ]
    )


def test_packet_decoder_operator_packet_subpacket_no():
    message = 'EE00D40C823060'
    decoder = process.PacketDecoder.from_hex(message)
    assert decoder.decode() == process.OperatorPacket(
        version=7,
        id_=3,
        subpackets=[
            process.LiteralPacket(version=2, id_=4, val=1),
            process.LiteralPacket(version=4, id_=4, val=2),
            process.LiteralPacket(version=1, id_=4, val=3),
        ]
    )


def test_packet_decoder_complex_example_1():
    message = '8A004A801A8002F478'
    decoder = process.PacketDecoder.from_hex(message)
    result = decoder.decode()
    assert result == process.OperatorPacket(
        version=4,
        id_=2,
        subpackets=[
            process.OperatorPacket(
                version=1,
                id_=2,
                subpackets=[
                    process.OperatorPacket(
                        version=5,
                        id_=2,
                        subpackets=[process.LiteralPacket(version=6, id_=4, val=15)]
                    ),
                ]
            ),
        ]
    )
    assert result.version_sum == 16


def test_packet_decoder_complex_example_2():
    message = '620080001611562C8802118E34'
    decoder = process.PacketDecoder.from_hex(message)
    result = decoder.decode()
    assert result == process.OperatorPacket(
        version=3,
        id_=0,
        subpackets=[
            process.OperatorPacket(
                version=0,
                id_=0,
                subpackets=[
                    process.LiteralPacket(version=0, id_=4, val=10),
                    process.LiteralPacket(version=5, id_=4, val=11),
                ]
            ),
            process.OperatorPacket(
                version=1,
                id_=0,
                subpackets=[
                    process.LiteralPacket(version=0, id_=4, val=12),
                    process.LiteralPacket(version=3, id_=4, val=13)
                ]
            ),
        ]
    )

    assert result.version_sum == 12


def test_packet_decoder_complex_example_3():
    message = 'C0015000016115A2E0802F182340'
    decoder = process.PacketDecoder.from_hex(message)
    result = decoder.decode()
    assert result == process.OperatorPacket(
        version=6,
        id_=0,
        subpackets=[
            process.OperatorPacket(
                version=0,
                id_=0,
                subpackets=[
                    process.LiteralPacket(version=0, id_=4, val=10),
                    process.LiteralPacket(version=6, id_=4, val=11)
                ]
            ),
            process.OperatorPacket(
                version=4,
                id_=0,
                subpackets=[
                    process.LiteralPacket(version=7, id_=4, val=12),
                    process.LiteralPacket(version=0, id_=4, val=13)
                ]
            ),
        ]
    )

    assert result.version_sum == 23


def test_packet_decoder_complex_example_4():
    message = 'A0016C880162017C3686B18A3D4780'
    decoder = process.PacketDecoder.from_hex(message)
    result = decoder.decode()
    assert result == process.OperatorPacket(
        version=5,
        id_=0,
        subpackets=[
            process.OperatorPacket(
                version=1,
                id_=0,
                subpackets=[
                    process.OperatorPacket(
                        version=3,
                        id_=0,
                        subpackets=[
                            process.LiteralPacket(version=7, id_=4, val=6),
                            process.LiteralPacket(version=6, id_=4, val=6),
                            process.LiteralPacket(version=5, id_=4, val=12),
                            process.LiteralPacket(version=2, id_=4, val=15),
                            process.LiteralPacket(version=2, id_=4, val=15),
                        ]
                    )
                ]
            )
        ]
    )

    assert result.version_sum == 31


def test_packet_decoder_complex_example_5():
    message = 'C200B40A82'
    decoder = process.PacketDecoder.from_hex(message)
    result = decoder.decode()
    assert result.val == 3


def test_packet_decoder_complex_example_6():
    message = '04005AC33890'
    decoder = process.PacketDecoder.from_hex(message)
    result = decoder.decode()
    assert result.val == 54


def test_packet_decoder_complex_example_7():
    message = '880086C3E88112'
    decoder = process.PacketDecoder.from_hex(message)
    result = decoder.decode()
    assert result.val == 7


def test_packet_decoder_complex_example_8():
    message = 'CE00C43D881120'
    decoder = process.PacketDecoder.from_hex(message)
    result = decoder.decode()
    assert result.val == 9


def test_packet_decoder_complex_example_9():
    message = 'D8005AC2A8F0'
    decoder = process.PacketDecoder.from_hex(message)
    result = decoder.decode()
    assert result.val == 1


def test_packet_decoder_complex_example_10():
    message = 'F600BC2D8F'
    decoder = process.PacketDecoder.from_hex(message)
    result = decoder.decode()
    assert result.val == 0


def test_packet_decoder_complex_example_11():
    message = '9C005AC2F8F0'
    decoder = process.PacketDecoder.from_hex(message)
    result = decoder.decode()
    assert result.val == 0


def test_packet_decoder_complex_example_12():
    message = '9C0141080250320F1802104A08'
    decoder = process.PacketDecoder.from_hex(message)
    result = decoder.decode()
    assert result.val == 1
