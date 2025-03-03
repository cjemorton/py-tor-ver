import libtorrent as lt
import os
import sys
from hashlib import sha1
import warnings

# Suppress deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

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
                return False  # Silent fail for missing files

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
        
        if computed_hash != expected_hash:
            return False  # Silent fail for piece mismatch
    return True  # All pieces verified successfully

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
        print("Usage: python3 verify.py <torrent_file> [<download_directory>]")
        sys.exit(0)

    torrent_file = sys.argv[1]
    download_dir = sys.argv[2] if len(sys.argv) > 2 else None

    all_verified = verify_torrent(torrent_file, download_dir)

    if all_verified:
        print("Torrent verified successfully.")
    else:
        print("Torrent verification failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
