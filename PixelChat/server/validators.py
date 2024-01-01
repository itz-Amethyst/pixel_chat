import os.path

from rest_framework.exceptions import ValidationError


valid_extensions = [".jpg", ".png", ".jpeg", ".gif"]
max_file_size = 4 * 1024 * 1024

def validate_icon_image_size(image):
    if image:
        # with Image.open(image) as img:
        #     if img.width > 70 or img.height > 70:
        #         raise ValidationError(detail = f"The maximum allowed size for image are 70x70")

        if image.size > max_file_size:
            raise ValidationError(detail = f"The maximum allowed size for image is 4MB")



def validate_image_file_extension(file):
    ext = os.path.splitext(file.name)[1]
    if not ext.lower() in valid_extensions:
        raise ValidationError(detail = "Unsupported file. only (jpeg png gif) allowed")
