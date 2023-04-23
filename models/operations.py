from .schemas import Trade

__all__ = ("TradeRead")

class TradeRead(Trade):
    def dict(self, **kwargs):
        print(self, kwargs)
        d = super().dict(**kwargs)
        return d