from rest_framework.throttling import AnonRateThrottle


class CustomAnonRateThrottle(AnonRateThrottle):
    rate = '2/minute'


class CustomCreatorRateThrottle(AnonRateThrottle):
    rate = '5/minute'
