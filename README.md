# CIEColorDiff
##Colorimetric difference calculator

Comparing colors scientifically is more difficult than one might expect, especially when
taking human perception into account, which is interisting for works of art.

This code was specifically created for my son's degree project for MSc in conservation.
The code in main.py is very specific for that project assuming colorimetric measurements
given as PDF documents.

The code in ciecolor.py however implements a class for holding data about a CIE color.
Its diff method takes another Ciecolor as argument and performs the algorithm described in 

_The CIEDE2000 Color-Difference Formula: Implementation Notes, Supplementary Test Data, 
and Mathematical Observations" by
Gaurav Sharma, Wencheng Wu and Edul N. Dalal, accepted 15 April 2004 
and published by COLOR research and application Volume 30, Number 1, February 2005_

to return the $\{Delta}E_{00}^*$ difference between the object's color and the other object's color.
