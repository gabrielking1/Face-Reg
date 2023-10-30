from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Registration,Course
from django.forms import ModelMultipleChoiceField










class RegForm(UserCreationForm):

    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('first_name','last_name', 'username', 'email', 'password1' ,'password2' )



class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        fields ="__all__"


    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        
        self.fields['face_id'].widget = forms.HiddenInput()


class CourseForm(forms.ModelForm):
    # feedback = forms.CharField(widget=forms.Textarea)
    course = ModelMultipleChoiceField(queryset=Course.objects.all(), widget = forms.CheckboxSelectMultiple)
    class Meta:
        model = Registration
        fields = "__all__"
        
    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        
        # self.fields['username'].widget = forms.HiddenInput()

class RegistrationForm(UserCreationForm):
    categories = ModelMultipleChoiceField(queryset=Course.objects.all())

    class Meta:
        model = Registration
        fields = "__all__"

    
