
from django import forms
from core.models import BreakType
# from django.core.validators import FileExtensionValidator

class BreakTypeCreationForm(forms.ModelForm):
   

    class Meta:
        model = BreakType
        exclude = ('is_active', 'create_at', 'update_at')
        fields = ['break_type']
        labels = {
            "break_type": "BreakType",
       
        }



    def clean(self):
        cleaned_data = super(BreakTypeCreationForm, self).clean()
        break_type = cleaned_data.get("break_type")
        
        if not break_type:
            raise forms.ValidationError("Please enter type.")


    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()

        return instance
    
    
    
    
    

from django import forms
from core.models import BreakType

class BreakTypeChangeForm(forms.ModelForm):
    

    class Meta:
        model = BreakType
        exclude = ('is_active', 'create_at', 'update_at')
        fields = ['break_type']
        labels = {
            "break_type": "BreakType",
        }

   

    def clean(self):
        cleaned_data = super(BreakTypeChangeForm, self).clean()
        break_type = cleaned_data.get("break_type")
        
        if not break_type:
            raise forms.ValidationError("Please enter type.")

        

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()

        return instance