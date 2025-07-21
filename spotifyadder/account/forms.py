from django import forms
from django.contrib.auth import get_user_model
from .models import Profile

from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    # The PasswordInput widget is used to render the password HTML element. This will include type="password" in the HTML so that the browser treats it as a password input.


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat password", widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ["username", "first_name", "email"]

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Passwords don't match.")
        return cd["password2"]

    def clean_email(self):
        data = self.cleaned_data["email"]
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("Email already in use.")
        return data


"""This form includes the fields username, first_name,
and email of the user model. We retrieve the user model dynamically by using the get_user_model()
function provided by the auth application. This retrieves the user model, which could be a custom
model instead of the default auth User model, since Django allows you to define custom user models.
These fields will be validated according to the validations of their corresponding model fields. For
example, if the user chooses a username that already exists, they will get a validation error because
username is a field defined with unique=True.

In order to keep your code generic, use the get_user_model() method to retrieve the
user model and the AUTH_USER_MODEL setting to refer to it when defining a model’s rela-
tionship with in to it, instead of referring to the auth user model directly. You can read
more information about this at https://docs.djangoproject.com/en/5.0/topics/
auth/customizing/#django.contrib.auth.get_user_model.

clean_password2() method to compare the second password against the first one
and raise a validation error if the passwords don’t match. This method is executed when the form is
validated by calling its is_valid() method. You can provide a clean_<fieldname>() method to any
of your form fields to clean the value or raise form validation errors for a specific field. Forms also
include a general clean() method to validate the entire form, which is useful to validate fields that
depend on each other. In this case, we use the field-specific clean_password2() validation instead
of overriding the clean() method of the form. This avoids overriding other field-specific checks that
the ModelForm gets from the restrictions set in the model (for example, validating that the username
is unique).

We have added validation for the email field that prevents users from registering with an existing
email address. We build a QuerySet to look up existing users with the same email address. We check
whether there are any results with the exists() method. The exists() method returns True if the
QuerySet contains any results, and False otherwise.

"""


class UserEditForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "email"]

    def clean_email(self):
        data = self.cleaned_data["email"]
        qs = User.objects.exclude(id=self.instance.id).filter(email=data)
        if qs.exists():
            raise forms.ValidationError("Email already in use.")
        return data


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["date_of_birth", "photo"]


"""These forms are as follows:
•
UserEditForm: This will allow users to edit their first name, last name, and email, which are
attributes of the built-in Django user model.
•
ProfileEditForm: This will allow users to edit the profile data that is saved in the custom
Profile model. Users will be able to edit their date of birth and upload an image for their
profile picture.

we have added validation for the email field that prevents users from changing their ex-
isting email address to an existing email address of another user. We exclude the current user from
the QuerySet. Otherwise, the current email address of the user would be considered an existing email
address, and the form won’t validate.
"""
