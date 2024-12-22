from BezierPiecewiseBuilder import BezierPiecewiseBuilder

# used for testing
import sympy.plotting as sym_plot
import matplotlib.pyplot as plt

import numpy as np
import math
import dataclasses

from sympy.printing.numpy import NumPyPrinter

@dataclasses.dataclass
class FourierSeriesTerm:
    n: int
    Real: float
    Imag: float

@dataclasses.dataclass
class FourierSeries:
    terms: dict

    def plot(self):
        nSamples = len(series.terms) * 5 + 5
        t_vals = np.linspace(0, 2 * np.pi, nSamples)
        complex_vals = np.zeros((nSamples, 2), dtype=np.float64)

        for term in series.terms.values():
            # Compute complex value of each term and accumulate
            complex_vals[:, 0] += term.Real * np.cos(term.n * t_vals) - term.Imag * np.sin(term.n * t_vals)
            complex_vals[:, 1] += term.Imag * np.cos(term.n * t_vals) + term.Real * np.sin(term.n * t_vals)

        plt.figure(figsize=(8, 8))
        plt.plot(complex_vals[:, 0], complex_vals[:, 1], label="Fourier Series Path")
        plt.title("Fourier Series Path in the Complex Plane")
        plt.xlabel("Real Part")
        plt.ylabel("Imaginary Part")
        plt.axhline(0, color='gray', lw=0.5)
        plt.axvline(0, color='gray', lw=0.5)
        plt.grid(True)
        plt.legend()
        plt.show()

class GLSLEmitter:
    def __init__(self):
        self.seriesMap: dict[str, 'FourierSeries'] = {}

    def addData(self, dataName, series: 'FourierSeries'):
        self.seriesMap[dataName] = series

    def emitShaderData(self, emitDefinition=True):
        Output = ""

        if emitDefinition:
            Output += "struct FourierTerm {\n"
            Output += "  float Real;\n"
            Output += "  float Imag;\n"
            Output += "};\n"

        Output += "\n"
        for dataName, dataSeries in self.seriesMap.items():
            numCoeff = len(dataSeries.terms)

            sortedTerms = [-idx for idx in range((numCoeff - 1) // 2, 0, -1)] + [0] + [idx for idx in range(1, (numCoeff - 1) // 2 + 1)]
            assert(len(sortedTerms) == numCoeff)

            Output += f"FourierTerm {dataName}[{numCoeff}] = FourierTerm[{numCoeff}](\n"
            for idx in sortedTerms:
                termCoeff = dataSeries.terms[idx]
                Output += f"  FourierTerm({termCoeff.Real}, {termCoeff.Imag}), // i = {idx}\n"
            Output += f");\n"
            Output += "\n"
        
        return Output
        


# returns a numpy function
def compileToNumpy(expr):
    fakeGlobal = {
        'numpy': np
    }
    code_expr = NumPyPrinter().doprint(expr)
    exec(f"def numpy_expr(t):\n    return {code_expr}\n", fakeGlobal)

    return fakeGlobal['numpy_expr']

def uniformSpaceNumericalIntgNp(func, lBound, uBound, N=5000):
    samples = np.linspace(lBound, uBound, N)
    total = 0
    total += np.sum(func(samples))
    
    total *= ((uBound - lBound) / N)

    return total


def parametricFunctionToFourierSeriesNumericalPreNP(t, funcx, funcy, nSeries=10):
    series = FourierSeries({})

    # int_0^{2\pi} {(funcx +i * funcy)e^{-inx} dx}
    # = int_0^{2\pi} {(funcx + i * funcy)(cos(nx)-isin(nx)) dx}
    # = int_0^{2\pi} {(funcx + i * funcy)(cos(nx)-isin(nx)) dx}
    # = int_0^{2\pi} {(funcx cos(nx) + funcy sin(nx) + i (funcy cos(nx)-funcx sinnx)) dx}

    # if nSeries is 10, then give (-10, ..., -1, 1, ..., 10)

    npfuncx = compileToNumpy(funcx)
    npfuncy = compileToNumpy(funcy)
    
    for nOuter in range(1, nSeries + 1):
        for n in [-nOuter, nOuter]:
            thisTerm = FourierSeriesTerm(
                n=n,
                Real=uniformSpaceNumericalIntgNp(
                    lambda t: npfuncx(t) * np.cos(n * t) + npfuncy(t) * np.sin(n * t),
                    0, 2 * math.pi
                ),
                Imag=uniformSpaceNumericalIntgNp(
                    lambda t: npfuncy(t) * np.cos(n * t) - npfuncx(t) * np.sin(n * t),
                    0, 2 * math.pi
                )
            )

            series.terms[n] = thisTerm

    constTerm = FourierSeriesTerm(
        n=0,
        Real=uniformSpaceNumericalIntgNp(npfuncx, 0, 2 * math.pi),
        Imag=uniformSpaceNumericalIntgNp(npfuncy, 0, 2 * math.pi)
    )
    series.terms[0] = constTerm

    return series

def plotSeries(series: FourierSeries):
    nSamples = len(series.terms) * 50 + 200
    t_vals = np.linspace(0, 2 * np.pi, nSamples)
    complex_vals = np.zeros((nSamples, 2), dtype=np.float64)

    for term in series.terms.values():
        # Compute complex value of each term and accumulate
        complex_vals[:, 0] += term.Real * np.cos(term.n * t_vals) - term.Imag * np.sin(term.n * t_vals)
        complex_vals[:, 1] += term.Imag * np.cos(term.n * t_vals) + term.Real * np.sin(term.n * t_vals)

    plt.figure(figsize=(8, 8))
    plt.plot(complex_vals[:, 0], complex_vals[:, 1], label="Fourier Series Path")
    plt.title("Fourier Series Path in the Complex Plane")
    plt.xlabel("Real Part")
    plt.ylabel("Imaginary Part")
    plt.axhline(0, color='gray', lw=0.5)
    plt.axvline(0, color='gray', lw=0.5)
    plt.grid(True)
    plt.legend()
    plt.show()


if __name__ == '__main__':

    t, funcx, funcy = BezierPiecewiseBuilder.testReturnF()
    series = parametricFunctionToFourierSeriesNumericalPreNP(t, funcx, funcy, 25)
    series.plot()

    emitter = GLSLEmitter()
    emitter.addData('f', series)
    shaderCode = emitter.emitShaderData()

    print(shaderCode)