from rest_framework.throttling import UserRateThrottle


class RateThrottle(UserRateThrottle):
    scope = 'rate'


class SourceThrottle(UserRateThrottle):
    scope = 'source'
