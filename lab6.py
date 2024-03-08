import requests
import hashlib
import os
import subprocess

# Send GET request to the file URL
def get_expected_hash():
    # Fetch the expected SHA-256 hash value from the VLC website
    file_url = 'http://download.videolan.org/pub/videolan/vlc/last/win64/vlc-3.0.20-win64.exe.sha256'
    response = requests.get(file_url)
    if response.status_code == 200:
        expected_hash = response.text.split()[0]
        # Extract the first hash from the response
        return expected_hash
    else:
        print("Failed to fetch SHA-256 hash value from VLC website.")
        return None

def download_vlc_installer():
    # Download the VLC installer
    url = 'http://download.videolan.org/pub/videolan/vlc/last/win64/vlc-3.0.20-win64.exe'
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        print("Failed to download VLC installer.")
        return None

def compute_hash(data):
    # Compute the SHA-256 hash
    sha256_hash = hashlib.sha256()
    sha256_hash.update(data)
    return sha256_hash.hexdigest()

def save_installer_to_disk(data):
    # Save the downloaded VLC installer to disk
    with open('vlc_installer.exe', 'wb') as file:
        file.write(data)

def run_installer():
    # Silently run the VLC installer
    subprocess.run(['vlc_installer.exe', '/S'])

def delete_installer():
    # Delete the VLC installer from disk
    os.remove('vlc_installer.exe')

def main():
    expected_hash = get_expected_hash()
    if expected_hash:
        print("Expected SHA-256 hash:", expected_hash)
        installer_data = download_vlc_installer()
        if installer_data:
            computed_hash = compute_hash(installer_data)
            print("Computed SHA-256 hash:", computed_hash)
            if expected_hash == computed_hash:
                installer_path = save_installer_to_disk(installer_data)
                run_installer(installer_path)
                delete_installer(installer_path)
                print("VLC Media Player installed successfully.")
            else:
                 print("Integrity check failed. Aborting installation.")
        else:
            print("Failed to download VLC installer.")
    else:
        print("Failed to retrieve expected SHA-256 hash from VLC website.")

        if __name__ == "__main__":
            main()

                
