from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(choices=(("V", "Vendedor"), ("G", "Gerente")))
    avatar = models.ImageField(upload_to="perfil")
    code = models.CharField(max_length=50, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.code = f"{self.user.username if self.user.username else ''}{self.role}{self.user.id}"  # type: ignore
        super().save(*args, **kwargs)
