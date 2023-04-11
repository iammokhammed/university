from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


def file_path(instance, filename):
    return f"{instance.user.username}/{filename}"


class Profile(models.Model):
    ROLE = (
        (0, "Student"),
        (1, "Teacher")
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to=file_path)
    bio = models.TextField()
    role = models.IntegerField(choices=ROLE, default=0)

    def __str__(self):
        if self.user.get_full_name():
            return self.user.get_full_name()
        return self.user.username


def user_post_save(instance, sender, created, *args, **kwargs):
    if created:
        Profile.objects.create(user_id=instance.id)


post_save.connect(user_post_save, sender=User)



