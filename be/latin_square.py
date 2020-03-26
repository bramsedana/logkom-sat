from pysat.solvers import Glucose3

def construct_var(x, y, z):
    return (x+1) * 100 + (y+1) * 10 + (z+1)

# input: matrix of int(? for now)
# output: boolean
def lat_square_sat(mat):
    g = Glucose3()

    assumption = []
    size = len(mat)
    for x in range(size):
        for y in range(size):
            val = mat[x][y]
            clause1 = []
            clause2 = []
            clause3 = []
            for z in range(size):
                var1 = construct_var(x, y, z)
                var2 = construct_var(x, z, y)
                var3 = construct_var(z, x, y)
                clause1.append(var1)
                clause2.append(var2)
                clause3.append(var3)
                if val == z:
                    assumption.append(var1)
                else:
                    assumption.append(-var1)

            g.add_clause(clause1)
            g.add_clause(clause2)
            g.add_clause(clause3)

    return g.solve(assumptions=assumption)

print(lat_square_sat([[1,2,3],[3,1,2],[2,3,1]]))
print(lat_square_sat([[1,1,1],[1,1,1],[1,1,1]]))
