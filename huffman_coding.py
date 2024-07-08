# huffman_coding.py

import heapq
from collections import Counter
import bitarray


class HuffmanCoding:
    def __init__(self):
        self._encoding = {}
        self._decoding = {}

    def build_tree(self, text):
        freq = Counter(text)
        heap = [[weight, [char, ""]] for char, weight in freq.items()]
        heapq.heapify(heap)

        while len(heap) > 1:
            lo = heapq.heappop(heap)
            hi = heapq.heappop(heap)
            for pair in lo[1:]:
                pair[1] = '0' + pair[1]
            for pair in hi[1:]:
                pair[1] = '1' + pair[1]
            heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])

        encoding = dict(heapq.heappop(heap)[1:])
        decoding = {v: k for k, v in encoding.items()}
        self._encoding = encoding
        self._decoding = decoding

    def compress(self, text):
        encoded_text = ''.join(self._encoding[char] for char in text)
        bits = bitarray.bitarray(encoded_text)
        return bits.tobytes()

    def decompress(self, compressed_bytes):
        bits = bitarray.bitarray()
        bits.frombytes(compressed_bytes)
        encoded_text = bits.to01()
        decoded_text = ''
        current_code = ''

        for bit in encoded_text:
            current_code += bit
            if current_code in self._decoding:
                decoded_text += self._decoding[current_code]
                current_code = ''

        return decoded_text
