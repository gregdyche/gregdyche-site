from django import forms
from .models import Subscriber

class SubscriptionForm(forms.ModelForm):
    """Form for blog subscription signup"""
    
    class Meta:
        model = Subscriber
        fields = ['email', 'tech', 'life', 'spirit']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter your email address',
                'required': True
            }),
            'tech': forms.CheckboxInput(attrs={
                'class': 'form-checkbox'
            }),
            'life': forms.CheckboxInput(attrs={
                'class': 'form-checkbox'
            }),
            'spirit': forms.CheckboxInput(attrs={
                'class': 'form-checkbox'
            }),
        }
        labels = {
            'email': 'Email Address',
            'tech': 'Technology Blog',
            'life': 'Life Management Blog',
            'spirit': 'Spiritual Growth Blog',
        }
        help_texts = {
            'email': 'We\'ll never share your email with anyone else.',
            'tech': 'Python development, AI/ML insights, and emerging technologies',
            'life': 'Personal productivity, education, and life optimization',
            'spirit': 'Faith, intentional living, and finding meaning in daily life',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        tech = cleaned_data.get('tech')
        life = cleaned_data.get('life')
        spirit = cleaned_data.get('spirit')
        
        # Ensure at least one category is selected
        if not any([tech, life, spirit]):
            raise forms.ValidationError(
                "Please select at least one blog category to subscribe to."
            )
        
        return cleaned_data
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make email field required
        self.fields['email'].required = True