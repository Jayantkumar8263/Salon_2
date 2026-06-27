from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from Staff_app.models import StaffProfile

# ___ Staff Profile Update Form____
class StaffProfileForm(forms.ModelForm):
    class Meta:
        model = StaffProfile
        fields = ['phone_number', 'photo', 'bio', 'Service', 'experience_years']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-select', 'multiple': True})
            
# ___ Staff Registration 
class StaffRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length = 50, required = True, help_text = 'Required')
    last_name = forms.CharField(max_length = 50, required = True, help_text = 'Required')
    email = forms.EmailField(max_length= 250, required=False, help_text= 'Required for the authentication, Enter valid EmailId')
    
    class Meta : # setting for our user creation form
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        def save(self, commit = True):
            user = super().save(commit = False)# In this line we are calling the *parent* form's to save the recient changes in the form by using the method ('super()').
            user.first_name = self.cleaned['first_name']# here user is stil the object which is saved in the memory, now we are adding extra data, using cleaned data.
            user.last_name = self.cleaned['last_name']
            user.email = self.cleaned['email']
            user.is_staff = True
            if commit :
                user.save()
                StaffProfile.objects.create(user = user)
            return user