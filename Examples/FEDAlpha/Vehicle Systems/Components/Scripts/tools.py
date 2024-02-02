"""
This module contains some basic functions for use inside various scripts
"""

from bisect import bisect_left
import math

# ------------------------------------------------------------------------------
# Field creation functions
#
def create_output(extension, name, o_type, default_value=None):
    """Create output field with optional default value, reset on every simulation run."""
    if extension.getOutput(name) is None:
        extension.addOutput(name, o_type)
    if default_value is not None:
        extension.getOutput(name).value = default_value
    return extension.getOutput(name)

def create_parameter(extension, name, p_type, default_value=None):
    """Create parameter field with optional default value set only when the field is created."""
    if extension.getParameter(name) is None:
        field = extension.addParameter(name, p_type)
        if default_value is not None:
            field.value = default_value
    return extension.getParameter(name)

def create_input(extension, name, i_type, default_value=None):
    """Create input field with optional default value set only when the field is created."""
    if extension.getInput(name) is None:
        field = extension.addInput(name, i_type)
        if default_value is not None:
            field.value = default_value
    return extension.getInput(name)


# ------------------------------------------------------------------------------
# Mathematical functions
#
def clamp(value, min_value, max_value):
    """Return a bounded value."""
    return min(max(value, min_value), max_value)


def lowpass_filter(extension, input_signal, output_signal, time_constant):
    """Apply a low-pass filter to a signal."""
    delta_time = extension.getApplicationContext().getSimulationTimeStep()
    value = (((delta_time * input_signal) + (time_constant * output_signal))
             / (delta_time + time_constant))
    return value

    
class Timer(object):
    """Counts down the specified amount of time.

    To use it, create a timer with the countdown_time and time_step values set. time_remaining 
    starts at 0, and restart() must be called to set the time_remaining to countdown_time. 

    update() is called to increment the timer, so it should be called once every step.

    Returns true while the timer is counting, and false when it reaches 0"""

    def __init__(self, countdown_time, time_step=1.0/60.0):
        self.countdown_time = countdown_time
        self.time_step = time_step
        self.time_remaining = 0.0

    def restart(self):
        self.time_remaining = self.countdown_time

    def update(self):
        self.time_remaining = max(self.time_remaining - self.time_step, 0.0)

    def __call__(self):
        return self.time_remaining > 0.0


class LinearInterpolation(object):
    """ Linear interpolation with extrapolation.  """
    def __init__(self, x, y):
        # sanity check
        x_length = len(x)
        y_length = len(y)

        if x_length < 2 or y_length < 2:
            raise ValueError("Arrays must have at least 2 values")
        if x_length != y_length:
            raise ValueError("Arrays must have same length")
        if any(x2 - x1 <= 0 for x1, x2 in zip(x, x[1:])):
            raise ValueError("x must be in ascending order")

        self.x = x
        self.y = y
        self.x_length = x_length
        self.y_length = y_length

    def __call__(self, input):
        # local lookups
        x, y = self.x, self.y

        i = max(min(bisect_left(x, input) - 1, self.x_length - 2), 0)

        x1, x2 = x[i:i+2]
        y1, y2 = y[i:i+2]

        return (y1*(x2-input) + y2*(input-x1)) / (x2-x1)
# ------------------------------------------------------------------------------

# Based on script from: https://github.com/pmav99/interpolation/blob/master/interpolation/bilinear.py
# Removed non-extrapolating version (broken) and reversed z12 and z21 in calculations to fix transposed results
class BilinearInterpolation(object):
    """ Bilinear interpolation with extrapolation.  """
    def __init__(self, x_index, y_index, values):
        # sanity check
        x_length = len(x_index)
        y_length = len(y_index)

        if x_length < 2 or y_length < 2:
            raise ValueError("Table must be at least 2x2")
        if x_length != len(values[0]):
            raise ValueError("Table must have equal number of columns to x_index")
        if y_length != len(values):
            raise ValueError("Table must have equal number of rows to y_index")
        if any(x2 - x1 <= 0 for x1, x2 in zip(x_index, x_index[1:])):
            raise ValueError("x_index must be in ascending order")
        if any(y2 - y1 <= 0 for y1, y2 in zip(y_index, y_index[1:])):
            raise ValueError("y_index must be in ascending order")

        self.x_index = x_index
        self.y_index = y_index
        self.values = values
        self.x_length = x_length
        self.y_length = y_length

    def __call__(self, x, y):
        # local lookups
      x_index, y_index, values = self.x_index, self.y_index, self.values

      i = bisect_left(x_index, x) - 1
      j = bisect_left(y_index, y) - 1

      if i == -1:
          x_slice = slice(None, 2)
      elif i == self.x_length - 1:
          x_slice = slice(-2, None)
      else:
          x_slice = slice(i, i + 2)
      # fix y index
      if j == -1:
          j = 0
          y_slice = slice(None, 2)
      elif j == self.y_length - 1:
          j = -2
          y_slice = slice(-2, None)
      else:
          y_slice = slice(j, j + 2)

      x1, x2 = x_index[x_slice]
      y1, y2 = y_index[y_slice]
      
      z11, z21 = values[j][x_slice]
      z12, z22 = values[j + 1][x_slice]

      return (z11 * (x2 - x) * (y2 - y) +
         z21 * (x - x1) * (y2 - y) +
         z12 * (x2 - x) * (y - y1) +
         z22 * (x - x1) * (y - y1)) / ((x2 - x1) * (y2 - y1))

