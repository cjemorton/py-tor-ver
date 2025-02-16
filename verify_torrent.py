import sys
import libtorrent as lt
import os

def verify_torrent(torrent_file_path):
    # Create a session
    ses = lt.session()
    
    # Read the torrent file from disk
    with open(torrent_file_path, 'rb') as f:
        torrent_info = lt.torrent_info(lt.bdecode(f.read()))

    # Add the torrent to the session for checking purposes
    params = {
        'save_path': os.path.expanduser('~'),  # Default save path, adjust based on your needs
        'storage_mode': lt.storage_mode_t.storage_mode_sparse,
        'flags': lt.add_torrent_paramsFlags_t.flag_duplicate_is_error,
        'ti': torrent_info
    }
    handle = ses.add_torrent(params)

    # Force recheck on the torrent
    handle.force_recheck()

    # Wait for the recheck to complete
    while handle.status().state == lt.torrent_status.checking_files:
        print("Checking files...")
        time.sleep(1)

    # Check the status after recheck
    status = handle.status()
    if status.verified_pieces == status.total_pieces:
        print("Verification complete: All pieces match the torrent file.")
    else:
        print(f"Verification failed. {status.verified_pieces}/{status.total_pieces} pieces match.")

    # Clean up
    ses.remove_torrent(handle)

if __name__ == "__main__":
    if len(sys.argv) != 2 or not sys.argv[1].endswith('.torrent'):
        print("Usage: python3 verify_torrent2.py <path_to_torrent_file>")
        sys.exit(1)
    
    try:
        verify_torrent(sys.argv[1])
    except Exception as e:
        print(f"An error occurred: {e}")
