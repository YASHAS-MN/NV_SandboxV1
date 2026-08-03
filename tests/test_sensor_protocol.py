from sandbox.sensors import Sensor


class DummySensor(Sensor):

    @property
    def name(self):
        return "dummy"


sensor = DummySensor()

assert sensor.name == "dummy"

assert sensor.priority == 100

sensor.before_execution()

sensor.after_execution()

print("Sensor protocol OK")
