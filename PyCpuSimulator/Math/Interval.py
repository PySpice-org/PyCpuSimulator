####################################################################################################
#
# PyCpuSimulator - AVR Simulator
# Copyright (C) 2015 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################

# Fixme: use https://github.com/FabriceSalvaire/python-arithmetic-interval

""" This module implements interval arithmetic.
"""

####################################################################################################

__ALL__ = ['Interval',
           'IntervalInt',
           'IntervalIntSupOpen',
           'Interval2D',
           'Interval2DInt',
           ]

####################################################################################################

import math
import sys

####################################################################################################

from .Functions import middle

####################################################################################################

Nan = float('nan')
FloatMinusInfinity = float('-inf')
FloatPlusInfinity = float('+inf')
IntMinusInfinity = sys.maxsize
IntPlusInfinity = -sys.maxsize

####################################################################################################

class Interval:

    """ Interval [inf, sup] in the float domain.

    An interval can be constructed using a couple (inf, sup) or an object that support the
    :meth:`__getitem__` interface::

      Interval(inf, sup)
      Interval((inf, sup))
      Interval(iterable)
      Interval(interval)

    To get the interval boundaries, use the :attr:`inf` and :attr:`sup` attribute.

    An empty interval is defined with *inf* and *sup* set to :obj:`None`.

    To compute the union of two intervals use:

      i3 = i1 | i2
      i1 |= i2

    To compute the intersection of two intervals use:

      i3 = i1 & i2
      i1 &= i2

    It returns an empty interval if the intersection is null.
    """

    __empty_interval_string__ = '[empty]'

    ##############################################

    def __init__(self, *args, **kwargs):

        self.inf, self.sup = self._check_arguments(args)

        self._left_open = kwargs.get('left_open', False)
        self._right_open = kwargs.get('right_open', False)
        # if self.inf == FloatMinusInfinity:
        #     self.left_open = True
        # if self.sup == FloatPlusInfinity:
        #     self.right_open = True

    ##############################################

    def _check_arguments(self, args):

        # Fixme: cast to float()?

        size = len(args)
        if size == 1:
            array = args[0]
            # Fixme: more check?
            #   and len(array) == 2
            inf, sup = array[:2] # will call __getitem__(slice(None, 2, None))
        elif size == 2:
            inf, sup = args
        else:
            raise ValueError("Too many arguments")

        if inf > sup: # None > None = False
            raise ValueError("inf <= sup constraint isn't true [%g, %g]" % (inf, sup))

        return inf, sup

    ##############################################

    def copy(self):

        """ Return a clone of the interval. """

        return self.__class__(self.inf, self.sup)

    #: alias of :meth:`copy`
    clone = copy

    ##############################################

    def __getitem__(self, index):

        """ Provide an indexing interface.

        The parameter *index* can be a location from 0 to 1 or a slice. The location 0 corresponds
        to *inf* and 1 to *sup*, respectively.
        """

        if isinstance(index, slice):
            start = 0 if index.start is None else index.start
            stop = 2 if index.stop is None else index.stop
            # Fixme: check index.step
            if start == 0 and stop == 2:
                return self.inf, self.sup
            elif start == 0 and stop == 1:
                return self.inf
            elif start == 1 and stop == 2:
                return self.sup
            else:
                raise IndexError("Wrong " + str(index))
        elif index == 0:
            return self.inf
        elif index == 1:
            return self.sup
        else:
            raise IndexError("Out of range index")

    ##############################################

    @property
    def left_open(self):
        return self.inf == FloatMinusInfinity or self._left_open

    @property
    def right_open(self):
        return self.sup == FloatPlusInfinity or self._right_open

    ##############################################

    def __repr__(self):

        return str(self.__class__) + ' ' + str(self)

    ##############################################

    def __str__(self):

        """ Return a textual representation of the interval. """

        if self.is_empty():
            return self.__empty_interval_string__
        else:
            s = ']' if self.left_open else '['
            s += '%g, %g' % (self.inf, self.sup)
            s += '[' if self.right_open else ']'
            return s

    ##############################################

    def is_empty(self):

        """ Test if the interval is empty. """

        return self.inf is None and self.sup is None

   ##############################################

    def zero_length(self):

        """ Return ``sup == inf``. """

        return self.sup == self.inf

    ##############################################

    def length(self):

        """ Return ``sup - inf``. """

        return self.sup - self.inf

    ##############################################

    def middle(self):

        """ Return the interval's middle. """

        return middle(self.inf, self.sup)

    ##############################################

    def __eq__(i1, i2):

        """ Test if the intervals are equal. """

        return i1.inf == i2.inf and i1.sup == i2.sup

    ##############################################

    def __lt__(i1, i2):

        """ Test if ``i1.sup < i2.inf``. """

        return i1.sup < i2.inf

    ##############################################

    def __gt__(i1, i2):

        """ Test if ``i1.inf > i2.sup``. """

        return i1.inf > i2.sup

    ##############################################

    def __iadd__(self, dx):

        """ Shift the interval of *dx*. """

        self.inf += dx
        self.sup += dx
        return self

    ##############################################

    def __add__(self, dx):

        """ Return a new interval shifted of *dx*. """

        return self.__class__((self.inf + dx,
                               self.sup + dx))

    ##############################################

    def enlarge(self, dx):

        """ Enlarge the interval of *dx*. """

        self.inf -= dx
        self.sup += dx

        return self

    ##############################################

    def __isub__(self, dx):

        """ Shift the interval of -*dx*. """

        self.inf -= dx
        self.sup -= dx
        return self

    ##############################################

    def __sub__(self, dx):

        """ Return a new interval shifted of -*dx*. """

        return self.__class__((self.inf - dx,
                               self.sup - dx))

    ##############################################

    def __mul__(self, scale):

        """ Return a new interval scaled by *scale*. """

        return self.__class__((self.inf * scale,
                               self.sup * scale))

    ##############################################

    def __contains__(self, x):

        """ Test if *x* is in the interval? """

        return self.inf <= x <= self.sup

   ###############################################

    def intersect(i1, i2):

        """ Test whether the interval intersects with i2? """

        return i1.inf <= i2.sup and i2.inf <= i1.sup

    ##############################################

    def is_included_in(i1, i2):

        """ Test whether the interval is included in i1? """

        return i2.inf <= i1.inf and i1.sup <= i2.sup

    ##############################################

    def is_outside_of(i1, i2):

        """ Test whether the interval is outside of i2? """

        return i1.inf < i2.inf or i2.sup < i1.sup

    ##############################################

    @staticmethod
    def _intersection(i1, i2):

        """ Compute the intersection of *i1* and *i2*. """

        if i1.intersect(i2):
            return (max((i1.inf, i2.inf)),
                    min((i1.sup, i2.sup)))
        else:
            return None, None

    ##############################################

    def __and__(i1, i2):

        """ Return the intersection of *i1* and *i2*.

        Return an empty interval if they don't intersect.
        """

        return i1.__class__(i1._intersection(i1, i2))

    ##############################################

    def __iand__(self, i2):

        """ Update the interval with its intersection with *i2*.

        Return an empty interval if they don't intersect.
        """

        self.inf, self.sup = self._intersection(self, i2)
        return self

    ##############################################

    @staticmethod
    def _union(i1, i2):

        """ Compute the union of *i1* and *i2*. """

        return (min((i1.inf, i2.inf)),
                max((i1.sup, i2.sup)))

    ##############################################

    def __or__(i1, i2):

        """ Return the union of *i1* and *i2*. """

        return i1.__class__(i1._union(i1, i2))

    ##############################################

    def __ior__(self, i2):

        """ Update the interval with its union with *i2*. """

        self.inf, self.sup = self._union(self, i2)
        return self

    ##############################################

    def map_in(self, interval_reference):

        """ Return a new interval shifted of *interval_reference.inf*. """

        return self - interval_reference.inf

    ##############################################

    def map_x_in(self, x, clamp=False):

        """ Return ``x - inf``. If *clamp* parameter is set True then the value is clamped in the
        interval.
        """

        x = int(x) # Fixme: why int?
        if clamp:
            if x <= self.inf:
                return 0
            elif x >= self.sup:
                x = self.sup
        return x - self.inf

    ##############################################

    def unmap_x_in(self, x):

        """ Return ``x + inf``. """

        return x + self.inf

####################################################################################################

class IntervalInt(Interval):

    """ Interval [inf, sup] in the integer domain.
    """

    ##############################################

    def __init__(self, *args, **kwargs):

        self.inf, self.sup = [int(x) if x is not None else None
                              for x in self._check_arguments(args)]

        self._left_open = kwargs.get('left_open', False)
        self._right_open = kwargs.get('right_open', False)
        # if self.inf == IntMinusInfinity:
        #     self.left_open = True
        # if self.sup == IntPlusInfinity:
        #     self.right_open = True

    ##############################################

    @property
    def left_open(self):
        return self.inf == IntMinusInfinity or self._left_open

    @property
    def right_open(self):
        return self.sup == IntPlusInfinity or self._right_open

    ##############################################

    def __str__(self):

        """ Return a textual representation of the interval. """

        if self.is_empty():
            return self.__empty_interval_string__
        else:
            s = ']' if self.left_open else '['
            s += '-oo' if self.inf == IntMinusInfinity else str(self.inf)
            s += ', '
            s += '+oo' if self.sup == IntPlusInfinity else str(self.sup)
            s += '[' if self.right_open else ']'
            return s

    ##############################################

    def length(self):

        """ Return ``sup - inf +1``. """

        return self.sup - self.inf +1

    ##############################################

    def length_float(self):

        """ Return ``sup - inf``. """

        return self.sup - self.inf

    ##############################################

    def to_slice(self):

        """ Return a slice instance. """

        return slice(self.inf, self.sup +1)

####################################################################################################

class IntervalIntSupOpen(IntervalInt):

    """ Interval [inf, sup[ in the integer domain.
    """

    ##############################################

    def __init__(self, *args):

        super(IntervalIntSupOpen, self).__init__(*args, left_open=False, right_open=True)

    ##############################################

    def intersect(i1, i2):

        """ Does the interval intersect with *i2*? """

        return i1.inf < i2.sup and i2.inf < i1.sup

   ###############################################

    def minus(i1, i2):

        # Fixme: unused

        """ Return a list of intervals corresponding to i1 - intersection of i1 and i2. If i2 is
        included in i1 then two intervals can be returned. If the compution is not defined then
        :obj:`None` is returned.
        """

        if i1.intersect(i2):
            if i1.is_included_in(i2):
                return None # IntervalIntSupOpen(None, None)
            elif i2.is_included_in(i1):
                r = []
                if i1.inf != i2.inf:
                    r.append(IntervalIntSupOpen(i1.inf, i2.inf))
                if i2.sup != i1.sup:
                    r.append(IntervalIntSupOpen(i2.sup, i1.sup))
                return tuple(r)
            elif i1.inf <= i2.inf:
                return (IntervalIntSupOpen(i1.inf, i2.inf),)
            else:
                return (IntervalIntSupOpen(i2.sup, i1.sup),)
        else:
            return None # IntervalIntSupOpen(None, None)

    ##############################################

    def exclude(i1, i2):

        """ Compute the subset intervals of *i1* given an exclusion interval *i2*.

        It returns :obj:`None` if the intervals don't intersect or *i1* is included in *i2*.  Else
        it returns a list of couples (interval, excluded_flag) where *interval* is a subset of the
        interval *i1* and *excluded_flag* indicated if the subset is excluded.
        """

        if i1.intersect(i2):
            if i1.is_included_in(i2):
                return None
            elif i2.is_included_in(i1):
                r = []
                if i1.inf != i2.inf:
                    r.append((IntervalIntSupOpen(i1.inf, i2.inf), True))
                r.append((i2, False))
                if i2.sup != i1.sup:
                    r.append((IntervalIntSupOpen(i2.sup, i1.sup), True))
                return tuple(r)
            elif i1.inf <= i2.inf: # I1 < I2
                return ((IntervalIntSupOpen(i1.inf, i2.inf), True),
                        (i2, False))
            else: # I2 < I1
                return ((i2, False),
                        (IntervalIntSupOpen(i2.sup, i1.sup), True))
        else:
            return None

#################################################################################

class Interval2D:

    """ Interval [inf, sup]*[inf, sup] in the float domain.

    The components can be accessed using the :attr:`x` and :attr:`y` attribute, or using an index
    interface where the index 0 maps to *x* and 1 to *y*, respectively.
    """

    ##############################################

    def __init__(self, x, y):

        self.x = Interval(x)
        self.y = Interval(y)

    ##############################################

    def copy(self):

        """ Return a clone of the interval. """

        return self.__class__(self.x, self.y)

    #: alias of :meth:`copy`
    clone = copy

    ##############################################

    def __setitem__(self, index, interval):

        if index == 0:
            self.x = interval
        elif index == 1:
            self.y = interval
        else:
            raise IndexError("Out of range index")

    ##############################################

    def __getitem__(self, index):

        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError("Out of range index")

    ##############################################

    def __str__(self):

        """ Return a textual representation of the interval. """

        return str(self.x) + '*' + str(self.y)

    ##############################################

    def __repr__(self):

        return str(self.__class__) + ' ' + str(self)

    ##############################################

    def bounding_box(self):

        """ Return the corresponding bounding box ``(x.inf, y.inf, x.sup, y.sup)``. """

        return (self.x.inf, self.y.inf,
                self.x.sup, self.y.sup)

    ##############################################

    def is_empty(self):

        """ Test if the interval is empty. """

        return self.x.is_empty() or self.y.is_empty()

    ##############################################

    def size(self):

        """ Return the horizontal and vertical length. """

        return self.x.length(), self.y.length()

    ##############################################

    def area(self):

        """ Return the area. """

        return self.x.length() * self.y.length()

    ##############################################

    def diagonal(self):

        """ Return the diagonal's length. """

        return math.sqrt((self.x.length())**2 + (self.y.length())**2)

    ##############################################

    def middle(self):

        """ Return the interval's middle. """

        return self.x.middle(), self.y.middle()

    ##############################################

    def __eq__(i1, i2):

        """ Test whether the intervals are equal. """

        return i1.x == i2.x and i1.y == i2.y

    ##############################################

    def __iadd__(self, dxy):

        """ Shift the interval of *dxy*. """

        self.x += dx
        self.y += dy
        return self

    ##############################################

    def __add__(self, dxy):

        """ Return a new interval shifted by *dxy*. """

        return self.__class__(self.x + dxy[0], self.y  + dxy[1])

    ##############################################

    def shift(self, dx, dy):

        """ Shift the interval of (dx, dy). """

        self.x += dx
        self.y += dy
        return self

    ##############################################

    def enlarge(self, dx):

        """ Enlarge the interval of dx. """

        self.x.enlarge(dx)
        self.y.enlarge(dx)

        return self

    ##############################################

    def __imul__(self, scale):

        """ Scale the interval by *scale*. """

        self.x *= scale
        self.y *= scale
        return self

    ##############################################

    def __mul__(self, scale):

        """ Return a new interval scaled by *scale*. """

        return self.__class__(self.x * scale, self.y * scale)

    ##############################################

    def intersect(self, i2):

        """ Test whether the interval intersects with i2? """

        return (self.x.intersect(i2.x) and self.y.intersect(i2.y))

    ##############################################

    def is_included_in(self, i2):

        """ Test whether the interval is included in i2? """

        return (self.x.is_included_in(i2.x) and self.y.is_included_in(i2.y))

    ##############################################

    def __and__(i1, i2):

        """ Return the intersection of *i1* and *i2*.

        Return an empty interval if they don't intersect.
        """

        return i1.__class__(i1.x & i2.x, i1.y & i2.y)

    ##############################################

    def __iand__(self, i2):

        """ Update the interval with its intersection with *i2*.

        Return an empty interval if they don't intersect.
        """

        self.x &= i2.x
        self.y &= i2.y
        return self

    ##############################################

    def __or__(i1, i2):

        """ Return the union of *i1* and *i2*. """

        return i1.__class__(i1.x | i2.x, i1.y | i2.y)

    ##############################################

    def __ior__(self, i2):

        """ Update the interval with its union with *i2*. """

        self.x |= i2.x
        self.y |= i2.y
        return self

    ##############################################

    def map_in(self, interval_reference):

        """ Construct a new interval shifted of *interval_reference.inf*. """

        return self.__class__(self.x.map_in(interval_reference.x),
                              self.y.map_in(interval_reference.y))

    ##############################################

    def map_xy_in(self, x, y, clamp=False):

        """ Return ``(x - y.inf, y - y.inf)``. """

        return (self.x.map_x_in(x, clamp),
                self.y.map_x_in(y, clamp))

    ##############################################

    def unmap_xy_in(self, x, y):

        """ Return ``(x + y.inf, y + y.inf)``. """

        return (self.x.unmap_x_in(x),
                self.y.unmap_x_in(y))

####################################################################################################

class IntervalInt2D(Interval2D):

    """ Interval [inf, sup]*[inf, sup] in the integer domain.
    """

    ##############################################

    def __init__(self, x, y):

        self.x = IntervalInt(x)
        self.y = IntervalInt(y)
