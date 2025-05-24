import hashlib
import os
import zlib

PAX_DIR = ".pax"

def hash_object(file_path):
    """
    Hashes a file and stores it in the .pax/objects directory.

    Parameters
    ----------
    file_path : str
        The path to the file to hash.

    Returns
    -------
    str
        The SHA1 of the file.
    """
    with open(file_path, "rb") as f:
        data = f.read()

    header = f"blob {len(data)}\0".encode()
    full_data = header + data

    sha1 = hashlib.sha1(full_data).hexdigest()

    # Split into directory and file: objects/ab/cdef...
    dir_name = os.path.join(PAX_DIR, "objects", sha1[:2])
    file_name = sha1[2:]

    os.makedirs(dir_name, exist_ok=True)
    object_path = os.path.join(dir_name, file_name)

    with open(object_path, "wb") as f:
        f.write(zlib.compress(full_data))

    print(sha1)
    return sha1 
