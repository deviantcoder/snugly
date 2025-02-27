import requests
from pathlib import Path


def download_vendor_static(url: str, out_path: Path, parent_mkdir: bool = False):
    """
    Downloads a file from the given URL and saves it to the specified output path.
    Args:
        url (str): The URL of the file to download.
        out_path (Path): The path where the downloaded file will be saved.
        parent_mkdir (bool, optional): If True, create parent directories if they do not exist. Defaults to False.
    Raises:
        ValueError: If out_path is not a valid Path object.
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
        print(f'Error downloading file: {error}')
        return False