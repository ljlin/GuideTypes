#!/usr/bin/env python3

import torch
import pyro
import pyro.distributions as dist
from pyro.infer import EmpiricalMarginal, Importance
from greenlet import greenlet
import time

def timeit(f, *args, **kwargs):
    t1 = time.time_ns()
    ret = f(*args, **kwargs)
    t2 = time.time_ns()
    return (ret, t2 - t1)


def test(cond_model, guide):
    importance = Importance(model=cond_model, guide=guide, num_samples=10000)
    emp_dist = EmpiricalMarginal(importance.run())


def fib(n):
    a, b = 1, 1
    i = 0
    while i < n:
        i = i + 1
        a, b = b, a + b
    return a

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
        if True:
            self._ctrl_p.switch(True)
            _temp_1 = ()
        else:
            self._ctrl_p.switch(False)
            _temp_1 = ()
        r = self._ctrl_p.switch()
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
        if self._last_b:
            self._ctrl_m.switch()
            _temp_4 = ()
        else:
            self._ctrl_m.switch()
            _temp_4 = ()
        self._latcnt += 1
        _temp_3 = pyro.sample("lat_" + str(self._latcnt), dist.Geometric(0.50000000))
        self._last_b = self._ctrl_m.switch(_temp_3)
        if self._last_b:
            self._ctrl_m.switch()
            return ()
        else:
            self._ctrl_m.switch()
            self._latcnt += 1
            _temp_2 = pyro.sample("lat_" + str(self._latcnt), dist.Geometric(0.50000000))
            self._last_b = self._ctrl_m.switch(_temp_2)
            return ()

def model():
    wm = Wrapper_for_Model()
    return wm.run()


def guide():
    pm = Proposal_for_Model()
    pm.run()

cond_model = pyro.condition(model, data={"obs_1": torch.tensor(6.0)})

_, gi = timeit(test, cond_model, guide)
print("generated code inference time: %fs" % (gi / 1e9))

"""
Traceback (most recent call last):
  ...
  ...
  ...
  File "GuideTypes/bench/bug/branching_1_test.py", line 113, in guide
    pm.run()
  File "GuideTypes/bench/bug/branching_1_test.py", line 65, in run
    return self._ctrl_m.switch()
TypeError: _wrap_p() takes 0 positional arguments but 1 was given
"""