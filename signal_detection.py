class SignalDetection:
    def __init__(hits, misses, false_alarms, correct_rejections):
        self.hits = hits
        self.misses = misses
        self.false_alarms = false_alarms
        self.correct_rejections = correct_rejections
    def hit_rate(self):
        return self.hits / (self.hits + self.misses)