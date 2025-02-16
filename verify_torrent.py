import libtorrent as lt
import os
import sys
from hashlib import sha1

def verify_torrent(torrent_file):
    # Load the torrent file
    info = lt.torrent_info(torrent_file)
    
    # Create a session to access the torrent file's data
    session = lt.session()
    
    # Assuming files are in the same directory as the torrent file
    save_path = os.path.dirname(torrent_file)

    for file in info.files():
        print(f"Verifying file: {file.path}")
        file_path = os.path.join(save_path, file.path)
        
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            continue

        # Open the file for reading
        with open(file_path, 'rb') as f:
            # Loop through pieces
            for piece_index in range(info.num_pieces()):
                start_byte = piece_index * info.piece_length()
                end_byte = min(start_byte + info.piece_length(), file.size)
                
                # Read the piece from file
                f.seek(start_byte)
                piece_data = f.read(end_byte - start_byte)
                
                # Compute SHA-1 hash of the piece
                computed_hash = sha1(piece_data).digest()
                
                # Get expected hash from torrent info
                expected_hash = info.hash_for_piece(piece_index).to_bytes()
                
                if computed_hash == expected_hash:
                    print(f"Piece {piece_index} verified successfully.")
                else:
                    print(f"Piece {piece_index} verification failed. Expected: {expected_hash.hex()}, Got: {computed_hash.hex()}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 verify_torrent.py <torrent_file>")
        sys.exit(1)

    torrent_file = sys.argv[1]
    verify_torrent(torrent_file)
