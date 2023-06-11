"""Sort example."""


class Factory:
    """Create an instance with factory and delivery date attributes."""

    def __init__(self, factory: str, delivery_date: int):
        self.delivery_date = delivery_date
        self.factory = factory

    def __repr__(self) -> str:
        """Return str representation of class attributes."""
        return f"Tool({self.delivery_date}, {self.factory})\n"


factories = [
    Factory("forge_works", 20240321),
    Factory("forge_works", 20240323),
    Factory("forge_works", 20240322),
    Factory("meltdown_manufacturing", 20240323),
    Factory("forge_works", 20240321),
    Factory("radiant_rims", 20240321),
    Factory("radiant_rims", 20240322),
    Factory("radiant_rims", 20240321),
    Factory("meltdown_manufacturing", 20240321),
    Factory("meltdown_manufacturing", 20240321),
]

priority_mapping = {
    "forge_works": 2,
    "meltdown_manufacturing": 0,
    "radiant_rims": 1,
}

factories.sort(key=lambda x: (x.delivery_date, priority_mapping[x.factory]))
print(factories)
