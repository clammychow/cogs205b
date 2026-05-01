import scipy.stats
import scipy.integrate

class BayesFactor:
    def __init__(self, n, k):
        self.n = n
        self.k = k
    
    def likelihood(self, theta):
        if not isinstance(theta, (float, int)) or isinstance(theta, bool):
            raise TypeError("Theta must be an integer or float")
        elif not 0 <= theta and theta <= 1:
            raise ValueError("Theta must be within the range [0, 1]")
        return scipy.stats.binom.pmf(self.k, self.n, theta)

    def evidence_slab(self):
        integral, error = scipy.integrate.quad(self.likelihood, 0, 1)
        return integral

    def evidence_spike(self):
        a = 0.4999
        b = 0.5001
        function = lambda theta: self.likelihood(theta) * 1/(b - a)
        integral, error = scipy.integrate.quad(function, a, b)
        return integral

    #def bayes_factor(self):