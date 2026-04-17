import heapq
from collections import defaultdict
import os

class Node:
    def __init__(self, char, freq, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

class HuffmanCompressor:
    def __init__(self, min_size=1024, max_size=150*1024*1024):  # min 1KB, max 150MB
        self.codes = {}
        self.min_size = min_size
        self.max_size = max_size

    def _frequency_dict(self, text):
        return defaultdict(int, {ch: text.count(ch) for ch in set(text)})

    def _build_tree(self, freq):
        heap = [Node(ch, f) for ch, f in freq.items()]
        heapq.heapify(heap)
        while len(heap) > 1:
            n1, n2 = heapq.heappop(heap), heapq.heappop(heap)
            merged = Node(None, n1.freq + n2.freq, n1, n2)
            heapq.heappush(heap, merged)
        return heap[0]

    def _generate_codes(self, node, current=""):
        if node.char is not None:
            # handle single-character file
            self.codes[node.char] = current if current else "0"
        else:
            self._generate_codes(node.left, current + "0")
            self._generate_codes(node.right, current + "1")

    def _encode_text(self, text):
        return ''.join(self.codes[ch] for ch in text)

    def _pad_bits(self, bits):
        padding = 8 - len(bits) % 8
        return f"{padding:08b}" + bits + '0' * padding

    def _to_bytearray(self, bits):
        return bytearray(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))

    def compress(self, text):
        # empty input
        if not text or len(text) == 0:
            return b""  

        # check size limits
        text_len = len(text.encode() if isinstance(text, str) else text)
        if text_len < self.min_size:
            print(f"File too small ({text_len} bytes), skipping compression.")
            return text.encode() if isinstance(text, str) else text
        if text_len > self.max_size:
            print(f"File too large ({text_len} bytes), skipping compression.")
            return text.encode() if isinstance(text, str) else text

        # single-character file
        if len(set(text)) == 1:
            print("Single-character file detected, compressing efficiently.")
            char = text[0]
            count = len(text)
            # store char + count as 4-byte integer
            return char.encode() + count.to_bytes(4, 'big')

        freq = self._frequency_dict(text)
        root = self._build_tree(freq)
        self._generate_codes(root)
        encoded = self._encode_text(text)
        padded = self._pad_bits(encoded)
        return bytes(self._to_bytearray(padded))


    #Decompress method
    def decompress(self, compressed_bytes, codes):
        if not compressed_bytes:
            return ""

        # reverse the code dictionary: code -> character
        reverse_codes = {v: k for k, v in codes.items()}

        # convert bytes to full bit string
        bits = ''.join(f"{byte:08b}" for byte in compressed_bytes)

        # read padding length from first 8 bits
        padding = int(bits[:8], 2)
        bits = bits[8:]  # remaining bits

        # remove padding bits from end
        bits = bits[:-padding]

        # decode
        decoded_text = ""
        current = ""

        for bit in bits:
            current += bit
            if current in reverse_codes:
                decoded_text += reverse_codes[current]
                current = ""

        return decoded_text
