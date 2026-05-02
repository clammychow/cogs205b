import scipy.stats
import scipy.integrate

class BayesFactor:
    def __init__(self, n, k):
        if not isinstance(n, int) or isinstance(n, bool):
            raise TypeError("n must be an integer")
        elif not isinstance(k, int) or isinstance(k, bool):
            raise TypeError("k must be an integer")
        elif k < 0 or n < 0:
            raise ValueError("Inputs cannot be negative")
        elif k > n:
            raise ValueError("k cannot be larger than n [Double check input order: BayesFactor(n, k)]")
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

    def bayes_factor(self):
        if self.evidence_slab() == 0:
            raise ValueError("Bayes Factor undefined; slab evidence ≈ 0")
        return self.evidence_spike() / self.evidence_slab()