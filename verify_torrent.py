import libtorrent as lt
import os
import sys
from hashlib import sha1

def verify_torrent(torrent_file, download_dir=None):
    info = lt.torrent_info(torrent_file)
    
    # Use provided download_dir or default to the directory of the torrent file
    save_path = download_dir if download_dir else os.path.dirname(torrent_file)

    for piece_index in range(info.num_pieces()):
        piece_data = b''
        piece_length = info.piece_length()

        for file_entry in info.files():
            file_offset = file_entry.offset
            file_path = os.path.join(save_path, file_entry.path)
            
            if not os.path.exists(file_path):
                print(f"File not found: {file_path}")
                continue

            with open(file_path, 'rb') as f:
                start_in_file = max(0, piece_index * piece_length - file_offset)
                end_in_file = min(file_entry.size, (piece_index + 1) * piece_length - file_offset)
                
                if start_in_file < end_in_file:  # The file contributes to this piece
                    f.seek(start_in_file)
                    piece_data += f.read(end_in_file - start_in_file)
            
            if len(piece_data) >= piece_length:
                break

        # Piece verification logic
        if piece_index == info.num_pieces() - 1:
            actual_piece_length = min(len(piece_data), piece_length)
            computed_hash = sha1(piece_data[:actual_piece_length]).digest()
        else:
            if len(piece_data) < piece_length:
                piece_data += b'\0' * (piece_length - len(piece_data))
            computed_hash = sha1(piece_data).digest()
        
        expected_hash = info.hash_for_piece(piece_index)
        
        if computed_hash == expected_hash:
            print(f"Piece {piece_index} verified successfully.")
        else:
            print(f"Piece {piece_index} verification failed.")
            print(f"  Expected: {expected_hash.hex()}")
            print(f"  Got: {computed_hash.hex()}")
            print(f"  Data sample: {piece_data[:16].hex() if piece_data else 'No data'}")
            print(f"  Piece Length: {piece_length}")
            print(f"  Data Read: {len(piece_data)} bytes")
            if piece_index == info.num_pieces() - 1:
                print(f"  Actual Piece Length: {actual_piece_length}")
                print(f"  Last byte sample: {piece_data[-16:].hex() if piece_data else 'No data'}")

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
        print("Usage: python3 verify_torrent.py <torrent_file> [<download_directory>]")
        sys.exit(0)

    torrent_file = sys.argv[1]
    download_dir = sys.argv[2] if len(sys.argv) > 2 else None
    verify_torrent(torrent_file, download_dir)

if __name__ == "__main__":
    main()
