"""
Image to ASCII Module - Profile Picture Rendering
==================================================

This module handles conversion of profile images to ASCII art for terminal display.

DATABASE INTEGRATION REQUIREMENTS:
----------------------------------
To connect this to PostgreSQL, you'll need to decide how to store images:

OPTION 1: Store file paths in database
---------------------------------------
- Store relative/absolute paths in VARCHAR field
- Keep images on filesystem
- Simpler, but requires file management

users table:
- profile_pic: VARCHAR(255) - stores path like '/uploads/profile_123.png'

Example query:
```python
cursor.execute("SELECT profile_pic FROM users WHERE id = %s", (user_id,))
image_path = cursor.fetchone()[0]
ascii_art = profile_picture(image_path)
```

OPTION 2: Store binary image data in database (BYTEA)
-----------------------------------------------------
- Store images as BYTEA (binary data)
- No file management needed
- May impact database size

users table:
- profile_pic_data: BYTEA - stores actual image bytes

Example query:
```python
cursor.execute("SELECT profile_pic_data FROM users WHERE id = %s", (user_id,))
image_data = cursor.fetchone()[0]

# Save to temp file for processing
import tempfile
with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp:
    tmp.write(image_data)
    tmp_path = tmp.name

ascii_art = profile_picture(tmp_path)
# Clean up temp file after use
os.unlink(tmp_path)
```

RECOMMENDED APPROACH:
--------------------
Use OPTION 1 (file paths) for better performance and simpler implementation.
Store images in a static folder like /uploads/profile_pictures/

Upload handling:
```python
def upload_profile_picture(user_id, uploaded_file):
    # Save file
    filename = f"profile_{user_id}_{int(time.time())}.png"
    filepath = f"/uploads/profile_pictures/{filename}"

    with open(filepath, 'wb') as f:
        f.write(uploaded_file.read())

    # Update database
    cursor.execute('''
        UPDATE users SET profile_pic = %s WHERE id = %s
    ''', (filepath, user_id))
    conn.commit()

    return filepath
```
"""

from ascii_magic import AsciiArt

class profile_picture:
    """
    Convert profile pictures to ASCII art for terminal display.

    DATABASE INTEGRATION:
    --------------------
    This class works with file paths. Ensure your database stores valid paths
    to image files, or implement BYTEA-to-file conversion before using this class.

    Attributes:
    ----------
    image_path : str
        Path to the image file (from filesystem or database)
    """
    def __init__(self, image_path):
        """
        Initialize with image path.

        DATABASE NOTE:
        -------------
        If using BYTEA storage, convert binary data to temp file first:
        ```python
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp:
            tmp.write(binary_data_from_db)
            tmp_path = tmp.name
        pic = profile_picture(tmp_path)
        ```

        Parameters:
        ----------
        image_path : str
            Path to image file
        """
        self.image_path = image_path

    def to_ascii(self, columns=40):
        """
        Convert image to ASCII art string.

        DATABASE INTEGRATION:
        --------------------
        No database queries needed. This is purely image processing.

        Parameters:
        ----------
        columns : int
            Width of ASCII art in characters (default: 40)

        Returns:
        -------
        str
            ASCII art representation of the image

        Raises:
        ------
        FileNotFoundError
            If image_path doesn't exist (check database paths are valid)
        """
        art = AsciiArt.from_image(self.image_path)
        return art.to_ascii(columns=columns, width_ratio=2.0)
