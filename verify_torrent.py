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

    for piece_index in range(info.num_pieces()):
        piece_data = b''
        piece_length = info.piece_length()
        
        # Loop through each file in the torrent to collect data for the piece
        for file_index in range(info.num_files()):
            file_entry = info.file_at(file_index)
            file_offset = file_entry.offset
            file_path = os.path.join(save_path, file_entry.path)
            
            if not os.path.exists(file_path):
                print(f"File not found: {file_path}")
                continue

            with open(file_path, 'rb') as f:
                # Determine if this file contributes to the current piece
                start_in_file = max(0, piece_index * piece_length - file_offset)
                end_in_file = min(file_entry.size, (piece_index + 1) * piece_length - file_offset)
                
                if start_in_file < end_in_file:  # The file contributes to this piece
                    f.seek(start_in_file)
                    piece_data += f.read(end_in_file - start_in_file)
            
            # If we've collected enough data for this piece, we're done
            if len(piece_data) >= piece_length:
                break

        # Truncate or pad the piece data if necessary
        piece_data = piece_data[:piece_length]  # Truncate if too long
        if len(piece_data) < piece_length:
            piece_data += b'\0' * (piece_length - len(piece_data))  # Pad with zeros if too short
        
        # Compute hash and verify
        computed_hash = sha1(piece_data).digest()
        expected_hash = info.hash_for_piece(piece_index)
        
        if computed_hash == expected_hash:
            print(f"Piece {piece_index} verified successfully.")
        else:
            print(f"Piece {piece_index} verification failed.")
            print(f"  Expected: {expected_hash.hex()}")
            print(f"  Got: {computed_hash.hex()}")
            print(f"  Data sample: {piece_data[:16].hex() if piece_data else 'No data'}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 verify_torrent.py <torrent_file>")
        sys.exit(1)

    torrent_file = sys.argv[1]
    verify_torrent(torrent_file)
