"""Calculus causation: limits, derivatives, integrals, series, approximations."""

WORLD = "calculus-causation-v0"
PREFIX = "clc"
DOMAIN = "formal-mathematics"
SUBJECT = "formal-mathematics.calculus"
SOURCES = ["mathlib4", "nist-dlmf"]
SCOPE = "Everyday calculus: limits and continuity, derivatives as rates, optimisation, integrals as accumulation, the fundamental theorem, series and approximation"
ROOT_LABEL = "Calculus causation world"
ROOT_STATEMENT = "Root of the calculus causation world: how limits cause derivatives and integrals to work, and how those tools cause rates, areas and approximations to be found."

CONCEPTS = [
    ("limit", "Limit of a function", "The value a function's outputs approach as inputs close in on a point.", []),
    ("continuity", "Continuity at a point", "No jump or hole: the value equals the approached value.", []),
    ("derivative", "Derivative as a rate", "The instantaneous slope of a function at a point.", []),
    ("tangent-line", "Tangent line slope", "The straight line just touching the curve at a point.", []),
    ("differentiability", "Differentiability", "A function having a well-defined derivative at a point.", []),
    ("critical-point", "Critical point", "A place where the derivative is zero or missing.", []),
    ("local-max", "Local maximum", "A peak higher than everything nearby.", []),
    ("local-min", "Local minimum", "A valley lower than everything nearby.", []),
    ("increasing-behaviour", "Rising derivative sign", "The function climbs where its derivative is positive.", []),
    ("decreasing-behaviour", "Falling derivative sign", "The function sinks where its derivative is negative.", []),
    ("second-derivative", "Second derivative concavity", "The bend direction read from the derivative's own rate.", []),
    ("inflection-point", "Inflection point", "Where the curve switches its bending direction.", []),
    ("integral", "Integral as accumulation", "The total collected from a varying rate.", []),
    ("area-under-curve", "Area under a curve", "The region between a graph and the axis.", []),
    ("antiderivative", "Antiderivative family", "All functions whose derivative is the given one.", []),
    ("ftc", "Fundamental theorem of calculus", "Differentiation and integration undo each other.", []),
    ("riemann-sum", "Riemann sum approximation", "Totalting thin slices to approximate an area.", []),
    ("mean-value", "Mean value theorem bound", "Somewhere the instant rate equals the average rate.", []),
    ("chain-rule", "Chain rule for composition", "The derivative of a nested function multiplies the pieces' rates.", []),
    ("related-rates", "Related rates problems", "Linked quantities whose changes follow from one another.", []),
    ("optimization", "Optimization by derivatives", "Finding best values by hunting flat points and checking bends.", []),
    ("geometric-series", "Geometric series sum", "The total of terms shrinking by a fixed ratio.", []),
    ("series-convergence", "Series convergence", "An endless addition settling on a finite total.", []),
    ("taylor-approx", "Taylor approximation", "Rebuilding a function from its derivatives at one point.", []),
    ("remainder-shrink", "Remainder term shrink", "The leftover error shrinking as more terms are added.", []),
    ("instantaneous-rate", "Instantaneous rate of change", "The rate at one exact moment.", []),
    ("average-rate", "Average rate of change", "Total change divided by total time.", []),
    ("differential-change", "Small change differential", "A tiny step's effect estimated linearly.", []),
    ("linearization", "Linear approximation near a point", "Replacing a curve by its tangent line for short stretches.", []),
]

RELATIONS = [
    ("limit-enables-derivative", "limit", "derivative", "enables", "The limit of a function enables the derivative as a rate to exist.", "the limit of difference quotients exists", ""),
    ("derivative-predicts-instant", "derivative", "instantaneous-rate", "predicts", "The derivative as a rate predicts the instantaneous rate of change at each point.", "the function is differentiable there", ""),
    ("average-transforms-instant", "average-rate", "instantaneous-rate", "transforms_to", "The shrinking interval's average rate of change transforms into the instantaneous rate of change.", "the interval shrinks toward zero width", ""),
    ("derivative-predicts-tangent", "derivative", "tangent-line", "predicts", "The derivative as a rate predicts the tangent line slope at that point.", "the curve is smooth there", ""),
    ("differentiability-causes-continuity", "differentiability", "continuity", "causes", "Differentiability causes continuity at a point.", "the derivative exists there", ""),
    ("critical-enables-max", "critical-point", "local-max", "enables", "A zero-slope critical point enables a local maximum candidate to be located.", "the derivative vanishes or fails there", ""),
    ("critical-enables-min", "critical-point", "local-min", "enables", "A zero-slope critical point enables a local minimum candidate to be located.", "the graph levels off at that point", ""),
    ("positive-causes-rising", "derivative", "increasing-behaviour", "causes", "A positive derivative as a rate causes rising derivative sign behaviour on that stretch.", "the derivative stays positive across the interval", ""),
    ("negative-causes-falling", "derivative", "decreasing-behaviour", "causes", "A negative derivative as a rate causes falling derivative sign behaviour on that stretch.", "the derivative stays negative across the interval", ""),
    ("second-predicts-inflection", "second-derivative", "inflection-point", "predicts", "A sign flip in second derivative concavity predicts an inflection point.", "the second derivative crosses zero", ""),
    ("second-predicts-max", "second-derivative", "local-max", "predicts", "A negative second derivative concavity predicts a local maximum at the critical point.", "the first derivative vanishes there", ""),
    ("second-predicts-min", "second-derivative", "local-min", "predicts", "A positive second derivative concavity predicts a local minimum at the critical point.", "the tangent is horizontal at that point", ""),
    ("integral-causes-area", "integral", "area-under-curve", "causes", "The integral as accumulation causes the area under a curve to be totalled.", "the function is bounded on the interval", ""),
    ("riemann-enables-integral", "riemann-sum", "integral", "enables", "Refining a Riemann sum approximation enables the integral as accumulation to emerge as the limit.", "the slice widths shrink toward zero", ""),
    ("ftc-enables-antiderivative", "ftc", "antiderivative", "enables", "The fundamental theorem of calculus enables the antiderivative family to evaluate definite integrals.", "an antiderivative is known in closed form", ""),
    ("ftc-enables-area", "ftc", "area-under-curve", "enables", "The fundamental theorem of calculus enables the area under a curve to be found without summing slices.", "boundary values are known", ""),
    ("antiderivative-inverts-derivative", "antiderivative", "derivative", "enables", "The antiderivative family enables the derivative as a rate to be run backwards.", "constants of freedom are allowed", ""),
    ("meanvalue-predicts-average", "mean-value", "average-rate", "predicts", "The mean value theorem bound predicts some point matching the average rate of change.", "the function is continuous then differentiable on the stretch", ""),
    ("chain-enables-composite", "chain-rule", "derivative", "enables", "The chain rule for composition enables the derivative as a rate through nested functions.", "one function feeds another", ""),
    ("chain-enables-related", "chain-rule", "related-rates", "enables", "The chain rule for composition enables related rates problems to link changing quantities.", "two quantities depend through time", ""),
    ("critical-enables-optimization", "critical-point", "optimization", "enables", "Finding a critical point enables optimization by derivatives to locate best values.", "the quantity has one variable", ""),
    ("ratio-causes-convergence", "geometric-series", "series-convergence", "causes", "A ratio below one in the geometric series sum causes series convergence.", "each term multiplies by a fixed ratio under one", ""),
    ("taylor-enables-linear", "taylor-approx", "linearization", "enables", "The first-order Taylor approximation enables the linear approximation near a point.", "the point sits close to the centre", ""),
    ("remainder-predicts-error", "remainder-shrink", "taylor-approx", "predicts", "Fast remainder term shrink predicts small Taylor approximation error near the centre.", "more terms are taken", ""),
    ("linear-enables-differential", "linearization", "differential-change", "enables", "Linear approximation near a point enables the small change differential to estimate growth.", "the step is small", ""),
    ("limit-enables-continuity", "limit", "continuity", "enables", "The limit of a function enables continuity at a point to be defined.", "the limit equals the point's value", ""),
    ("differentiability-enables-tangent", "differentiability", "tangent-line", "enables", "Differentiability enables a well-defined tangent line slope.", "the difference quotient limit exists", ""),
    ("inflection-causes-bend-flip", "inflection-point", "second-derivative", "causes", "Crossing an inflection point causes the second derivative concavity to switch sign.", "the curve passes the zero of the second derivative", ""),
    ("antiderivative-prereq-ftc", "antiderivative", "ftc", "prerequisite", "An antiderivative family is a prerequisite for the fundamental theorem of calculus to apply in closed form.", "a usable antiderivative exists", ""),
    ("riemann-prereq-integral", "riemann-sum", "integral", "prerequisite", "Riemann sum approximation is a prerequisite for the integral as accumulation to be defined.", "slices cover the interval", ""),
    ("integral-causes-net-change", "integral", "differential-change", "causes", "The integral as accumulation causes small change differential pieces to total into a net change.", "the rate varies along the path", ""),
    ("convergence-prereq-taylor", "series-convergence", "taylor-approx", "prerequisite", "Series convergence of the expansion is a prerequisite for the Taylor approximation to hold.", "the expansion is summed near the centre", ""),
    ("derivative-prereq-second", "derivative", "second-derivative", "prerequisite", "A derivative as a rate is a prerequisite for second derivative concavity to exist.", "the rate itself can be differentiated", ""),
    ("limit-prereq-riemann", "limit", "riemann-sum", "prerequisite", "Taking a limit of a function is a prerequisite for Riemann sum approximation to become exact.", "slice widths approach zero", ""),
    ("continuity-prereq-differentiability", "continuity", "differentiability", "prerequisite", "Continuity at a point is a prerequisite for differentiability there.", "the point is in the domain interior", ""),
    ("second-enables-optimization", "second-derivative", "optimization", "enables", "Second derivative concavity enables optimization by derivatives to confirm best values.", "critical points are already found", ""),
    ("geometric-enables-taylor", "geometric-series", "taylor-approx", "enables", "The geometric series sum enables the Taylor approximation of simple functions.", "the expansion matches a geometric form", ""),
    ("integral-predicts-area", "integral", "area-under-curve", "predicts", "The integral as accumulation predicts the exact area under a curve.", "the curve stays above the axis", ""),
    ("differential-predicts-error", "differential-change", "linearization", "predicts", "A small change differential predicts the error of the linear approximation near a point.", "the second-order terms stay tiny", ""),
    ("passing-max-predicts-flip", "local-max", "increasing-behaviour", "predicts", "Passing a local maximum predicts the rising derivative sign turning to falling.", "the graph crosses the peak left to right", ""),
    ("passing-min-predicts-flip", "local-min", "decreasing-behaviour", "predicts", "Passing a local minimum predicts the falling derivative sign turning to rising.", "the graph crosses the valley left to right", ""),
]

MYTHS = [
    ("derivative-is-slope-only", "The derivative is only about slopes",
     "The derivative as a rate is any instantaneous rate of change, from speed to growth.", "derivative"),
    ("integral-is-area-only", "The integral is only about areas",
     "The integral as accumulation totals any varying flow, not just geometric area.", "integral"),
    ("zero-derivative-means-max", "A zero derivative always means a peak or valley",
     "A critical point can be a flat inflection, as in x cubed at zero.", "critical-point"),
    ("infinite-sum-diverges", "Adding infinitely many terms always blows up",
     "A shrinking geometric series sum settles on a finite total.", "series-convergence"),
    ("ftc-works-always", "The fundamental theorem always applies",
     "It needs continuity and a usable antiderivative family along the interval.", "ftc"),
]

BOUNDARIES = [
    ("nondifferentiable-points", "Corners break derivatives",
     "At kinks and jumps the derivative as a rate fails to exist.", "differentiability"),
    ("divergent-series", "Not every series settles",
     "Without series convergence, term-by-term reasoning is invalid.", "series-convergence"),
    ("approximation-range", "Linear estimates are local",
     "Linear approximation near a point degrades quickly away from it.", "linearization"),
]

EXAMPLES = [
    ("car-speedometer", "A car's speedometer",
     "The speedometer shows the instantaneous rate of change of distance while the trip average is the average rate of change.",
     ["instantaneous-rate", "average-rate", "derivative"]),
    ("filling-tank", "Filling a lopsided tank",
     "The volume of an odd-shaped tank comes from the integral as accumulation of its slice areas.",
     ["integral", "riemann-sum", "area-under-curve"]),
    ("fence-optimization", "The biggest pen from fixed fencing",
     "The best pen size sits at a critical point confirmed by second derivative concavity.",
     ["critical-point", "optimization", "second-derivative"]),
    ("drug-decay", "Repeated drug doses",
     "Each dose's leftover follows a geometric series sum toward a stable level.",
     ["geometric-series", "series-convergence", "related-rates"]),
]

CONTROLS = [
    ("corner-derivative", "Corners have derivatives",
     "A corner point must not be treated as having a well-defined derivative."),
    ("divergent-total", "Every infinite sum has a total",
     "An endless addition must not be treated as always having a finite total."),
    ("area-below-axis-negative-space", "Area below the axis counts positive",
     "The signed integral must not be treated as plain area below the axis."),
    ("antiderivative-unique", "Antiderivatives are unique",
     "The antiderivative family must not be treated as a single function."),
]
