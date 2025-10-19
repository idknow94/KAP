from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
import random


AVATAR_CHOICES = [
    ('avatar1.png', 'Avatar 1'),
    ('avatar2.png', 'Avatar 2'),
    ('avatar3.png', 'Avatar 3'),
    ('avatar4.png', 'Avatar 4'),
]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    avatar = models.CharField(
        max_length=50, choices=AVATAR_CHOICES, default=random.choice([choice[0] for choice in AVATAR_CHOICES]))
    tokens = models.IntegerField(default=3)  # posting tokens per week
    last_reset = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def can_post(self):
        """Return True if user still has posting tokens."""
        self.reset_tokens_if_needed()
        return self.tokens > 0

    def use_token(self):
        """Decrement a posting token when a new issue is posted."""
        self.reset_tokens_if_needed()
        if self.tokens > 0:
            self.tokens -= 1
            self.save()

    def reset_tokens_if_needed(self):
        """Reset weekly posting tokens every 7 days."""
        if timezone.now() - self.last_reset > timedelta(days=7):
            self.tokens = 3
            self.last_reset = timezone.now()
            self.save()


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
