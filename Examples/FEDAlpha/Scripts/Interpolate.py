from bisect import bisect_left

class LinearInterpolation(object):
    """ Linear interpolation with optional extrapolation.  """
    def __init__(self, x, y):
        # sanity check
        x_length = len(x)
        y_length = len(y)

        if x_length < 2 or y_length < 2:
            raise ValueError("Arrays must have at least 2 values")
        if x_length != y_length:
            raise ValueError("Arrays must have same length")
        if any(x2 - x1 <= 0 for x1, x2 in zip(x, x[1:])):
            raise ValueError("x must be in strictly ascending order!")

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

      # print('x is: ', x)
      # print('y is: ', y)
      # print('x1 is: ', x1)
      # print('x2 is: ', x2)
      # print('y1 is: ', y1)
      # print('y2 is: ', y2)
      # print('input is: ', input)
      # print('result is: ' , (y1*(x2-input) + y2*(input-x1)) / (x2-x1))

      return (y1*(x2-input) + y2*(input-x1)) / (x2-x1)  
  
# from: https://github.com/pmav99/interpolation/blob/master/interpolation/bilinear.py
# but removed non-extrapolating version (broken) and reversed z12 and z21 in calculations to fix transposed results
class BilinearInterpolation(object):
    """ Bilinear interpolation with optional extrapolation.  """
    def __init__(self, x_index, y_index, values):
        # sanity check
        x_length = len(x_index)
        y_length = len(y_index)

        if x_length < 2 or y_length < 2:
            raise ValueError("Table must be at least 2x2.")
        if y_length != len(values):
            raise ValueError("Table must have equal number of rows to y_index.")
        if any(x2 - x1 <= 0 for x1, x2 in zip(x_index, x_index[1:])):
            raise ValueError("x_index must be in strictly ascending order!")
        if any(y2 - y1 <= 0 for y1, y2 in zip(y_index, y_index[1:])):
            raise ValueError("y_index must be in strictly ascending order!")

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