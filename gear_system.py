from typing import Optional, Union, Any


class Wheel:
    def __init__(self, rim: float, tire: float) -> None:
        self.rim: float = rim
        self.tire: float = tire

    # incoming query
    def diameter(self) -> float:
        return self.rim + (self.tire * 2)


class Observer:
    def changed(self) -> None:
        # Simulate side effects like saving to DB
        pass


class Gear:
    def __init__(
            self,
            chainring: float = None,
            cog: float = None,
            wheel: Wheel = None
    ) -> None:
        self.chainring: float = chainring
        self.cog: float = cog
        self.wheel: Wheel = wheel
        self.observer  =  Observer()

    # incoming query (w/ sent-to-self & outgoing query)
    def gear_inches(self) -> float:
        if self.wheel is None:
            raise ValueError("Wheel is not set")
        return self._ratio() * self.wheel.diameter()

    # incoming command (w/ sent-to-self w/ outgoing command)
    def set_cog(self, new_cog: float) -> None:
        self.cog = new_cog
        self.observer.changed()

    def _ratio(self) -> float:
        if self.chainring is None or self.cog is None:
            raise ValueError("Chainring and cog must be set")
        return self.chainring / float(self.cog)

    # def _changed(self) -> None:
    #     if self.observer is not None:
    #         self.observer.changed(self.chainring, self.cog)
