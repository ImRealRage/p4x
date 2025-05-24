import hashlib
import os
import zlib

PAX_DIR = ".pax"

def hash_object(file_path, obj_type="blob"):
    """
    Hash a file and store it as a Pax object.

    This function reads the content of the specified file, constructs a
    header with the given object type and file size, and computes the SHA1
    hash of the combined header and file content. The resulting SHA1 hash
    is used to store the compressed file data in the Pax object directory.

    Parameters
    ----------
    file_path : str
        The path to the file to be hashed.
    obj_type : str, optional
        The type of the object (e.g., "blob", "tree"). Defaults to "blob".

    Returns
    -------
    str
        The SHA1 hash of the stored object.
    """
    with open(file_path, "rb") as f:
        data = f.read()

    header = f"{obj_type} {len(data)}".encode() + b"\0"
    full_data = header + data

    sha1 = hashlib.sha1(full_data).hexdigest()

    dir_name = os.path.join(".pax", "objects", sha1[:2])
    file_name = sha1[2:]
    os.makedirs(dir_name, exist_ok=True)

    with open(os.path.join(dir_name, file_name), "wb") as out:
        out.write(zlib.compress(full_data))

    return sha1
