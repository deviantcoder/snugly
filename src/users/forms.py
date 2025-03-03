from accounts.forms import BaseAppUserCreationForm, BaseProfileForm
from accounts.models import UserProfile

from crispy_forms.layout import Layout, Field

from django.contrib.auth import get_user_model


User = get_user_model()


class UserCreationForm(BaseAppUserCreationForm):
    """
    Form for creating regular users with the USER role. Inherits from BaseAppUserCreationForm.
    Methods:
        save(commit=True): Saves the user instance with an additional role attribute.
    """

    role = User.Roles.USER

    def __init__(self, *args, **kwargs):
        super().__init__(*args, form_action='users:register_user', **kwargs)

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