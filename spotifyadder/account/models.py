from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to="users/%Y/%m/%d/", blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"


'''
The one-to-one field user will be used to associate profiles with users. We use AUTH_USER_MODEL to
refer to the user model instead of pointing to the auth.User model directly. This makes our code
more generic, as it can operate with custom-defined user models. With on_delete=models.CASCADE,
we force the deletion of the related Profile object when a User object gets deleted.
The date_of_birth field is a DateField. We have made this field optional with blank=True, and we
allow null values with null=True.

The photo field is an ImageField. We have made this field optional with blank=True. An ImageField
field manages the storage of image files. It validates that the file provided is a valid image, stores the
image file in the directory indicated with the upload_to parameter, and stores the relative path to the
file in the related database field. An ImageField field is translated to a VARHAR(100) column in the
database by default. A blank string will be stored if the value is left empty.
'''

