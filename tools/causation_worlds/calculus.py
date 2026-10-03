"""Calculus causation: limits, derivatives, integrals, series, approximations."""

WORLD = "calculus-causation-v0"
PREFIX = "clc"
DOMAIN = "formal-mathematics"
SUBJECT = "formal-mathematics.calculus"
SOURCES = ["mathlib4", "nist-dlmf"]
SCOPE = "Everyday calculus: limits and continuity, derivatives as rates, optimisation, integrals as accumulation, the fundamental theorem, series and approximation"
ROOT_LABEL = "Calculus causation world"
ROOT_STATEMENT = 'Root of the calculus causation world: how differentiability, integrability and convergence hypotheses support rate, extremum, area and approximation predictions.'

CONCEPTS = [
    ('limit', 'Limit of a function', 'A value approached by f(x) as x approaches a specified accumulation point through its domain.', []),
    ('continuity', 'Continuity at a point', 'The condition lim_(x->a) f(x) = f(a), for a point a in the domain.', []),
    ('derivative', 'Derivative as a rate', 'The finite limit of [f(a+h)-f(a)]/h as h tends to zero, when it exists.', []),
    ('tangent-line', 'Tangent line slope', 'The slope of the limiting secant line to a graph when the limit is finite.', []),
    ('differentiability', 'Differentiability', 'A function having a well-defined derivative at a point.', []),
    ('critical-point', 'Critical point', 'An interior domain point c at which f prime is zero or does not exist.', []),
    ('local-max', 'Local maximum', 'A value f(c) at least as large as f(x) for all domain points x sufficiently near c.', []),
    ('local-min', 'Local minimum', 'A value f(c) at most as large as f(x) for all domain points x sufficiently near c.', []),
    ('increasing-behaviour', 'Increasing function', 'A function with f(x) < f(y) whenever x < y within the specified interval; strict increase is meant here.', []),
    ('decreasing-behaviour', 'Decreasing function', 'A function with f(x) > f(y) whenever x < y within the specified interval; strict decrease is meant here.', []),
    ('second-derivative', 'Second derivative concavity', 'The sign of f double-prime as a sufficient test of upward or downward concavity on an interval.', []),
    ('inflection-point', 'Inflection point', 'A point where a continuous graph changes from concave upward to concave downward or conversely.', []),
    ('integral', 'Integral as accumulation', 'The signed definite integral of an integrable real function on a bounded interval.', []),
    ('area-under-curve', 'Area under a curve', 'The nonnegative geometric area between a real graph and the horizontal axis over a specified interval.', []),
    ('antiderivative', 'Antiderivative family', 'All functions whose derivative is the given one.', []),
    ('ftc', 'Fundamental theorem of calculus', 'For continuous f, differentiating its integral recovers f, and any antiderivative F evaluates its definite integral by endpoint differences.', []),
    ('riemann-sum', 'Riemann sum approximation', 'Totalling f at one tag in each partition interval times its width to approximate a definite integral.', []),
    ('mean-value', 'Mean value theorem bound', 'For a real function continuous on [a,b] and differentiable on (a,b), some derivative equals the secant slope.', []),
    ('chain-rule', 'Chain rule for composition', "The derivative of a nested function multiplies the pieces' rates.", []),
    ('related-rates', 'Related rates problems', 'Linked quantities whose changes follow from one another.', []),
    ('optimization', 'Optimization by derivatives', 'Locating extrema by critical-point tests and by comparison with boundary values on the admissible domain.', []),
    ('geometric-series', 'Geometric series sum', 'A series a + ar + ar^2 + ... with fixed real or complex ratio r.', []),
    ('series-convergence', 'Series convergence', 'Convergence of the sequence of partial sums to a finite limit.', []),
    ('taylor-approx', 'Taylor approximation', 'The polynomial P_n(x) formed from derivatives through order n at a centre a, with an error requiring a separate bound.', []),
    ('remainder-shrink', 'Remainder term shrink', 'The condition that R_n(x) = f(x)-P_n(x) tends to zero as Taylor degree n grows at a specified x.', []),
    ('instantaneous-rate', 'Instantaneous rate of change', 'The rate at one exact moment.', []),
    ('average-rate', 'Average rate of change', 'Total change divided by total time.', []),
    ('differential-change', 'Small change differential', 'The linear quantity dy = f prime(a) dx used to estimate the finite increment f(a+dx)-f(a).', []),
    ('linearization', 'Linear approximation near a point', 'The affine function L(x) = f(a) + f prime(a)(x-a) associated with differentiable f at a.', []),
    ('actual-change', 'Finite output change', 'The exact increment Delta y = f(a+h)-f(a) for a finite input step h.', []),
    ('derivative-sign-change', 'First derivative sign change', 'Opposite strict signs of f prime on the two sides of an interior point.', []),
]

RELATIONS = [
    ('average-predicts-instant', 'average-rate', 'instantaneous-rate', 'predicts', 'The limiting average rate of change predicts the instantaneous rate of change at the base point.', 'f is real-valued and differentiable at a, and [f(a+h)-f(a)]/h is evaluated for nonzero h tending to zero', ''),
    ('derivative-predicts-tangent', 'derivative', 'tangent-line', 'predicts', 'The derivative as a rate predicts the tangent line slope of the graph.', 'f is a real function differentiable at a with a finite derivative and the tangent is the limit of secant lines through (a,f(a))', ''),
    ('differentiability-predicts-continuity', 'differentiability', 'continuity', 'predicts', 'Differentiability predicts continuity at a point.', 'f is real-valued on an open interval containing a and has a finite derivative at a', ''),
    ('max-predicts-critical', 'local-max', 'critical-point', 'predicts', 'A local maximum predicts a critical point when it occurs in the domain interior.', 'c lies inside an open real interval on which f is defined and f(c) is a local maximum; endpoints are excluded', ''),
    ('min-predicts-critical', 'local-min', 'critical-point', 'predicts', 'A local minimum predicts a critical point when it occurs in the domain interior.', 'c is an interior point of the real domain and f(c) is a local minimum, rather than a boundary minimum', ''),
    ('positive-predicts-rising', 'derivative', 'increasing-behaviour', 'predicts', 'A positive derivative as a rate predicts an increasing function on the interval.', 'f is continuous on [a,b], differentiable on (a,b), a < b, and f prime(x) > 0 throughout (a,b)', ''),
    ('negative-predicts-falling', 'derivative', 'decreasing-behaviour', 'predicts', 'A negative derivative as a rate predicts a decreasing function on the interval.', 'a < b, f is continuous on [a,b] and differentiable on (a,b), with f prime(x) < 0 at every interior point', ''),
    ('second-predicts-inflection', 'second-derivative', 'inflection-point', 'predicts', 'A strict sign change in second derivative concavity predicts an inflection point.', 'f is twice differentiable near c and f double-prime is strictly positive on one side of c and strictly negative on the other', ''),
    ('second-predicts-max', 'second-derivative', 'local-max', 'predicts', 'Negative second derivative concavity predicts a strict local maximum at a stationary point.', 'f is twice continuously differentiable near an interior c, f prime(c) = 0, and f double-prime(c) < 0', ''),
    ('second-predicts-min', 'second-derivative', 'local-min', 'predicts', 'Positive second derivative concavity predicts a strict local minimum at a stationary point.', 'c is interior, f is C^2 near c, f prime(c) = 0, and f double-prime(c) > 0', ''),
    ('riemann-predicts-integral', 'riemann-sum', 'integral', 'predicts', 'The limit of a Riemann sum approximation predicts the integral as accumulation independently of the tags.', 'f is Riemann integrable on a finite interval [a,b], and partition mesh tends to zero with arbitrary tags inside each subinterval', ''),
    ('ftc-predicts-antiderivative', 'ftc', 'antiderivative', 'predicts', 'The fundamental theorem of calculus predicts an antiderivative family F(x) = integral_a^x f(t) dt + C.', 'f is continuous on an open real interval containing a and x, and C is any real constant', ''),
    ('ftc-predicts-area', 'ftc', 'area-under-curve', 'predicts', 'The fundamental theorem of calculus predicts the area under a curve as F(b)-F(a).', 'a < b, f is continuous and nonnegative on [a,b], and F is continuous there with F prime = f on (a,b)', ''),
    ('antiderivative-predicts-integral', 'antiderivative', 'integral', 'predicts', 'An antiderivative family predicts the integral as accumulation by an endpoint difference independent of the additive constant.', 'f is continuous on [a,b] and F prime = f on an open interval containing [a,b], so every antiderivative F+C gives F(b)-F(a)', ''),
    ('meanvalue-predicts-average', 'mean-value', 'average-rate', 'predicts', 'The mean value theorem bound predicts that some derivative value equals the average rate of change (f(b)-f(a))/(b-a).', 'a < b and f is continuous on [a,b] and differentiable on (a,b)', ''),
    ('chain-predicts-composite', 'chain-rule', 'derivative', 'predicts', 'The chain rule for composition predicts the derivative as a rate of f(g(x)) to be f prime(g(x)) times g prime(x).', 'the real inner function g is differentiable at x and the real outer function f is differentiable at g(x)', ''),
    ('chain-enables-related', 'chain-rule', 'related-rates', 'enables', 'The chain rule for composition enables related rates problems to compute dy/dt from dy/dx and dx/dt.', 'x=g(t) is differentiable at the time t and y=f(x) is differentiable at x=g(t)', ''),
    ('critical-enables-optimization', 'critical-point', 'optimization', 'enables', 'Locating every critical point enables optimization by derivatives through comparison with endpoint values.', 'f is continuous on a compact interval [a,b], has finitely many interior critical points, and all of these and both endpoints are evaluated', ''),
    ('ratio-predicts-convergence', 'geometric-series', 'series-convergence', 'predicts', 'A geometric series sum with |r| < 1 predicts series convergence to a/(1-r).', 'a and r are fixed real or complex numbers and |r| < 1 for the series sum_(n=0)^infinity a*r^n', ''),
    ('remainder-prereq-taylor', 'remainder-shrink', 'taylor-approx', 'prerequisite', 'Remainder term shrink is a prerequisite for Taylor approximation polynomials to converge to the function at a specified point.', 'f has derivatives of every order at centre a, P_n is its Taylor polynomial, and equality f(x) = lim_(n->infinity) P_n(x) is required at fixed x', ''),
    ('differentiability-predicts-linearization', 'differentiability', 'linearization', 'predicts', 'Differentiability predicts a linear approximation near a point with error o(|h|).', 'f is differentiable at an interior point a and the increment h tends to zero within its real domain', ''),
    ('continuity-prereq-differentiability', 'continuity', 'differentiability', 'prerequisite', 'Continuity at a point is a prerequisite for differentiability there.', 'f is defined on a real open interval containing a and differentiability means a finite two-sided derivative at a', ''),
    ('second-enables-optimization', 'second-derivative', 'optimization', 'enables', 'Second derivative concavity enables optimization by derivatives to certify a unique global minimum on an interval.', 'f is C^2 on an open interval, f double-prime > 0 throughout it, and an interior c satisfies f prime(c) = 0', ''),
    ('geometric-predicts-taylor', 'geometric-series', 'taylor-approx', 'predicts', 'The geometric series sum predicts Taylor approximation polynomials 1+x+...+x^n for 1/(1-x) with remainder x^(n+1)/(1-x).', 'the centre is zero, n is a nonnegative integer, x is real, and |x| < 1', ''),
    ('integral-predicts-area', 'integral', 'area-under-curve', 'predicts', 'The integral as accumulation predicts the area under a curve when the integrand is nonnegative.', 'f is Riemann integrable and f(x) >= 0 on the finite interval [a,b] with a < b', ''),
    ('differential-predicts-change', 'differential-change', 'actual-change', 'predicts', 'The small change differential dy = f prime(a) dx predicts the finite output change Delta y to first order, with Delta y-dy = o(|dx|).', 'f is differentiable at a and nonzero dx tends to zero, so the error divided by |dx| tends to zero', ''),
    ('sign-change-predicts-max', 'derivative-sign-change', 'local-max', 'predicts', 'A first derivative sign change from positive to negative predicts a strict local maximum.', 'f is continuous at c and differentiable on (c-epsilon,c) and (c,c+epsilon), with f prime > 0 to the left and < 0 to the right for epsilon > 0', ''),
    ('sign-change-predicts-min', 'derivative-sign-change', 'local-min', 'predicts', 'A first derivative sign change from negative to positive predicts a strict local minimum.', 'for some epsilon > 0, f is continuous at c, differentiable on both punctured sides of c, with f prime < 0 to the left and > 0 to the right', ''),
]

MYTHS = [
    ('derivative-is-slope-only', 'The derivative is only about slopes', 'The derivative as a rate is any instantaneous rate of change, from speed to growth.', 'derivative'),
    ('integral-is-area-only', 'The integral is only about areas', 'The integral as accumulation totals any varying flow, not just geometric area.', 'integral'),
    ('zero-derivative-means-max', 'A zero derivative always means a peak or valley', 'A critical point can be a flat inflection, as in x cubed at zero.', 'critical-point'),
    ('infinite-sum-diverges', 'Adding infinitely many terms always blows up', 'The geometric series with first term 1 and ratio 1/2 has partial sums tending to 2.', 'series-convergence'),
    ('ftc-works-always', 'The fundamental theorem always applies', 'The elementary continuous-integrand form guarantees an integral-defined antiderivative; a closed-form antiderivative is not required, and weaker versions have their own hypotheses.', 'ftc'),
    ('taylor-convergence-enough', 'A convergent Taylor series always equals its function', 'For f(0)=0 and f(x)=exp(-1/x^2) when x != 0, every derivative at zero is zero; its Taylor series converges to zero but differs from f away from zero.', 'taylor-approx'),
]

BOUNDARIES = [
    ('nondifferentiable-points', 'Corners break derivatives', 'Different finite one-sided slopes at a corner prevent a two-sided derivative; a jump also prevents differentiability through failure of continuity.', 'differentiability'),
    ('divergent-series', 'Series convergence does not justify every interchange', 'Pointwise convergence alone does not justify termwise differentiation or integration; the relevant theorem needs extra uniform-convergence, domination or power-series hypotheses.', 'series-convergence'),
    ('approximation-range', 'Linear estimates need an error bound', 'Differentiability controls linearization error only as h tends to zero; for an affine function the approximation is exact at every distance.', 'linearization'),
    ('critical-not-extremum', 'A critical point need not be an extremum', 'The derivative of f(x)=x^3 vanishes at zero while the function remains strictly increasing through zero.', 'critical-point'),
    ('finite-taylor', 'Finite Taylor polynomials need no infinite convergence', 'A first-order approximation with o(|h|) error only needs differentiability at the centre; convergence of the infinite Taylor series is a separate question.', 'taylor-approx'),
    ('inflection-not-second-zero', 'A zero second derivative is inconclusive', 'For f(x)=x^4, f double-prime(0)=0 but concavity does not change, so zero is not an inflection point.', 'inflection-point'),
]

EXAMPLES = [
    ('car-speedometer', 'A car speedometer', 'For cumulative distance s(t)=t^2 metres at t seconds, average speed over [2,3] is 5 m/s while instantaneous speed at t=2 is 4 m/s.', ['instantaneous-rate', 'average-rate', 'derivative']),
    ('filling-tank', 'Filling a lopsided tank', 'A tank whose horizontal cross-section at height z has area (1+z) square metres has volume integral_0^2 (1+z) dz = 4 cubic metres below height 2 metres.', ['integral', 'riemann-sum', 'area-under-curve']),
    ('fence-optimization', 'The biggest pen from fixed fencing', 'A rectangular pen with 20 metres of perimeter has A(x)=x(10-x) on [0,10]; A prime=10-2x and A double-prime=-2 give a maximum area of 25 square metres at x=5, with zero area at the endpoints.', ['critical-point', 'optimization', 'second-derivative']),
    ('drug-decay', 'An idealized repeated-dose model', 'With identical doses D and a fixed retained fraction 1/2 between doses, the amount just after the nth dose is D sum_(k=0)^(n-1) (1/2)^k and tends to 2D; this is a mathematical model, not dosage advice.', ['geometric-series', 'series-convergence']),
    ('differential-error', 'A differential is not the error', 'For f(x)=x^2 at x=3 with dx=0.01, dy=0.06 while Delta y=0.0601; the error is 0.0001, not dy.', ['differential-change', 'actual-change', 'linearization']),
    ('endpoint-optimum', 'An endpoint escapes the critical-point list', 'For f(x)=x on [0,1], f prime=1 everywhere inside, yet the global maximum is at x=1; endpoint values must be checked.', ['critical-point', 'optimization', 'local-max']),
]

CONTROLS = [
    ('corner-derivative', 'Corners have derivatives', 'A corner point must not be treated as having a well-defined derivative.'),
    ('divergent-total', 'Every infinite sum has a total', 'An endless addition must not be treated as always having a finite total.'),
    ('area-below-axis-negative-space', 'Area below the axis counts positive', 'The signed integral must not be treated as plain area below the axis.'),
    ('antiderivative-unique', 'Antiderivatives are unique', 'The antiderivative family must not be treated as a single function.'),
    ('negative-ratio', 'Every ratio below one converges', 'The geometric series with ratio -2 must not be treated as convergent merely because -2 < 1.'),
    ('taylor-equality', 'Smoothness forces Taylor equality', 'An infinitely differentiable function must not be treated as necessarily equal to its Taylor series.'),
    ('differential-is-error', 'A differential is the approximation error', 'The linear differential dy must not be treated as the error Delta y-dy.'),
    ('zero-second-inflection', 'Zero second derivative proves inflection', 'A zero second derivative must not be treated as sufficient for a concavity change.'),
]
