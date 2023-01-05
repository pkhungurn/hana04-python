from io import BufferedIOBase

from msgpack import Packer


class MessagePacker:
    def __init__(self, out: BufferedIOBase):
        self.out = out
        self.packer = Packer()
        self.single_float_packer = Packer(use_single_float=True)

    def pack_str(self, value: str):
        self.out.write(self.packer.pack(value))

    def pack_bool(self, value: bool):
        self.out.write(self.packer.pack(value))

    def pack_int(self, value: int):
        self.out.write(self.packer.pack(value))

    def pack_single_float(self, value: float):
        self.out.write(self.single_float_packer.pack(value))

    def pack_double_float(self, value: float):
        self.out.write(self.packer.pack(value))

    def pack_array_header(self, n: int):
        self.out.write(self.packer.pack_array_header(n))

    def pack_map_header(self, n: int):
        self.out.write(self.packer.pack_map_header(n))

    def pack_bytes(self, value: bytes):
        self.out.write(self.packer.pack(value))