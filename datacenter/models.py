from django.db import models
from django.utils.timezone import localtime


SECONDS_IN_MINUTE = 60
SECONDS_IN_HOUR = 3600


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )


def format_duration(duration):
    total_seconds = int(duration)
    hours = total_seconds // SECONDS_IN_HOUR
    minutes = (total_seconds % SECONDS_IN_HOUR) // SECONDS_IN_MINUTE
    secs = total_seconds % SECONDS_IN_MINUTE
    duration_in_format = f'{hours} ч. {minutes} мин. {secs} с.'
    return duration_in_format


def get_duration(visit):
    entered_at = localtime(visit.entered_at)
    if visit.leaved_at is None:
        finished_at = localtime().replace(microsecond=0)
    else:
        finished_at = localtime(visit.leaved_at)
    duration = finished_at - entered_at
    return duration.total_seconds()


def is_visit_long(visit, minutes=60):
    return get_duration(visit) >= minutes * SECONDS_IN_MINUTE
