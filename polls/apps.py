from django.apps import AppConfig
from polls.models import Pompe, Status

try:
    import RPi.GPIO as GPIO
except (ImportError, RuntimeError):
    0

class PollsConfig(AppConfig):
    name = 'polls'

    # Configure GPIO inputs in the following array.
    # Setup your inputs here and outputs here.
    INPUTS = [24, 7, 14, 11, 23]
    OUTPUTS = [8]


    def ready(self):
        self.config()
        if self.is_on_rpi:
            # Set on stqrtup status right away.
            self.get_status()
            # Set monitoring.
            self.start_monitoring()


    def get_status(self):
        """
        Get the initial status of the IO at startup.
        """
        if self.is_on_rpi:
            for input in self.INPUTS:
                p = Pompe.get_by_gpio(input)
                s = Status(pompe=p)
                if GPIO.input(input) == 0:
                    s.etat = Status.OK
                else:
                    s.etat = Status.DEFAULT
                s.save()


    def config(self):
        """
        Configure RPi to actually run correctly
        :return:
        """
        self.is_on_rpi = False
        try:
            import RPi.GPIO as GPIO
            self.is_on_rpi = True
        except (ImportError, RuntimeError):
            self.is_on_rpi = False

        if self.is_on_rpi:
            GPIO.setmode(GPIO.BOARD)
            for input in self.INPUTS:
                GPIO.setup(input, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            for output in self.OUTPUTS:
                GPIO.setup(output, GPIO.OUT)