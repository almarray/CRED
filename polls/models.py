from django.db import models

class Pompe(models.Model):
    """Represente une pompe, une pompe a un statut courant et un journal d'historique du statut."""
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=2, unique=True)
    gpio = models.IntegerField(default=0)

    @classmethod
    def get_by_gpio(self, gpio):
        return self.objects.get(gpio=gpio)

    @classmethod
    def get_by_code(self, code):
        return self.objects.get(code=code)

    def status_log(self):
        """ Returns the query set of the given statuses"""
        return self.status_set.all().order_by("-date")

    def current_status(self):
        """The current status is represented by the last status occured in time."""
        return self.status_set.latest('date')

    def __str__(self):
        return str(self.name)


class Status(models.Model):
    """Represente le statut d'une pompe selon un log."""
    pompe = models.ForeignKey(Pompe, on_delete=models.CASCADE)

    # Status codes.
    HORS_FUNCTION = 'HS'
    OK = 'OK'
    DEFAULT = 'KO'
    ACK = 'ACK'
    ALERT = 'AL'
    ALERT_ACK = 'ALA'

    # Existing states
    ETATS = (
        (HORS_FUNCTION, 'Hors function'),
        (OK, 'OK'),
        (DEFAULT, 'Défaut'),
        (ACK, 'Défaut acquitté'),
        (ALERT, 'Alerte'),
        (ALERT_ACK, 'Alerte acquitté')
    )

    # field etat.
    etat = models.CharField(
        max_length=3,
        choices=ETATS,
        default=OK
    )
    # Datetime of the event
    date = models.DateTimeField('date', auto_now=True)

    def __str_(self):
        return str(self.etat) + " at " + self.date.strftime("%Y-%m-%d %H:%M:%S")
