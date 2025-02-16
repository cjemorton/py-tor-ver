import subprocess
import sys
import re

def run_torrent_verification(torrent_file):
    try:
        # Run the verification script
        result = subprocess.run(
            ['python3', 'verify_torrent.py', torrent_file],
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

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 wrapper_script.py <torrent_file>")
        sys.exit(1)
    
    torrent_file = sys.argv[1]
    run_torrent_verification(torrent_file)
