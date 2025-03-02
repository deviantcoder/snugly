from django.contrib.auth import get_user_model

from accounts.forms import BaseAppUserCreationForm, BaseProfileForm
from accounts.models import MentorProfile

from crispy_forms.layout import Layout, Field


User = get_user_model()


class MentorCreationForm(BaseAppUserCreationForm):
    """
    Form for creating new mentor users with the MENTOR role. Inherits from BaseAppUserCreationForm.
    Methods:
        save(commit=True): Saves the user instance with an additional role attribute.
    """

    role = User.Roles.MENTOR

    def __init__(self, *args, **kwargs):
        super().__init__(*args, form_action='mentors:register_mentor', **kwargs)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class MentorProfileForm(BaseProfileForm):
    form_url_name = 'mentors:edit_profile'

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
