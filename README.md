task 1


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


task 3 

class Product(BaseModel):
    encrypted_price = models.BinaryField(null=True, blank=True)
    encrypted_marja = models.BinaryField(null=True, blank=True)
    encrypted_package_code = models.BinaryField(null=True, blank=True)

  
    key = b'16 byte key12345'  

    def encrypt_field(self, field_value):
        cipher = AES.new(self.key, AES.MODE_EAX)
        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(field_value.encode('utf-8'))
        return nonce + ciphertext + tag

    def decrypt_field(self, encrypted_field):
        nonce = encrypted_field[:16]
        ciphertext = encrypted_field[16:-16]
        tag = encrypted_field[-16:]
        cipher = AES.new(self.key, AES.MODE_EAX, nonce)
        decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
        return decrypted_data.decode('utf-8')

    @property
    def price(self):
        return self.decrypt_field(self.encrypted_price)

    @price.setter
    def price(self, value):
        self.encrypted_price = self.encrypt_field(str(value))

    @property
    def marja(self):
        return self.decrypt_field(self.encrypted_marja)

    @marja.setter
    def marja(self, value):
        self.encrypted_marja = self.encrypt_field(str(value))

    @property
    def package_code(self):
        return self.decrypt_field(self.encrypted_package_code)

    @package_code.setter
    def package_code(self, value):
        self.encrypted_package_code = self.encrypt_field(value)

task 4

class Team(BaseModel):
    title = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    coach = models.CharField(max_length=100)

    team_created = models.DateField()

    def __str__(self):
        return self.title

class Player(BaseModel):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    title = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100)
    position = models.CharField(max_length=100)

    age = models.PositiveIntegerField(default=0)
    goals_scored = models.PositiveIntegerField(default=0)
    assists = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
    
class ResultChoice(models.TextChoices):
    HOME = 'Home win'
    AWAY = 'Away win'
    DRAW = 'Draw'

class Match(BaseModel):
    home_team = models.ForeignKey(Team, related_name='home_matches', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='away_matches', on_delete=models.CASCADE)

    date = models.DateField()

    stadium = models.CharField(max_length=100)
    result = models.CharField(max_length=10, choices=ResultChoice.choices)

    def __str__(self):
        return self.home_team.title

class Championship(BaseModel):
    title = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    starting = models.DateField()
    ending = models.DateField()

    def __str__(self):
        return self.title