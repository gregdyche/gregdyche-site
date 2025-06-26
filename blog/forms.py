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


class CoachingInquiryForm(forms.Form):
    """Form for coaching inquiry submissions"""
    
    INTEREST_CHOICES = [
        ('private', 'Private Session'),
        ('business', 'Business Lunch & Learn'),
        ('custom', 'Something Custom'),
        ('exploring', 'Just Exploring'),
    ]
    
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Your name',
            'required': True
        })
    )

class ContactPageInquiryForm(forms.Form):
    """Form for contact page inquiry submissions"""

    INTEREST_CHOICES = [
        ('ai', 'AI & Technology'),
        ('python', 'Python Development'),
        ('education', 'Educational Technology'),
        ('productivity', 'Productivity Systems'),
        ('career', 'Career & Tech Transitions'),
        ('faith', 'Faith & Intentional Living'),
        ('other', 'Something Else'),
    ]

    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Your name',
            'required': True
        })
    )

    interest = forms.ChoiceField(
        choices=INTEREST_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'required': True
        })
    )

    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-textarea',
            'rows': 4,
            'placeholder': 'Your message...',
            'required': True
        })
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'your.email@example.com',
            'required': True
        })
    )
    
    interest = forms.ChoiceField(
        choices=INTEREST_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'required': True
        })
    )
    
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-textarea',
            'rows': 4,
            'placeholder': 'Tell me about your challenge or goal...',
            'required': True
        })
    )