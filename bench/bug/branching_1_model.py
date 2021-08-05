class Wrapper_for_Model:
    def run(self):
        self._latcnt = 0
        self._obscnt = 0
        return self.Model()

    def Model(self):
        if True:
            _temp_1 = ()
        else:
            _temp_1 = ()
        self._latcnt += 1
        r = pyro.sample("lat_" + str(self._latcnt), dist.Poisson(4.00000000))
        if (4 < r):
            l = 6
        else:
            self._latcnt += 1
            t = pyro.sample("lat_" + str(self._latcnt), dist.Poisson(4.00000000))
            _temp_0 = fib((3 * r))
            l = (t + _temp_0)
        self._obscnt += 1
        y = pyro.sample("obs_" + str(self._obscnt), dist.Poisson(l))
        return r
