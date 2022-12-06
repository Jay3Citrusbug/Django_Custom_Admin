
from django import forms
from core.models import Product
# from django.core.validators import FileExtensionValidator

class ProductCreationForm(forms.ModelForm):
    # name=forms.CharField(max_length=100,required=False)
    # product_code=forms.CharField(max_length=100,required=False)

    class Meta:
        model = Product
        exclude = ('is_active', 'create_at', 'update_at')
        fields = ['name','category','product_code','description','short_description','price']
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
        self.fields['description'].required = False
        self.fields['short_description'].required = False
        self.fields['price'].required = False

    # def clean(self):
    #     cleaned_data = super(ProductCreationForm, self).clean()
    #     print(cleaned_data)

    #     name = cleaned_data.get("name")
    #     category = cleaned_data.get("category")
    #     product_code = cleaned_data.get("product_code")
        

    def clean(self):
        
        super(ProductCreationForm, self).clean()
         
        # extract the username and text field from the data
        name = self.cleaned_data.get('name')
        category = self.cleaned_data.get('category')
        product_code = self.cleaned_data.get('product_code')
        description = self.cleaned_data.get("description")
        short_description = self.cleaned_data.get("short_description")
        price = self.cleaned_data.get("price")


        if not name:
            self._errors['name'] = self.error_class([
                'name empty'])
        if not category:
            self._errors['category'] = self.error_class([
                'category empty'])
        if not product_code:
            self._errors['product_code'] = self.error_class([
                'code empty'])
        if not description:
            self._errors['description'] = self.error_class([
                'code empty'])
        if not short_description:
            self._errors['short_description'] = self.error_class([
                'code empty'])
        if not price:
            self._errors['price'] = self.error_class([
                'code empty'])
        return self.cleaned_data           


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
        fields = ['name','category','product_code','description','short_description','price']
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
        self.fields['description'].required = False
        self.fields['short_description'].required = False
        self.fields['price'].required = False
    
    
    
    def clean(self):
        cleaned_data = super(ProductChangeForm, self).clean()
        
        name = cleaned_data.get("name")
        category = cleaned_data.get("category")
        product_code = cleaned_data.get("product_code")
        description = cleaned_data.get("description")
        short_description = cleaned_data.get("short_description")
        price = cleaned_data.get("price")

        if not name:
            self._errors['name'] = self.error_class([
                'name empty'])
        if not category:
            self._errors['category'] = self.error_class([
                'category empty'])
        if not product_code:
            self._errors['product_code'] = self.error_class([
                'code empty'])
        if not description:
            self._errors['description'] = self.error_class([
                'code empty'])
        if not short_description:
            self._errors['short_description'] = self.error_class([
                'code empty'])
        if not price:
            self._errors['price'] = self.error_class([
                'code empty'])
        return self.cleaned_data       
        
        # if not name and not category and not product_code:
        #     raise forms.ValidationError([
        #         forms.ValidationError(('Please enter name.'), code='error1'),
        #         forms.ValidationError(('Please select category.'), code='error2'),
        #         forms.ValidationError(('Please enter productcode.'), code='error2'),
        #     ])
        # else:
        #     if not name and not category:
        #        raise forms.ValidationError([
        #             forms.ValidationError(('Please select name.'), code='error2'),
        #             forms.ValidationError(('Please enter category.'), code='error2'),
        #     ])
        #     elif not category and  not product_code:
        #         raise forms.ValidationError([
        #             forms.ValidationError(('Please select category.'), code='error2'),
        #             forms.ValidationError(('Please enter productcode.'), code='error2'),
        #     ])
        #     elif not product_code and  not name:
        #         raise forms.ValidationError([
        #             forms.ValidationError(('Please select name.'), code='error2'),
        #             forms.ValidationError(('Please enter productcode.'), code='error2'),
        #     ])
        #     else:
        #         if not name:
        #             raise forms.ValidationError("Please enter name.")
        #         elif not category:
        #             raise forms.ValidationError("Please select category.")
        #         elif not product_code:
        #             raise forms.ValidationError("Please enter productcode.")
                    
            # if not product_code:
            #     raise forms.ValidationError("Please enter productcode.")


    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()

        return instance
    