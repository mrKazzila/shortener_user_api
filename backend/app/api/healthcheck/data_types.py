from dataclasses import dataclass


@dataclass(frozen=True)
class HealthcheckStatus:
    status: str = 'ok'


OK_STATUS = HealthcheckStatus()
