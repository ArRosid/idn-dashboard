class TrainingType:
    choices = (
        (0, "Training Offline"),
        (1, "Training Online"),
        (2, "Bootcamp"),
        (3, "Premium Webinar"),
        (4, "Free Webinar"),
    )


class RegistrationStatus:
    not_paid = 0
    choices = ((0, "Not Paid"), (1, "Wait for Confirm"), (2, "Paid"))


class Month:
    choices = (
        (1, "Januari"),
        (2, "Februari"),
        (3, "Maret"),
        (4, "April"),
        (5, "Mei"),
        (6, "Juni"),
        (7, "Juli"),
        (8, "Agustus"),
        (9, "September"),
        (10, "Oktober"),
        (11, "November"),
        (12, "Desember"),
    )
