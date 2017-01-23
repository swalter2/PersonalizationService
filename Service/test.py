# -*- coding: utf-8 -*-

#from events import Event

#event = Event()

#event.get_events(['Fußball','Handball','Reiten','Musik','Sport'])

import matplotlib.pyplot as plt
import numpy as np

arr = np.random.random((1000,))

from learning import analyze_score_distribution

analyze_score_distribution(arr, "test")