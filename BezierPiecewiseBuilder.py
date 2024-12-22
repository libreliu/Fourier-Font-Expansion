import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import sympy.plotting as sym_plot

from ExampleInputSpline import exampleInputSpline

class BezierPiecewiseBuilder:
    def __init__(self):
        self.beziers = []

    def pushBezier(self, p0, p1, p2, p3):
        """Append a bezier curve"""
        self.beziers.append({
            'p': [p0, p1, p2, p3]
        })
    
    def _cubicBezierCurve(self, p0, p1, p2, p3, t):
        return (1 - t)**3 * p0 + 3 * (1 - t)**2 * t * p1 + 3 * (1 - t) * t**2 * p2 + t**3 * p3

    def _directEvalAll(self, nPerSegment=5):
        """Evaluate splines to points with uniform sampling"""
        numSplines = len(self.beziers)
        points = np.ndarray((nPerSegment * numSplines, 2))
        for idx, spline in enumerate(self.beziers):
            for segmentIdx in range(nPerSegment):
                t = segmentIdx / (nPerSegment - 1)

                points[idx * nPerSegment + segmentIdx, 0] =  self._cubicBezierCurve(
                    spline['p'][0][0],
                    spline['p'][1][0],
                    spline['p'][2][0],
                    spline['p'][3][0],
                    t
                )

                points[idx * nPerSegment + segmentIdx, 1] =  self._cubicBezierCurve(
                    spline['p'][0][1],
                    spline['p'][1][1],
                    spline['p'][2][1],
                    spline['p'][3][1],
                    t
                )

        
        return points
    
    def plotSegments(self, nPerSegment=5):
        """Plot the segment in the builder using matplotlib"""
        points = self._directEvalAll(nPerSegment)

        # Plot the Bézier curve
        plt.figure(figsize=(8, 6))
        plt.plot(points[:, 0], points[:, 1], 'b-')
        plt.show()

    def toSympyFunction(self):
        """Parameterize to [0, 2 pi] using sympy for the whole curve, returns matrix repr; may not C_0"""
        numBeziers = len(self.beziers)

        t = sp.Symbol('t')
        pi = sp.pi
        bezierPiecewiseExprs = []
        for idx, desc in enumerate(self.beziers):
            bezierPiecewiseExprs.append((
                self._cubicBezierCurve(
                    sp.Matrix(desc['p'][0]),
                    sp.Matrix(desc['p'][1]),
                    sp.Matrix(desc['p'][2]),
                    sp.Matrix(desc['p'][3]),
                    numBeziers * t / (2 * pi) - idx
                ),
                sp.And(t >= 2 * pi * idx / numBeziers, t < 2 * pi * (idx + 1) / numBeziers)
            ))
        
        return (t, sp.Piecewise(*bezierPiecewiseExprs, (sp.Matrix([0, 0]), True)))
    
    def toSympyFunctionComponentized(self):
        """Parameterize to [0, 2 pi] using sympy but returns (t, x(t), y(t)); not C_0"""
        numBeziers = len(self.beziers)

        t = sp.Symbol('t')
        pi = sp.pi
        bezierPiecewiseExprs = [[], []]
        for idx, desc in enumerate(self.beziers):
            for coordIdx in range(2):
                bezierPiecewiseExprs[coordIdx].append((
                    self._cubicBezierCurve(
                        desc['p'][0][coordIdx],
                        desc['p'][1][coordIdx],
                        desc['p'][2][coordIdx],
                        desc['p'][3][coordIdx],
                        numBeziers * t / (2 * pi) - idx
                    ),
                    sp.And(t >= 2 * pi * idx / numBeziers, t < 2 * pi * (idx + 1) / numBeziers)
                ))
        
        return (
            t,
            sp.Piecewise(*bezierPiecewiseExprs[0], (0, True)),
            sp.Piecewise(*bezierPiecewiseExprs[1], (0, True))
        )
    
    @staticmethod
    def testPlot():
        builder = BezierPiecewiseBuilder()

        for spline in exampleInputSpline:
            bezierPoints = spline['bezier_points']
            numPoints = len(bezierPoints)
            for i in range(numPoints):
                p0 = bezierPoints[i % numPoints]['coordinates'][:2]
                p1 = bezierPoints[i % numPoints]['handle_right'][:2]
                p2 = bezierPoints[(i+1) % numPoints]['handle_left'][:2]
                p3 = bezierPoints[(i+1) % numPoints]['coordinates'][:2]

                builder.pushBezier(p0, p1, p2, p3)

        builder.plotSegments()

    @staticmethod
    def testReturnF():
        builder = BezierPiecewiseBuilder()

        for spline in exampleInputSpline:
            bezierPoints = spline['bezier_points']
            numPoints = len(bezierPoints)
            for i in range(numPoints):
                p0 = bezierPoints[i % numPoints]['coordinates'][:2]
                p1 = bezierPoints[i % numPoints]['handle_right'][:2]
                p2 = bezierPoints[(i+1) % numPoints]['handle_left'][:2]
                p3 = bezierPoints[(i+1) % numPoints]['coordinates'][:2]

                builder.pushBezier(p0, p1, p2, p3)

        
        t, funcx, funcy = builder.toSympyFunctionComponentized()
        return (t, funcx, funcy)

    @staticmethod
    def testSympyComponentized():
        """Plot an f"""
       
        t, funcx, funcy = BezierPiecewiseBuilder.testReturnF()
        funcx.evalf(subs={t: 0})
        sym_plot.plot_parametric((funcx, funcy), (t, 0, 2 * 3.14), n=1000)
        # sp.print_glsl(func)
        # ts = np.linspace(0, 2*np.pi, 100)
        # values = []
        # for tval in ts:
        #     values.append((
        #         funcx.evalf(subs={t: tval}),
        #         funcy.evalf(subs={t: tval}),
        #     ))
        # values = np.asarray(values)
        # plt.figure(figsize=(8, 6))
        # plt.plot(values[:, 0], values[:, 1], 'b-')
        # plt.show()
        

        # builder.plotSegments()

if __name__ == '__main__':
    BezierPiecewiseBuilder.testPlot()
    BezierPiecewiseBuilder.testSympyComponentized()