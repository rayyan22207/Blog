from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'profile_pic', 'bio', 'age', 'website', 'location']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter full name'}),
            'profile_pic': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Tell us about yourself'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Your age'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Your website or portfolio'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City, Country'}),
        }
