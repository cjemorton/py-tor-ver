import libtorrent as lt
import os
import sys
from hashlib import sha1

def verify_torrent(torrent_file):
    info = lt.torrent_info(torrent_file)
    session = lt.session()
    save_path = os.path.dirname(torrent_file)

    for file in info.files():
        print(f"Verifying file: {file.path}")
        file_path = os.path.join(save_path, file.path)
        
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            continue

        with open(file_path, 'rb') as f:
            file_data = f.read()
            file_size = len(file_data)
            piece_length = info.piece_length()

            for piece_index in range(info.num_pieces()):
                start_byte = piece_index * piece_length
                end_byte = min(start_byte + piece_length, file_size)
                
                # Ensure we don't read beyond the file size
                piece_data = file_data[start_byte:end_byte]
                
                computed_hash = sha1(piece_data).digest()
                expected_hash = info.hash_for_piece(piece_index)
                
                if computed_hash == expected_hash:
                    print(f"Piece {piece_index} verified successfully.")
                else:
                    print(f"Piece {piece_index} verification failed.")
                    print(f"  Expected: {expected_hash.hex()}")
                    print(f"  Got: {computed_hash.hex()}")
                    # Dump the first few bytes of data for debugging
                    print(f"  Data sample: {piece_data[:16].hex()}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 verify_torrent.py <torrent_file>")
        sys.exit(1)

    torrent_file = sys.argv[1]
    verify_torrent(torrent_file)
