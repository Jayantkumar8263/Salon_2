from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import CustomerProfile

#___UserCreationForm_____
class CustomerSign_upForm(UserCreationForm):
    first_name = forms.CharField(max_length = 50, required = True, help_text = 'Required')
    last_name = forms.CharField(max_length = 50, required = True, help_text = 'Required')
    email = forms.EmailField(max_length= 250, required=False, help_text= 'Required for the authentication, Enter valid EmailId')
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {

            "first_name": forms.TextInput(attrs={

                "class":"form-control custom-input"

            }),

            "last_name": forms.TextInput(attrs={

                "class":"form-control custom-input"

            }),

            "username": forms.TextInput(attrs={

                "class":"form-control custom-input"

            }),

            "email": forms.EmailInput(attrs={

                "class":"form-control custom-input"

            }),

        }
        def save(self, commit = True):
            user = super().save(commit = False)
            user.first_name = self.cleaned['first_name']
            user.last_name = self.cleaned['last_name']
            user.email = self.cleaned['email']
            if commit:
                user.save()
                CustomerProfile.objects.create(user = user)
            return user

#____Custom User Registration Form with Email____
class CustomRegistrationForm(UserCreationForm):

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={ # here widget is used to customize the appearance of the form field in the HTML output, in form we are using bootstrap classes to make the form look good, class is used to apply CSS styles to the form field, palaceholder is used to provide a hint to the user about what to enter in the field.
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )

    class Meta: # here meta is used to specify the model and fields to be included in the form, meta is a nested class within the form class that provides metadata about the form.
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter username'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Password fields ko bhi Bootstrap class dene ke liye
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter password'
        })

        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })

#___Profile Update Form____
# class ProfileUpdateForm(forms.ModelForm):
#     email = forms.EmailField(required=True)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'first_name', 'last_name']
#         model = CustomerProfile # Connecting form to the CustomerProfile model, this model has fields like phone number, banner, avatar etc.
#         fields = ['phone_number', 'banner', 'avatar']

#     def __init__(self, *args, **kwargs):# we use def __init__(self, *args, **kwargs): to customize the initialization of the form and add Bootstrap classes to the form fields for better styling, here self is for the instance of the form, *args and **kwargs are used to pass variable number of arguments to the method.
#         self.user = kwargs.get('instance')# this line retrieves the user details passed to the form during initialization and assigns/stores it to self.user for later use,
#         # we are using instance for updating the user details.
#         super().__init__(*args, **kwargs)

#         for field in self.fields.values():
#             field.widget.attrs.update({'class': 'form-control'})


"""# ___ Customer Profile Update Form____
class CustomerProfileUpdateForm(forms.ModelForm):# this form is for updating the customerdetails like phone number, banner, avatar in the profile page, i created this form seprately because these fields are in the customerprofile model not in the user model.
    class Meta:
        model = CustomerProfile # Connecting form to the CustomerProfile model, this model has fields like phone number, banner, avatar etc.
        fields = ['phone_number', 'banner', 'avatar']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values(): # i am using this loop to add bootstrap class to all the fields in the form, values() is for getting the field objects like CharField, ImageField etc.
            field.widget.attrs.update({'class': 'form-control'}) # adding bootstrap class to all the fields in the form, 'form-control' is a bootstrap class for styling the form fields, update() method is used to add the class to the existing classes of the field, ye update karta hai existing classes ko.
"""


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control'
            })


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = CustomerProfile
        fields = [
            'phone_number',
            'banner',
            'avatar',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control'
            })