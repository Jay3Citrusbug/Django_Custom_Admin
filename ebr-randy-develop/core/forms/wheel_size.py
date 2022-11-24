
from django import forms
from core.models import WheelSize
# from django.core.validators import FileExtensionValidator

class WheelSizeCreationForm(forms.ModelForm):
   

    class Meta:
        model = WheelSize
        exclude = ('is_active', 'create_at', 'update_at')
        fields = ['wheel_size']
        labels = {
            "wheel_size": "WheelSize",
       
        }



    def clean(self):
        cleaned_data = super(WheelSizeCreationForm, self).clean()
        wheel_size = cleaned_data.get("wheel_size")
        
        if not wheel_size:
            raise forms.ValidationError("Please enter size.")


    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()

        return instance
    
    
    
    
    

from django import forms
from core.models import WheelSize

class WheelSizeChangeForm(forms.ModelForm):
    

    class Meta:
        model = WheelSize
        exclude = ('is_active', 'create_at', 'update_at')
        fields = ['wheel_size']
        labels = {
            "wheel_size": "WheelSize",
        }

   

    def clean(self):
        cleaned_data = super(WheelSizeChangeForm, self).clean()
        wheel_size = cleaned_data.get("wheel_size")
        
        if not wheel_size:
            raise forms.ValidationError("Please enter size.")

        

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()

        return instance