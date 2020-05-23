def validate_image_file(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.jpg', '.png', '.webp', '.bmp', '.tiff']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')

    if value.size > 10485760:
        raise ValidationError("The maximum file size that can be uploaded is 10MB")
