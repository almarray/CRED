from django.test import TestCase
from django.utils import timezone
from .models import Pompe, Status

class PompeStatusTest(TestCase):

    def test_create_models(self):
        """ Test model behaviour"""
        pompe = Pompe(name="Pompe bas", code="PB")
        pompe.save()
        status = Status(etat=Status.ACK)
        status.pompe = pompe
        status.save()
        self.assertIsNotNone(status.date) # !! date is set when the object is saved no before.
        status2 = Status(etat=Status.DEFAULT)
        status2.pompe = pompe
        status2.save()

        # Check getting the list of statuses.
        self.assertIs(pompe.status_set.count(), 2)
        self.assertIs(str(pompe),"Pompe bas")
        self.assertTrue(pompe.status_log().ordered)
        self.assertIsNotNone(pompe.current_status())
        self.assertEqual(pompe.current_status().etat, Status.DEFAULT)