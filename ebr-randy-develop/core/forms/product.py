
from django import forms
from core.models import Product
# from django.core.validators import FileExtensionValidator

class ProductCreationForm(forms.ModelForm):
    # name=forms.CharField(max_length=100,required=False)
    # product_code=forms.CharField(max_length=100,required=False)

    class Meta:
        model = Product
        exclude = ('is_active', 'create_at', 'update_at')
        labels = {
            "name": "Name",
            "category":"Category",
            "product_code":"code"       
        }
        
    def __init__(self, *args, **kwargs):
        super(ProductCreationForm, self).__init__(*args, **kwargs)
        
        self.fields['name'].required = False
        self.fields['category'].required = False
        self.fields['product_code'].required = False

    def clean(self):
        cleaned_data = super(ProductCreationForm, self).clean()
        name = cleaned_data.get("name")
        category = cleaned_data.get("category")
        product_code = cleaned_data.get("product_code")
        
        
        if not name and not category and not product_code:
            raise forms.ValidationError([
                forms.ValidationError(('Please enter name.'), code='error1'),
                forms.ValidationError(('Please select category.'), code='error2'),
                forms.ValidationError(('Please enter productcode.'), code='error2'),
            ])
        else:
            if not name and not category:
               raise forms.ValidationError([
                    forms.ValidationError(('Please select name.'), code='error2'),
                    forms.ValidationError(('Please enter category.'), code='error2'),
            ])
            elif not category and  not product_code:
                raise forms.ValidationError([
                    forms.ValidationError(('Please select category.'), code='error2'),
                    forms.ValidationError(('Please enter productcode.'), code='error2'),
            ])
            elif not product_code and  not name:
                raise forms.ValidationError([
                    forms.ValidationError(('Please select name.'), code='error2'),
                    forms.ValidationError(('Please enter productcode.'), code='error2'),
            ])
            else:
                if not name:
                    raise forms.ValidationError("Please enter name.")
                elif not category:
                    raise forms.ValidationError("Please select category.")
                elif not product_code:
                    raise forms.ValidationError("Please enter productcode.")


    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()

        return instance
    
    
    
    
    

from django import forms
from core.models import Product
# from django.core.validators import FileExtensionValidator

class ProductChangeForm(forms.ModelForm):
   
    # name=forms.CharField(max_length=100,required=False)
    # product_code=forms.CharField(max_length=100,required=False)
    
    class Meta:
        model = Product
        exclude = ('is_active', 'create_at', 'update_at')
        fields = ['name','category','product_code']
        labels = {
            "name": "Name",
            "category":"Category",
            "product_code":"code"
            }
    
    def __init__(self, *args, **kwargs):
        super(ProductChangeForm, self).__init__(*args, **kwargs)
        
        self.fields['name'].required = False
        self.fields['category'].required = False
        self.fields['product_code'].required = False
    
    
    
    def clean(self):
        cleaned_data = super(ProductChangeForm, self).clean()
        name = cleaned_data.get("name")
        category = cleaned_data.get("category")
        product_code = cleaned_data.get("product_code")
        
        # if not name:
        #     raise forms.ValidationError("Please enter name.")
        # if not category:
        #     raise forms.ValidationError("Please select category.")
        # if not product_code:
        #     raise forms.ValidationError("Please enter productcode.")
        
        if not name and not category and not product_code:
            raise forms.ValidationError([
                forms.ValidationError(('Please enter name.'), code='error1'),
                forms.ValidationError(('Please select category.'), code='error2'),
                forms.ValidationError(('Please enter productcode.'), code='error2'),
            ])
        else:
            if not name and not category:
               raise forms.ValidationError([
                    forms.ValidationError(('Please select name.'), code='error2'),
                    forms.ValidationError(('Please enter category.'), code='error2'),
            ])
            elif not category and  not product_code:
                raise forms.ValidationError([
                    forms.ValidationError(('Please select category.'), code='error2'),
                    forms.ValidationError(('Please enter productcode.'), code='error2'),
            ])
            elif not product_code and  not name:
                raise forms.ValidationError([
                    forms.ValidationError(('Please select name.'), code='error2'),
                    forms.ValidationError(('Please enter productcode.'), code='error2'),
            ])
            else:
                if not name:
                    raise forms.ValidationError("Please enter name.")
                elif not category:
                    raise forms.ValidationError("Please select category.")
                elif not product_code:
                    raise forms.ValidationError("Please enter productcode.")
                    
            # if not product_code:
            #     raise forms.ValidationError("Please enter productcode.")


    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()

        return instance
    