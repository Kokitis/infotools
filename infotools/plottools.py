from typing import *

import matplotlib.pyplot as plt

from infotools import numbertools


def hr_labels(ax: plt.Axes, which: Literal['x', 'y', 'xy', 'both'] = 'y') -> plt.Axes:
	""" Converts numerical values into a human-friendly format.
		Parameters
		----------
		ax:plt.Axes
			The ax object that needs to be modified.
		which: Literal['x', 'y', 'xy', 'both']; default 'y'
			Specifies which axis to modify.
		Returns
		-------
		plt.Axes
			The modified ax object.
	"""
	if which in {'x', 'xy', 'both'}:
		x_ticks = ax.xaxis.get_majorticklocs()
		x_labels = [numbertools.human_readable(i) for i in x_ticks]
		ax.set_xticklabels(x_labels)

	if which in {'y', 'xy', 'both'}:
		y_ticks = ax.yaxis.get_majorticklocs()
		y_labels = [numbertools.human_readable(i) for i in y_ticks]
		ax.set_yticklabels(y_labels)

	return ax
