

from django.forms import ModelForm, CharField, TextInput, EmailInput, PasswordInput, ValidationError
from .models import User



def fieldAttributesWithPlaceholder(placeholder: str) -> dict:
    return {'class': 'input-field', 'placeholder': placeholder, 'required': True}



# form to handle the sign up
class CreateUserForm(ModelForm):

    confirm_password = CharField(
        label='Confirm Password',
        widget=PasswordInput(
            attrs=fieldAttributesWithPlaceholder('Confirm Password'),
        )
    )

    class Meta:

        model = User
        fields = ['username', 'email', 'password']

        widgets = {

            'username': TextInput(
                attrs=fieldAttributesWithPlaceholder('Username'),
            ),

            'email': EmailInput(  
                attrs=fieldAttributesWithPlaceholder('Email')
            ),

            'password': PasswordInput(
                attrs=fieldAttributesWithPlaceholder('Password')
            ),
        }


    #the clean method for the form class
    #purposefully for validating the user password

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        cPassword = cleaned_data.get('confirm_password')


        username = User.objects.get(username = cleaned_data.get('username'))

        if username:
            raise ValidationError('Username already exists. Try a different one.')

        if password and cPassword and cPassword != password:
            raise ValidationError('Passwords do not match.')

        return cleaned_data





class LoginUserForm(ModelForm):

    class Meta:

        model = User
        fields = ['username', 'password']

        widgets = {

            'username': TextInput(
                attrs=fieldAttributesWithPlaceholder('Username')
            ),

            'password': PasswordInput(
                attrs=fieldAttributesWithPlaceholder('Password')
            )
        }

    
    def clean(self):

        cleaned_data = super().clean()

        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if not username:
            raise ValidationError('The username field cannot be empty')
        
        if not password:
            raise ValidationError('The password field cannot be empty')
        


        user = User.objects.get(username=username, password=password)
        

        if not user:
            raise ValidationError('Incorrect username or password.')

        return cleaned_data
    



