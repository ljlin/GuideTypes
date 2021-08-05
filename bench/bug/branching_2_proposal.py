class Proposal_for_Model:
    def run(self):
        self._latcnt = 0
        self._obscnt = 0
        def _wrap_m():
            return self.Model()
        def _wrap_p():
            return self.Proposal()
        self._ctrl_m = greenlet(_wrap_m)
        self._ctrl_p = greenlet(_wrap_p)
        self._last_b = None
        return self._ctrl_m.switch()

    def Model(self):
        r = self._ctrl_p.switch()
        if True:
            self._ctrl_p.switch(True)
            _temp_1 = ()
        else:
            self._ctrl_p.switch(False)
            _temp_1 = ()
        if (4 < r):
            self._ctrl_p.switch(True)
            l = 6
        else:
            self._ctrl_p.switch(False)
            t = self._ctrl_p.switch()
            _temp_0 = fib((3 * r))
            l = (t + _temp_0)
        self._obscnt += 1
        return r

    def Proposal(self):
        self._latcnt += 1
        _temp_4 = pyro.sample("lat_" + str(self._latcnt), dist.Geometric(0.50000000))
        self._last_b = self._ctrl_m.switch(_temp_4)
        if self._last_b:
            self._ctrl_m.switch()
            _temp_3 = ()
        else:
            self._ctrl_m.switch()
            _temp_3 = ()
        if self._last_b:
            self._ctrl_m.switch()
            return ()
        else:
            self._ctrl_m.switch()
            self._latcnt += 1
            _temp_2 = pyro.sample("lat_" + str(self._latcnt), dist.Geometric(0.50000000))
            self._last_b = self._ctrl_m.switch(_temp_2)
            return ()
