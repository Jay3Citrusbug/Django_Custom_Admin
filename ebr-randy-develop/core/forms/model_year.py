
from django import forms
from core.models import ModelYear
# from django.core.validators import FileExtensionValidator

class ModelYearCreationForm(forms.ModelForm):
    # """Custom ReviewCategory"""
    # slug = forms.CharField(required=False)
    # meta_title = forms.CharField(required=True, label='Meta Title', widget=forms.TextInput(attrs={'placeholder': '| ElectricBikeReview.com', 'readonly': True}))

    class Meta:
        model = ModelYear
        exclude = ('is_active', 'create_at', 'update_at')
        fields = ['year']
        labels = {
            "year": "Year",
            # "featured_review": "Featured Review",
            # "category_image_full": "Category Image",
            # "description": "Long Description",
            # "short_description": "Short Description(Meta Tags)",
            # "icon_image": "Icon Image",
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field in self.fields:
    #         if field not in ['category_image_full', 'icon_image']:
    #             self.fields[field].widget.attrs.update({'class': 'form-control'})
    #         self.fields['name'].widget.attrs.update({'autofocus': 'autofocus'})

    def clean(self):
        cleaned_data = super(ModelYearCreationForm, self).clean()
        year = cleaned_data.get("year")
        
        if not year:
            raise forms.ValidationError("Please enter year.")

        # if not description:
        #     raise forms.ValidationError("Please enter description.")

        # if category_image_full:
        #     if category_image_full.size > 15097152:
        #         raise forms.ValidationError("Please select image below 15 mb!")

        # if order:
        #     qry = ReviewCategory.objects.filter(order=order, parent_category=parent_category)
        #     if qry.exists():
        #         raise forms.ValidationError("Please select other order for category.")

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()

        return instance
    
    
    
    
    

from django import forms
from core.models import ModelYear

class ModelYearChangeForm(forms.ModelForm):
    # """Custom ReviewCategory"""
    # slug = forms.CharField(required=False)
    # meta_title = forms.CharField(required=True, label='Meta Title', widget=forms.TextInput(attrs={'placeholder': '| ElectricBikeReview.com', 'readonly': True}))

    class Meta:
        model = ModelYear
        exclude = ('is_active', 'create_at', 'update_at')
        fields = ['year']
        labels = {
            "year": "Year",
            # "featured_review": "Featured Review",
            # "category_image_full": "Category Image",
            # "description": "Long Description",
            # "short_description": "Short Description(Meta Tags)",
            # "icon_image": "Icon Image",
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field in self.fields:
    #         if field not in ['category_image_full', 'icon_image']:
    #             self.fields[field].widget.attrs.update({'class': 'form-control'})
    #         self.fields['name'].widget.attrs.update({'autofocus': 'autofocus'})

    def clean(self):
        cleaned_data = super(ModelYearChangeForm, self).clean()
        year = cleaned_data.get("year")
        
        if not year:
            raise forms.ValidationError("Please enter year.")

        # if not description:
        #     raise forms.ValidationError("Please enter description.")

        # if category_image_full:
        #     if category_image_full.size > 15097152:
        #         raise forms.ValidationError("Please select image below 15 mb!")

        # if order:
        #     qry = ReviewCategory.objects.filter(order=order, parent_category=parent_category)
        #     if qry.exists():
        #         raise forms.ValidationError("Please select other order for category.")

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()

        return instance