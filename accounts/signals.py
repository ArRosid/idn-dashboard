from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User, Profile
from accounts.utils import randomStringAffiliateID


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, affiliate_id=randomStringAffiliateID(8))

    instance.profile.save()
