from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **kwargs):
        """
            Create and saves user with the given email & password
        """
        if not email:
            ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **kwargs):
        kwargs.setdefault("is_superuser", False)
        return self._create_user(email, password, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_staff", True)

        if kwargs.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self._create_user(email, password, **kwargs)
