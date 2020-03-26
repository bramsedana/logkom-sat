from pysat.solvers import Glucose3

def construct_var(x, y, z):
    return (x+1) * 100 + (y+1) * 10 + (z+1)

# input: matrix of int(? for now)
# output: boolean
def lat_square_sat(mat):
    g = Glucose3()

    size = len(mat)
    for x in range(size):
        for y in range(size):
            val1 = mat[x][y]
            clause1 = []
            clause2 = []
            clause3 = []
            for z in range(size):
                var1 = construct_var(x, y, z)
                if val1 == z:
                    clause1.append(var1)
                else:
                    clause1.append(-var1)
                
                val2 = mat[x][z]
                var2 = construct_var(x, z, y)
                if val2 == y:
                    clause2.append(var2)
                else:
                    clause2.append(-var2)

                val3 = mat[z][x]
                var3 = construct_var(z, x, y)
                if val3 == y:
                    clause3.append(var3)
                else:
                    clause3.append(-var3)
            g.add_clause(clause1)
            g.add_clause(clause2)
            g.add_clause(clause3)

    print(g.get_model())
    return g.solve()

print(lat_square_sat([[1,2,3],[3,1,2],[2,3,1]]))
print(lat_square_sat([[1,1,1],[1,1,1],[1,1,1]]))
