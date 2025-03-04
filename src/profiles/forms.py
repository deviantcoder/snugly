from django import forms

from django.contrib.auth import get_user_model
from django.urls import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, HTML

from accounts.forms import BaseAppUserCreationForm

from .models import MentorProfile, UserProfile


User = get_user_model()


class BaseProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.form_url_name = kwargs.pop('form_url_name', None)

        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'

        if self.form_url_name is not None:
            self.helper.attrs = {
                'hx-post': reverse(self.form_url_name),
                'hx-encoding': 'multipart/form-data',
                'hx-trigger': 'submit',
            }

        self.base_layout = Layout(
            HTML('<div class="modal-footer border-0 pt-0 px-4">'),
            Submit('submit', 'Save', css_class='btn btn-primary radius-md px-4 fw-medium', css_id='submit-btn'),
            # HTML('<button type="button" class="btn btn-outline-secondary radius-md px-4 fw-medium" data-bs-dismiss="modal"><i class="bi bi-x-circle me-2"></i> Close</button>'),
            HTML('</div>')
        )
        self.helper.layout = self.base_layout

    def append_fields(self, fields_layout):
        """
        Helper method to append fields to the base layout.
        """

        self.helper.layout = Layout(
            fields_layout,
            self.base_layout
        )


class MentorCreationForm(BaseAppUserCreationForm):
    """
    Form for creating new mentor users with the MENTOR role. Inherits from BaseAppUserCreationForm.
    """

    role = User.Roles.MENTOR

    def __init__(self, *args, **kwargs):
        super().__init__(*args, form_action='profiles:register_mentor', **kwargs)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class MentorProfileForm(BaseProfileForm):
    class Meta:
        model = MentorProfile
        fields = ('image', 'bio', 'experience', 'availability')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        mentor_fields = Layout(
            Field('image', css_class='form-control rounded-2 p-2'),
            Field('bio', css_class='form-control rounded-2 p-2', placeholder='Tell us a bit about yourself'),
            Field('experience', css_class='form-control rounded-2 p-2', placeholder='What experience do you have?'),
            Field('availability', css_class='form-control rounded-2 p-2', placeholder='What time are you available?'),
        )

        self.append_fields(mentor_fields)


class UserCreationForm(BaseAppUserCreationForm):
    """
    Form for creating regular users with the USER role. Inherits from BaseAppUserCreationForm.
    """

    role = User.Roles.USER

    def __init__(self, *args, **kwargs):
        super().__init__(*args, form_action='profiles:register_user', **kwargs)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        

class UserProfileForm(BaseProfileForm):
    class Meta:
        model = UserProfile
        fields = ('image', 'bio')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        user_fields = Layout(
            Field('image', css_class='form-control rounded-2 p-2'),
            Field('bio', css_class='form-control rounded-2 p-2', placeholder='Tell us a bit about yourself'),
        )
        
        self.append_fields(user_fields)
