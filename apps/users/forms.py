from django.contrib.auth.forms import UserCreationForm

from apps.users.models import User


class CreationForm(UserCreationForm):
    """
    New user form.
    """
    class Meta(UserCreationForm.Meta):
        """
        Use :model:'User'.
        With fields 'title', 'username', 'email'.
        """
        model = User
        fields = ('title', 'username', 'email')
