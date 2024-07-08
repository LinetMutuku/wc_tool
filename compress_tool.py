# compress_tool.py

import argparse
from huffman_coding import HuffmanCoding


def compress_file(input_file, output_file):
    # Read input file
    with open(input_file, 'r') as f:
        original_text = f.read()

    # Initialize HuffmanCoding instance
    huffman = HuffmanCoding()
    huffman.build_tree(original_text)

    # Compress data
    compressed_data = huffman.compress(original_text)

    # Write compressed data to output file
    with open(output_file, 'wb') as f:
        f.write(compressed_data)

    print(f"Compression successful. Compressed file saved as '{output_file}'")


def decompress_file(input_file, output_file):
    # Read compressed file
    with open(input_file, 'rb') as f:
        compressed_data = f.read()

    # Initialize HuffmanCoding instance
    huffman = HuffmanCoding()

    # Decompress data
    decompressed_text = huffman.decompress(compressed_data)

    # Write decompressed data to output file
    with open(output_file, 'w') as f:
        f.write(decompressed_text)

    print(f"Decompression successful. Decompressed file saved as '{output_file}'")


def main():
    parser = argparse.ArgumentParser(description="Text Compression Tool using Huffman Coding")
    parser.add_argument('mode', choices=['compress', 'decompress'], help="Mode: compress or decompress")
    parser.add_argument('input_file', help="Input file path")
    parser.add_argument('output_file', help="Output file path")

    args = parser.parse_args()

    if args.mode == 'compress':
        compress_file(args.input_file, args.output_file)
    elif args.mode == 'decompress':
        decompress_file(args.input_file, args.output_file)


if __name__ == "__main__":
    main()
