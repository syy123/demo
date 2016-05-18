# -*- coding: utf-8 -*-
"""
Created on Tue May 17 17:36:26 2016

@author: Administrator
"""

import numpy as np
import pylab as pl

x = np.ones(100)
y = x * 5;
r = "$\
      {H_{RC}}(f) = \left\{ \
       \begin{array}{ll} \
       1 & 0 \le |f| \le \cfrac{1-\alpha}{2T_s}  \\ \
       \cfrac{1}{2}\left[1 + \sin\left(\cfrac{\pi}{2\alpha}-\cfrac{\pi T_s}{\alpha}|f|\right)\right] & \cfrac{1-\alpha}{2T_s} < |f| \le \cfrac{1+\alpha}{2T_s}  \\ \
       0  & |f| > \cfrac{1+\alpha}{2T_s} \
       \end{array}\
     \right.\
    $"
r2=r'\begin{displaymath}H(f)=2T_s cos\pi fT_s \, , \; |f| \leq \frac{1}{2T_s}\end{displaymath}'
r1 = r'$cosx$' 
pl.plot(x,y, label = r2)
pl.legend()
pl.show()