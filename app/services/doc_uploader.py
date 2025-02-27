import os

class DocUploader:
    def __init__(self, upload_dir="uploads"):
        """Initialize the uploader with a directory to store files."""
        self.upload_dir = upload_dir
        os.makedirs(self.upload_dir, exist_ok=True)  

    def save_file(self, file, filename):
        """
        Save the uploaded file to the upload directory.
        
        :param file: File-like object (can be Flask's `request.files['file']`)
        :param filename: Name to save the file as
        :return: Path of the saved file
        """
        file_path = os.path.join(self.upload_dir, filename)
        with open(file_path, "wb") as f:
            f.write(file)  # Write file content
        return file_path

    def delete_file(self, filename):
        """
        Delete a file from the upload directory.
        
        :param filename: Name of the file to be deleted
        :return: True if deleted, False if file does not exist
        """
        file_path = os.path.join(self.upload_dir, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
