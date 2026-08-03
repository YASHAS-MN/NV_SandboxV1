from sandbox.sensors import (
    Sensor,
    SensorManager,
)


calls = []


class SensorA(Sensor):

    @property
    def name(self):
        return "A"

    @property
    def priority(self):
        return 20

    def before_execution(self):
        calls.append("A-before")

    def after_execution(self):
        calls.append("A-after")


class SensorB(Sensor):

    @property
    def name(self):
        return "B"

    @property
    def priority(self):
        return 10

    def before_execution(self):
        calls.append("B-before")

    def after_execution(self):
        calls.append("B-after")


manager = SensorManager()

manager.register(SensorA())
manager.register(SensorB())

assert manager.sensors[0].name == "B"
assert manager.sensors[1].name == "A"

manager.before_execution()
manager.after_execution()

assert calls == [

    "B-before",
    "A-before",

    "B-after",
    "A-after",

]

print("SensorManager OK")
