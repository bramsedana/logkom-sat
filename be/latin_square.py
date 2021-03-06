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
            for z in range(size):
                var1 = construct_var(x, y, z)
                if val == 0:
                    continue
                if val == z+1:
                    assumption.append(var1)
                else:
                    assumption.append(-var1)

            for a in range(size-1):
                var1 = construct_var(a,x,y)
                var3 = construct_var(x,a,y)
                for b in range(a+1, size):
                    clause1 = []
                    clause2 = []
                    var2 = construct_var(b,x,y)
                    var4 = construct_var(x,b,y)
                    clause1.append(-var1)
                    clause1.append(-var2)
                    clause2.append(-var3)
                    clause2.append(-var4)
                    g.add_clause(clause1)
                    g.add_clause(clause2)

    return g.solve(assumptions=assumption)

# Example to use
# print(lat_square_sat([[1,2,3],[3,1,2],[2,3,1]]))
# print(lat_square_sat([[1,1,1],[1,1,1],[1,1,1]]))
