from be.latin_square import *

print(lat_square_sat([[1, 1, 0], [0, 0, 0], [0, 0, 0]]))
print(lat_square_sat([[1, 0, 0], [1, 0, 0], [0, 0, 0]]))
print(lat_square_sat([[1, 2, 3], [1, 0, 0], [0, 0, 0]]))
print(lat_square_sat([[1, 2, 3], [3, 1, 2], [2, 3, 1]]))
print(lat_square_sat([[1, 2, 3], [3, 1, 2], [2, 3, 0]]))
