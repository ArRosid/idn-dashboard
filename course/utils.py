import os


def upload_bukti_pembayaran(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s_%s.%s" % (
        instance.user.email,
        instance.registration.training.name,
        ext,
    )
    return os.path.join("bukti_pembayaran/", filename)
