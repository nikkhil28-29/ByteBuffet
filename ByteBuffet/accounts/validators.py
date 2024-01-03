from django.core.exceptions import ValidationError
import os

#custom validator fun, so thatw e can dispaly our instructions ..when an error occur
def allow_only_images_validator(value):
    ext = os.path.splitext(value.name)[1] #example- cover-image(0).jpg(1(index))   #extension, we need the to tell about 1st index
    print(ext)
    valid_extensions = ['.png', '.jpg', '.jpeg']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension. Allowed FileType: ' +str(valid_extensions))