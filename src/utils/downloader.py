from pathlib import Path

import requests


def download_vendor_static(url: str, out_path: Path, parent_mkdir: bool = False):
    """
    Downloads a file from the specified URL and saves it to the given output path.
    Args:
        url (str): The URL of the file to download.
        out_path (Path): The path where the downloaded file will be saved.
        parent_mkdir (bool, optional): If True, create parent directories if they do not exist.
    Returns:
        bool: True if the file was downloaded and saved successfully, False otherwise.
    """

    if not isinstance(out_path, Path):
        raise ValueError('out_path must be a valid Path object')
    
    if parent_mkdir:
        out_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        response = requests.get(url)
        response.raise_for_status()

        out_path.write_bytes(response.content)

        return True
    except requests.RequestException as error:
        print('Error downloading file') # < change to logging
        return False