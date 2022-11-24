
from django import forms
from core.models import FrameType
# from django.core.validators import FileExtensionValidator

class FrameTypeCreationForm(forms.ModelForm):
   

    class Meta:
        model = FrameType
        exclude = ('is_active', 'create_at', 'update_at')
        fields = ['frame_type']
        labels = {
            "frame_type": "FrameType",
       
        }



    def clean(self):
        cleaned_data = super(FrameTypeCreationForm, self).clean()
        frame_type = cleaned_data.get("frame_type")
        
        if not frame_type:
            raise forms.ValidationError("Please enter frame.")


    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()

        return instance
    
    
    
    
    

from django import forms
from core.models import FrameType

class FrameTypeChangeForm(forms.ModelForm):
    

    class Meta:
        model = FrameType
        exclude = ('is_active', 'create_at', 'update_at')
        fields = ['frame_type']
        labels = {
            "frame_type": "FrameType",
        }

   

    def clean(self):
        cleaned_data = super(FrameTypeChangeForm, self).clean()
        frame_type = cleaned_data.get("frame_type")
        
        if not frame_type:
            raise forms.ValidationError("Please enter frame.")

        

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()

        return instance