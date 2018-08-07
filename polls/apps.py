from django.apps import AppConfig
from polls.models import Pompe, Status

try:
    import RPi.GPIO as GPIO
except (ImportError, RuntimeError):
    0

class PollsConfig(AppConfig):
    name = 'polls'

    def ready(self):
        """ Code executed on qpplicqtion start. """
        self.config()
        if self.is_on_rpi:
            # Set on stqrtup status right away.
            self.get_status()
            # Set monitoring.
            self.start_monitoring()


    def start_monitoring(self):
        for input in self.INPUTS:
            GPIO.add_event_detect(input, GPIO.BOTH, callback=self.set_status_callback, bouncetime=200)


    def set_status_callback(self, channel):
        """
        :param channel:
        :return:
        """
        from .models import Pompe, State
        p = Pompe.get_by_gpio(channel)
        current_state = p.current_state().state
        measured_state = bool(GPIO.input(channel))

        if current_state != current_state:
            new_state = State(pompe=p, state=measured_state)
            new_state.save()

    

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
                GPIO.setup(input, GPIO.IN)
            for output in self.OUTPUTS:
                GPIO.setup(output, GPIO.OUT)
