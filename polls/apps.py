from django.apps import AppConfig

try:
    import RPi.GPIO as GPIO
except (ImportError, RuntimeError):
    0

class PollsConfig(AppConfig):
    name = 'polls'

    def ready(self):
        """ Code executed on qpplicqtion start. """
        self.is_on_rpi = False
        try:
            import RPi.GPIO as GPIO
            self.is_on_rpi = True
        except (ImportError, RuntimeError):
            self.is_on_rpi = False
        if self.is_on_rpi:
            print("Initialization sequence...")
            self.config()

    def set_status_callback(self, channel):
        """
        :param channel:
        :return:
        """
        from .models import Pompe, State
        print("IO change detected on " + str(channel) + " - " + str(GPIO.input(channel)))
        p = Pompe.get_by_gpio(channel)
        current_state = p.current_state().state
        measured_state = bool(GPIO.input(channel))

        if current_state != measured_state:
            new_state = State(pompe=p, state=measured_state)
            new_state.save()

    

    def config(self):
        """
        Configure RPi to actually run correctly
        :return:
        """
        print("Start config : " + str(self.is_on_rpi) )
        if self.is_on_rpi:
            from .models import Pompe, State
            GPIO.setmode(GPIO.BCM)
            pompes = Pompe.objects.all()
            for p in pompes:
                print("Configuring : " + str(p.name) + " (" + str(p.gpio) + ")")
                GPIO.setup(p.gpio, GPIO.IN)
                # Initialize state
                new_state = State(pompe=p, state=bool(GPIO.input(p.gpio)))
                new_state.save()
                GPIO.add_event_detect(p.gpio, GPIO.BOTH, callback=self.set_status_callback, bouncetime=200)