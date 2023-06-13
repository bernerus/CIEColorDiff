from math import *

# CIE color computation
# Copyright Christer Bernérus 2022, 2023
# License: GPL2

class Ciecolor:
	def __init__(self, name, hdeg, cstar, bstar, astar, lstar):
		self.hdeg = hdeg
		self.cstar = cstar
		self.bstar = bstar
		self.astar = astar
		self.lstar = lstar
		self.name = name

	def __str__(self):
		s = "%s: %s, %s, %s, %s, %s" % (self.name, self.hdeg, self.astar, self.bstar, self.cstar, self.lstar)
		return s

	def diff(self, other, kl=1, kc=1, kh=1):
		# CIEDE2000 color difference formula, implemented according to the article
		# "The CIEDE2000 Color-Difference Formula: Implementation Notes, Supplementary Test Data, and Mathematical Observations" by
		# Gaurav Sharma, Wencheng Wu and  Edul N. Dalal, accepted 15 April 2004 and published by COLOR research and application Volume 30, Number 1, February 2005

		# Eq 2
		cstar1ab = sqrt(self.astar * self.astar + self.bstar * self.bstar)
		cstar2ab = sqrt(other.astar * other.astar + other.bstar * other.bstar)

		# Eq 3
		cstarvec = (cstar1ab + cstar2ab) / 2

		# Eq 4
		g = 0.5 * (1 - sqrt(cstarvec ** 7 / (cstarvec ** 7 + 25 ** 7)))

		# Eq 5
		a1prim = (1 + g) * self.astar
		a2prim = (1 + g) * other.astar

		# Eq 6
		c1prim = sqrt(a1prim * a1prim + self.bstar * self.bstar)
		c2prim = sqrt(a2prim * a2prim + other.bstar * other.bstar)

		# Eq 7
		h1prim = 0 if self.bstar == 0 and a1prim == 0 else atan2(self.bstar, a1prim) * 180 / pi
		h2prim = 0 if other.bstar == 0 and a2prim == 0 else atan2(other.bstar, a2prim) * 180 / pi
		if h1prim < 0:
			h1prim += 360
		if h2prim < 0:
			h2prim += 360

		# Eq 8
		deltaLprim = other.lstar - self.lstar

		# Eq 9
		deltacprim = c2prim - c1prim

		# Eq 10
		if c1prim * c2prim == 0:
			deltahprim = 0
		elif fabs(h2prim - h1prim) <= 180:
			deltahprim = h2prim - h1prim
		elif h2prim - h1prim > 180:
			deltahprim = (h2prim - h1prim) - 360
		elif h2prim - h1prim < -180:
			deltahprim = (h2prim - h1prim) + 360
		else:
			raise ValueError("Cannot find angle difference")

		# eq 11
		deltaHprim = 2 * sqrt(c1prim * c2prim) * sin(pi / 180 * deltahprim / 2)

		# Eq 12

		lprimvec = (self.lstar + other.lstar) / 2

		# Eq 13
		cprimvec = (c1prim + c2prim) / 2

		# Eq 14
		if c1prim * c2prim == 0:
			hprimvec = (h1prim + h2prim)
		elif fabs(h1prim - h2prim) <= 180:
			hprimvec = (h1prim + h2prim) / 2
		elif fabs(h1prim - h2prim) > 180 and (h1prim + h2prim) < 360:
			hprimvec = (h1prim + h2prim + 360) / 2
		elif fabs(h1prim - h2prim) > 180 and (h1prim + h2prim) >= 360:
			hprimvec = (h1prim + h2prim - 360) / 2
		else:
			raise ValueError("Cannot find vector angle difference")

		# Eq 15
		t = 1 - 0.17 * cos((hprimvec - 30) * pi / 180) + 0.24 * cos((2 * hprimvec) * pi / 180) + 0.32 * cos((3 * hprimvec + 6) * pi / 180) - 0.20 * cos((4 * hprimvec - 63) * pi / 180)

		# Eq 16
		deltatheta = 30 * exp(-(((hprimvec - 275) / 25) ** 2))

		# Eq 17
		rc = 2 * sqrt(cprimvec ** 7 / (cprimvec ** 7 + 25 ** 7))

		# Eq 18
		sl = 1 + (0.015 * (lprimvec - 50) ** 2) / sqrt(20 + (lprimvec - 50) ** 2)

		# Eq 19
		sc = 1 + 0.045 * cprimvec

		# Eq 20
		sh = 1 + 0.015 * cprimvec * t

		# Eq 21
		rt = -sin(2 * deltatheta * pi / 180) * rc

		# Eq 22
		deltaE0012 = sqrt((deltaLprim / (kl * sl)) ** 2 + (deltacprim / (kc * sc)) ** 2 + (deltaHprim / (kc * sh)) ** 2 + rt * (deltacprim / (kc * sc)) * (deltaHprim / (kh * sh)))

		return deltaE0012

	def diff76(self, other):

		deltaE76 = sqrt((other.lstar-self.lstar)**2 + (other.astar-self.astar)**2 + (other.bstar-self.bstar)**2)
		return deltaE76


