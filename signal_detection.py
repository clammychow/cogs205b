import scipy.stats

class SignalDetection:
    def __init__(hits, misses, false_alarms, correct_rejections):
        self.hits = hits
        self.misses = misses
        self.false_alarms = false_alarms
        self.correct_rejections = correct_rejections
    def hit_rate(self):
        return self.hits / (self.hits + self.misses)
    def false_alarm_rate(self):
        return self.false_alarms / (self.false_alarms + self.correct_rejections)
    def d_prime(self):
        return scipy.stats.norm.ppf(self.hit_rate) - scipy.stats.norm.ppf(self.false_alarm_rate)
    def criterion(self):
        return -0.5 * (scipy.stats.norm.ppf(self.hit_rate) + scipy.stats.norm.ppf(self.false_alarm_rate))
    