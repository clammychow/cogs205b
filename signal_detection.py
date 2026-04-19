import scipy.stats

class SignalDetection:
    def __init__(self, hits, misses, false_alarms, correct_rejections):
        for i in (hits, misses, false_alarms, correct_rejections):
            if not isinstance(i, int) or isinstance(i, bool):
                raise TypeError("Outcome counts must be integers")
            elif i < 0:
                raise ValueError("Outcome counts cannot be negative")
        self.hits = hits
        self.misses = misses
        self.false_alarms = false_alarms
        self.correct_rejections = correct_rejections

    # core methods
    def hit_rate(self):
        if self.hits + self.misses == 0:
            raise ValueError("Hit Rate undefined: hits and misses add to 0")
        return self.hits / (self.hits + self.misses)
    def false_alarm_rate(self):
        if self.false_alarms + self.correct_rejections == 0:
            raise ValueError("False Alarm Rate undefined: false alarms and correct rejections add to 0")
        return self.false_alarms / (self.false_alarms + self.correct_rejections)
    def d_prime(self):
        return scipy.stats.norm.ppf(self.hit_rate()) - scipy.stats.norm.ppf(self.false_alarm_rate())
    def criterion(self):
        return -0.5 * (scipy.stats.norm.ppf(self.hit_rate()) + scipy.stats.norm.ppf(self.false_alarm_rate()))
    
    # operator overloading
    def __add__(self, other):
        if not isinstance(other, SignalDetection):
            raise TypeError("Both objects must be of the SignalDetection class")
        return SignalDetection(self.hits + other.hits, 
        self.misses + other.misses,
        self.false_alarms + other.false_alarms, 
        self.correct_rejections + other.correct_rejections)

    def __sub__(self, other):
        if not isinstance(other, SignalDetection):
            raise TypeError("Both objects must be of the SignalDetection class")
        return SignalDetection(self.hits - other.hits, 
        self.misses - other.misses,
        self.false_alarms - other.false_alarms, 
        self.correct_rejections - other.correct_rejections)

    def __mul__(self, factor):
        if not isinstance(factor, int) or isinstance(factor, bool):
            raise TypeError("Factor must be an integer")
        return SignalDetection(self.hits * factor,
        self.misses * factor,
        self.false_alarms * factor,
        self.correct_rejections * factor)