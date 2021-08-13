
# Points for point map:
# ((a, b, c, d), (e, f, g, h), (i, j, k, l))
# a  e  i
# b  f  j
# c  g  k
# d  h  l

class Triangle:
    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    def isPointInside(self, p):
        def area(p1,p2,p3):
            return abs((p1[0]*(p2[1]-p3[1])+(p2[0]*(p3[1]-p1[1]))+(p3[0]*(p1[1]-p2[1])))/2.0)
        A = area(self.p1, self.p2, self.p3)
        A1 = area(p, self.p2, self.p3)
        A2 = area(self.p1, p, self.p3)
        A3 = area(self.p1, self.p2, p)
        return A1 + A2 + A3 - A < 0.001
    
    def intepolateZ(self, p):
        w1 = (((self.p2[1] - self.p3[1]) * (p[0] - self.p3[0]) +
                (self.p3[0] - self.p2[0]) * (p[1] - self.p3[1])) /
               ((self.p2[1] - self.p3[1]) * (self.p1[0] - self.p3[0]) + 
                (self.p3[0] - self.p2[0]) * (self.p1[1] - self.p3[1])))
        w2 = (((self.p3[1] - self.p1[1]) * (p[0] - self.p3[0]) +
                (self.p1[0] - self.p3[0]) * (p[1] - self.p3[1])) /
               ((self.p2[1] - self.p3[1]) * (self.p1[0] - self.p3[0]) + 
                (self.p3[0] - self.p2[0]) * (self.p1[1] - self.p3[1])))
        w3 = 1.0 - w1 - w2
        return self.p1[2] * w1 + self.p2[2] * w2 + self.p3[2] * w3

class TriangleMap:
    # points: the points from above. The constructor adds fake points.
    def __init__(self, points):
        self.triangles = []
        # 1) Add fake points
        fakePoints = [[None] * (len(points[0]) + 2) for _ in range((len(points) + 2))]
        for i in range(len(fakePoints)):
            for j in range(len(fakePoints[0])):
                adjI = i
                adjX = 0
                if i == 0:
                    adjX = -1000
                    adjI = 1
                elif i == len(fakePoints) - 1:
                    adjX = 1000
                    adjI = len(points)
                adjJ = j
                adjY = 0
                if j == 0:
                    adjJ = 1
                    adjY = -1000
                elif j == len(fakePoints[0]) - 1:
                    adjJ = len(points[0])
                    adjY = +1000
                fakePoints[i][j] = [x for x in points[adjI - 1][adjJ - 1]]
                fakePoints[i][j][0] += adjX
                fakePoints[i][j][1] += adjY
        # print(fakePoints)
        for i in range(len(fakePoints) - 1):
            for j in range(len(fakePoints[0]) - 1):
                self.triangles.append(Triangle(fakePoints[i][j],
                                               fakePoints[i][j + 1],
                                               fakePoints[i + 1][j]))
                self.triangles.append(Triangle(fakePoints[i + 1][j + 1],
                                               fakePoints[i + 1][j],
                                               fakePoints[i][j + 1]))
    
    def getZ(self, x, y):
        for t in self.triangles:
            if t.isPointInside([x, y]):
                # print(f"{x},{y} is in {t.p1},{t.p2},{t.p3}")
                return t.intepolateZ([x, y])
        for _ in range(10):
            print(f"BAAAAAAAAAAAD: No triangles found for point {x} {y}")



# t = TriangleMap([
#     [[1,1,0],[1,2,0],[1,5,0]],
#     [[2,1,0],[2,2,0],[2,5,0]],
#     [[5,1,0],[5,2,0],[5,5,0]],
#     [[9,1,0],[9,2,0],[9,4,0]]
# ])

# t = Triangle([0, 0, 0], [1, 0, 100], [0, 1, -10])
# print(t.isPointInside([0.5, 0.1, 0]))

# t = TriangleMap([
#     [[-1,-1,-100],[-1,1,0]],
#     [[1,-1,50],[1,1,0]]
# ])

# print(t.getZ(-1, -1))
# print(t.getZ(-2, -2))
# print(t.getZ(0, -2))
# print(t.getZ(0, 0))
# print(t.getZ(-1002, -1))