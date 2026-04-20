import scipy.stats
import matplotlib.pyplot as plt

class SignalDetection:
    def __init__(self, hits, misses, false_alarms, correct_rejections):
        for count in (hits, misses, false_alarms, correct_rejections):
            if not isinstance(count, int) or isinstance(count, bool):
                raise TypeError("Outcome counts must be integers")
            elif count < 0:
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
            raise TypeError("All objects must be of the SignalDetection class")
        return SignalDetection(self.hits + other.hits, 
        self.misses + other.misses,
        self.false_alarms + other.false_alarms, 
        self.correct_rejections + other.correct_rejections)

    def __sub__(self, other):
        # negative results handled by ValueError in __init__
        if not isinstance(other, SignalDetection):
            raise TypeError("All objects must be of the SignalDetection class")
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

    # ROC plot
    @staticmethod
    def plot_roc(sdt_list):
        if not isinstance(sdt_list, list):
            raise TypeError("Enter a list of SignalDetection objects")
        for sdt in sdt_list:
            if not isinstance(sdt, SignalDetection):
                raise TypeError("Cannot plot non-SignalDetection objects")

        # creates lists of x and y values using sdt rates
        hr_list = []
        far_list = []
        for sdt in sdt_list:
            hr_list.append(sdt.hit_rate())
            far_list.append(sdt.false_alarm_rate())

        # Adds endpoints and orders by hit rate
        roc_points = list(zip(hr_list, far_list))
        roc_points.extend([(0, 0), (1, 1)])
        sorted_points = sorted(roc_points)
        hr_list, far_list = zip(*sorted_points)

        # creates and returns figure with hit rate on horizontal axis
        fig, ax = plt.subplots()
        ax.plot(hr_list, far_list)
        ax.set_title("Receiver Operating Characteristics Curve")
        ax.set_xlabel("Hit Rates")
        ax.set_ylabel("False Alarm Rates")
        return fig, ax