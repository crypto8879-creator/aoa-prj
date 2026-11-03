#Create a folder, for example my project.
#Open the folder in VS Code.
#Create a Python file named prac.py.
#Paste the above code.
#Keep sample.txt in the same folder (or the code will create it).
#Open CMD in that folder.
#py prac.py
import os
import shutil
import hashlib

# Create cloud folder
os.makedirs("cloud_upload", exist_ok=True)

# Function to add watermark
def watermark_text(file_path, user_id):

    with open(file_path, "r") as f:
        content = f.read()

    # Generate watermark
    watermark = hashlib.sha256(user_id.encode()).hexdigest()

    # Add watermark to file
    new_file = "wm_" + os.path.basename(file_path)

    with open(new_file, "w") as f:
        f.write(content + "\nUSER-ID: " + watermark)

    # Upload file
    shutil.copy(new_file, "cloud_upload")

    print("Watermark added successfully")
    print("File uploaded to cloud_upload folder:", new_file)


# Main program
if __name__ == "__main__":

    file = "sample.txt"

    # Create sample file if not present
    if not os.path.exists(file):
        with open(file, "w") as f:
            f.write("This is confidential data.")

    watermark_text(file, "user123")
