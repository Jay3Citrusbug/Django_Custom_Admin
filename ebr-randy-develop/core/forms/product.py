
from django import forms
from core.models import Product
# from django.core.validators import FileExtensionValidator

class ProductCreationForm(forms.ModelForm):
   

    class Meta:
        model = Product
        exclude = ('is_active', 'create_at', 'update_at')
        labels = {
            "name": "Name",
            "category":"Category",
            "product_code":"code"       
        }



    def clean(self):
        cleaned_data = super(ProductCreationForm, self).clean()
        name = cleaned_data.get("name")
        category = cleaned_data.get("category")
        product_code = cleaned_data.get("product_code")
        
        if not name:
            raise forms.ValidationError("Please enter frame.")
        if not category:
            raise forms.ValidationError("Please enter frame.")
        if not product_code:
            raise forms.ValidationError("Please enter frame.")


    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()

        return instance
    
    
    
    
    

from django import forms
from core.models import Product
# from django.core.validators import FileExtensionValidator

class ProductChangeForm(forms.ModelForm):
   

    class Meta:
        model = Product
        exclude = ('is_active', 'create_at', 'update_at')
        fields = ['name','category','product_code']
        labels = {
            "name": "Name",
            "category":"Category",
            "product_code":"code"
            
            
       
        }



    def clean(self):
        cleaned_data = super(ProductChangeForm, self).clean()
        name = cleaned_data.get("name")
        category = cleaned_data.get("category")
        product_code = cleaned_data.get("product_code")
        
        if not name:
            raise forms.ValidationError("Please enter frame.")
        if not category:
            raise forms.ValidationError("Please enter frame.")
        if not product_code:
            raise forms.ValidationError("Please enter frame.")


    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()

        return instance
    