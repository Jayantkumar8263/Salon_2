from django import forms
from . models import Appointment

#__Appointment-Form Model___
class AppointmentForm(forms.ModelForm):
    start_time = forms.DateTimeField(label= "Appointment date and time ", widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}))
    class Meta:
        model = Appointment  # Connecting form to the appointment model, Tell's the modelForm which model to use.
        fields = ['staff', 'service', 'start_time']
        
        def __init__(self, *args, **kwargs):# We add this to make the dropdowns look nice with Bootstrap.
            super().__init__( *args, **kwargs)# Run the parent's setup first
            self.fields['staff'].widget.attrs.update({'class': 'form-select'})
            self.fields['service'].widget.attrs.update({'class': 'form-select'})
            service = None
        def clean(self):
            cleaned_data = super().clean() # It gets all the clean data in the form. 
            staff = cleaned_data.get('staff')
            service = cleaned_data.get("service")
            if staff and service:# it check's if both exist before comparing them.
                if service not in staff.services.all():# it will rise the validation error 
                    raise forms.ValidationError(f"{staff.user.first_name} does not performs this service, please check the staff's services")
            return cleaned_data
