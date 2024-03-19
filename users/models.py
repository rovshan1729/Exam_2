from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models


class User(AbstractUser):
    """
    Default custom user model for My Awesome Project.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    image = models.ImageField(upload_to='media/profile/', blank=True, null=True)

    bio = models.TextField()

    is_deleted = models.BooleanField(default=False)

    def delete(self):
        self.is_deleted = True
        self.save()

    def save(self, *args, **kwargs):
        if self.is_deleted:
            self.is_active = False
            self.save()
        super().save(*args, **kwargs)


    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
