from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field

from utils.send_verify_email import send_verify_email

User = get_user_model()


class RoleBasedCreationForm(UserCreationForm):
    """
    Base form for creating users with role-based functionality.

    Methods:
        __init__(*args, **kwargs):
            Initializes the form with custom layout and field properties using crispy forms.
        save(commit=True):
            Saves the user instance with the assigned role.
        clean_email():
            Validates that the email is unique.
    """

    role = None

    def __init__(self, *args, **kwargs):
        self.form_action = kwargs.pop('form_action', 'users:register_user')

        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = self.form_action
        self.helper.layout = Layout(
            Row(
                Column(Field('first_name', css_class='radius-md p-2', placeholder='John', required=True), css_class='form-group col-md-6 mb-0'),
                Column(Field('last_name', css_class='radius-md p-2', placeholder='Doe', required=True), css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column(Field('email', css_class='radius-md p-2', placeholder='johndoe@gmail.com', required=True), css_class='form-group col-md-6 mb-0'),
                Column(Field('username', css_class='radius-md p-2', placeholder='johndoe', help_text='', required=True), css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Field('password1', css_class='radius-md p-2', placeholder='Enter password'),
            Field('password2', css_class='radius-md p-2', placeholder='Confirm password'),
            Row(
                Column(
                    Submit('submit', 'Sign Up', css_class='btn btn-success light-green border-0 hover-grow-sm radius-md pe-5 ps-5'),
                    css_class='text-center'
                ),
            )
        )

        for fieldname in ('username', 'password1', 'password2'):
            self.fields[fieldname].help_text = None

        self.fields['password1'].label = 'Password'
        self.fields['password2'].label = 'Confirm password'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.role if self.role else User.Roles.USER

        user.is_active = False

        if commit:
            user.save()
            send_verify_email(user)

        return user

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already in use.')
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already in use.')
        return username.strip().lower()


class UserCreationForm(RoleBasedCreationForm):
    """
    Form for creating regular users with the USER role. Inherits from RoleBasedCreationForm.
    Methods:
        save(commit=True): Saves the user instance with an additional role attribute.
    """

    role = User.Roles.USER

    def __init__(self, *args, **kwargs):
        super().__init__(*args, form_action='users:register_user', **kwargs)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class MentorCreationForm(RoleBasedCreationForm):
    """
    Form for creating new mentor users with the MENTOR role. Inherits from RoleBasedCreationForm.
    Methods:
        save(commit=True): Saves the user instance with an additional role attribute.
    """

    role = User.Roles.MENTOR

    def __init__(self, *args, **kwargs):
        super().__init__(*args, form_action='users:register_mentor', **kwargs)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')