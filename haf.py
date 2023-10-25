import heapq
from collections import defaultdict, Counter


class HuffmanCoding:
    def __init__(self, text):
        self.text = text
        self.frequency = Counter(text)

    class Node:
        def __init__(self, frequency, char=None):
            self.char = char
            self.frequency = frequency
            self.left = None
            self.right = None

        def __lt__(self, other):
            return self.frequency < other.frequency

    def build_tree(self):
        heap = [self.Node(frequency, char) for char, frequency in self.frequency.items()]
        heapq.heapify(heap)
        while len(heap) > 1:
            node1 = heapq.heappop(heap)
            node2 = heapq.heappop(heap)
            merged = self.Node(node1.frequency + node2.frequency)
            merged.left = node1
            merged.right = node2
            heapq.heappush(heap, merged)
        return heapq.heappop(heap)

    def build_codes(self, node, current_code, codes):
        if node.char:
            codes[node.char] = current_code
            return
        self.build_codes(node.left, current_code + "0", codes)
        self.build_codes(node.right, current_code + "1", codes)

    def compress(self):
        codes = {}
        root = self.build_tree()
        self.build_codes(root, "", codes)
        encoded_text = ''.join([codes[char] for char in self.text])
        return encoded_text, codes

    def decompress(self, encoded_text, codes):
        decoded_text = ""
        reverse_mapping = {v: k for k, v in codes.items()}
        current_code = ""
        for bit in encoded_text:
            current_code += bit
            if current_code in reverse_mapping:
                character = reverse_mapping[current_code]
                decoded_text += character
                current_code = ""
        return decoded_text


if __name__ == '__main__':
    # Чтение текста из файла
    with open('input.txt', 'r') as file:
        text = file.read().replace('\n', '')

    # Инициализация объекта HuffmanCoding
    huffman_coding = HuffmanCoding(text)

    # Сжатие текста
    encoded_text, codes = huffman_coding.compress()
    print(f"Encoded Text: {encoded_text}")

    # Распаковка текста
    decoded_text = huffman_coding.decompress(encoded_text, codes)
    print(f"Decoded Text: {decoded_text}")

    # Проверка на идентичность исходного и распакованного текста
    if text == decoded_text:
        print("Тест пройден. Исходный текст и распакованный текст идентичны.")
    else:
        print("Тест не пройден. Исходный текст и распакованный текст различны.")

    # Оценка степени сжатия
    original_size = len(text)
    compressed_size = len(encoded_text)
    compression_ratio = compressed_size / original_size
    print(f"Степень сжатия: {compression_ratio}")
