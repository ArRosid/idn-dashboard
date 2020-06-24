import os
from django.core.exceptions import ValidationError


def max_file_size_2m(value):
    limit = 2 * 1024 * 1024
    if value.size > limit:
        raise ValidationError("File too large. Size should not exceed 2 MiB.")


def upload_bukti_pembayaran(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s_%s.%s" % (
        instance.user.email,
        instance.registration.training.name,
        ext,
    )
    return os.path.join("bukti_pembayaran/", filename)
