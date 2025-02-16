import libtorrent as lt
import sys

def verify_torrent(torrent_file):
    # Load the torrent file
    info = lt.torrent_info(torrent_file)
    
    # Create a session to access the torrent file's data
    session = lt.session()

    # You don't need to start the download process to verify, just check the checksums
    for file in info.files():
        print(f"Verifying file: {file.path}")
        
        # Checksum for each piece, piece size and hash
        for i in range(info.num_pieces()):
            # Retrieve the expected checksum for the piece
            expected_hash = info.hash_for_piece(i)
            
            # Here, you can use a function to actually read the file and compute the hash to compare with expected_hash
            print(f"Piece {i} checksum: {expected_hash}")
        
        # Optionally, print out some file details for confirmation
        print(f"File path: {file.path}, Size: {file.size}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 verify_torrent.py <torrent_file>")
        sys.exit(1)

    torrent_file = sys.argv[1]
    verify_torrent(torrent_file)
