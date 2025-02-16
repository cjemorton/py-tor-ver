import subprocess
import sys
import re

def run_torrent_verification(torrent_file, download_dir=None):
    try:
        # Prepare arguments for subprocess.run
        args = ['python3', 'verify_torrent.py', torrent_file]
        if download_dir:
            args.append(download_dir)
        
        # Run the verification script
        result = subprocess.run(
            args,
            check=True,
            text=True,
            capture_output=True
        )
        
        # Check for any piece verification failure
        if "verification failed" in result.stdout:
            print("Error: One or more pieces failed verification.")
            sys.exit(1)

        # If no verification failures were found, all pieces passed
        print("All pieces verified successfully.")

    except subprocess.CalledProcessError as e:
        # If the script itself fails, print the error and exit
        print(f"An error occurred while running the verification script: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
        print("Usage: python3 wrapper_script.py <torrent_file> [<download_directory>]")
        sys.exit(0)

    torrent_file = sys.argv[1]
    download_dir = sys.argv[2] if len(sys.argv) > 2 else None
    run_torrent_verification(torrent_file, download_dir)

if __name__ == "__main__":
    main()
