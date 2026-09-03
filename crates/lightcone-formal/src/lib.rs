//! Exact formal execution belongs to an engine lane, not to the passive
//! Lightcone. Every primitive below is evaluated by two independently shaped
//! implementations and fails closed on disagreement.

use serde::{Deserialize, Serialize};
use thiserror::Error;

#[derive(Clone, Copy, Debug, Deserialize, Serialize, PartialEq, Eq)]
pub struct Rational {
    pub numerator: i128,
    pub denominator: i128,
}

impl Rational {
    pub fn new(numerator: i128, denominator: i128) -> Result<Self, FormalError> {
        if denominator == 0 {
            return Err(FormalError::DivisionByZero);
        }
        if numerator == 0 {
            return Ok(Self {
                numerator: 0,
                denominator: 1,
            });
        }
        let common = i128::try_from(gcd(numerator.unsigned_abs(), denominator.unsigned_abs()))
            .map_err(|_| FormalError::Overflow)?;
        let mut numerator = numerator / common;
        let mut denominator = denominator / common;
        if denominator < 0 {
            numerator = numerator.checked_neg().ok_or(FormalError::Overflow)?;
            denominator = denominator.checked_neg().ok_or(FormalError::Overflow)?;
        }
        Ok(Self {
            numerator,
            denominator,
        })
    }

    pub fn integer(value: i128) -> Self {
        Self {
            numerator: value,
            denominator: 1,
        }
    }

    pub fn checked_add(self, other: Self) -> Result<Self, FormalError> {
        let left = self
            .numerator
            .checked_mul(other.denominator)
            .ok_or(FormalError::Overflow)?;
        let right = other
            .numerator
            .checked_mul(self.denominator)
            .ok_or(FormalError::Overflow)?;
        let denominator = self
            .denominator
            .checked_mul(other.denominator)
            .ok_or(FormalError::Overflow)?;
        Self::new(
            left.checked_add(right).ok_or(FormalError::Overflow)?,
            denominator,
        )
    }

    pub fn checked_sub(self, other: Self) -> Result<Self, FormalError> {
        self.checked_add(Self::new(
            other.numerator.checked_neg().ok_or(FormalError::Overflow)?,
            other.denominator,
        )?)
    }

    pub fn checked_mul(self, other: Self) -> Result<Self, FormalError> {
        Self::new(
            self.numerator
                .checked_mul(other.numerator)
                .ok_or(FormalError::Overflow)?,
            self.denominator
                .checked_mul(other.denominator)
                .ok_or(FormalError::Overflow)?,
        )
    }

    pub fn checked_div(self, other: Self) -> Result<Self, FormalError> {
        if other.numerator == 0 {
            return Err(FormalError::DivisionByZero);
        }
        Self::new(
            self.numerator
                .checked_mul(other.denominator)
                .ok_or(FormalError::Overflow)?,
            self.denominator
                .checked_mul(other.numerator)
                .ok_or(FormalError::Overflow)?,
        )
    }

    pub fn checked_pow(self, exponent: u32) -> Result<Self, FormalError> {
        let mut result = Self::integer(1);
        for _ in 0..exponent {
            result = result.checked_mul(self)?;
        }
        Ok(result)
    }
}

impl std::fmt::Display for Rational {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        if self.denominator == 1 {
            write!(formatter, "{}", self.numerator)
        } else {
            write!(formatter, "{}/{}", self.numerator, self.denominator)
        }
    }
}

#[derive(Clone, Copy, Debug, Deserialize, Serialize, PartialEq, Eq)]
pub struct Point {
    pub x: i128,
    pub y: i128,
}

#[derive(Clone, Debug, Deserialize, Serialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case", tag = "primitive", content = "arguments")]
pub enum Request {
    ArithmeticAdd {
        left: Rational,
        right: Rational,
    },
    ArithmeticSubtract {
        left: Rational,
        right: Rational,
    },
    ArithmeticMultiply {
        left: Rational,
        right: Rational,
    },
    ArithmeticDivide {
        dividend: Rational,
        divisor: Rational,
    },
    AlgebraSolveLinear {
        coefficient: Rational,
        offset: Rational,
        result: Rational,
    },
    AlgebraPolynomialValue {
        coefficients: Vec<i128>,
        x: i128,
    },
    CalculusPolynomialDerivative {
        coefficients: Vec<i128>,
    },
    CalculusDefiniteIntegral {
        coefficients: Vec<i128>,
        lower: i128,
        upper: i128,
    },
    GeometryDistanceSquared {
        left: Point,
        right: Point,
    },
    GeometryTriangleTwiceArea {
        a: Point,
        b: Point,
        c: Point,
    },
    GeometryPythagoreanCheck {
        side_a: i128,
        side_b: i128,
        hypotenuse: i128,
    },
    ProbabilityDisjointUnion {
        left: Rational,
        right: Rational,
    },
    WordRateDistance {
        rate: Rational,
        time: Rational,
    },
    WordUnitRate {
        total: Rational,
        units: Rational,
    },
    WordPercentOf {
        part: Rational,
        whole: Rational,
    },
}

#[derive(Clone, Debug, Deserialize, Serialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case", tag = "type", content = "value")]
pub enum Value {
    Rational(Rational),
    Integer(i128),
    IntegerList(Vec<i128>),
    Boolean(bool),
}

#[derive(Clone, Debug, Deserialize, Serialize, PartialEq, Eq)]
pub struct ExecutionReceipt {
    pub runtime: &'static str,
    pub primitive: &'static str,
    pub value: Value,
    pub oracle_value: Value,
    pub oracle_agreement: bool,
    pub exact: bool,
}

pub fn execute_checked(request: &Request) -> Result<ExecutionReceipt, FormalError> {
    let value = runtime(request)?;
    let oracle_value = oracle(request)?;
    if value != oracle_value {
        return Err(FormalError::OracleDisagreement {
            runtime: value,
            oracle: oracle_value,
        });
    }
    Ok(ExecutionReceipt {
        runtime: "lightcone-formal-v1",
        primitive: primitive_name(request),
        value: value.clone(),
        oracle_value,
        oracle_agreement: true,
        exact: true,
    })
}

pub fn primitive_name(request: &Request) -> &'static str {
    match request {
        Request::ArithmeticAdd { .. } => "arithmetic_add",
        Request::ArithmeticSubtract { .. } => "arithmetic_subtract",
        Request::ArithmeticMultiply { .. } => "arithmetic_multiply",
        Request::ArithmeticDivide { .. } => "arithmetic_divide",
        Request::AlgebraSolveLinear { .. } => "algebra_solve_linear",
        Request::AlgebraPolynomialValue { .. } => "algebra_polynomial_value",
        Request::CalculusPolynomialDerivative { .. } => "calculus_polynomial_derivative",
        Request::CalculusDefiniteIntegral { .. } => "calculus_definite_integral",
        Request::GeometryDistanceSquared { .. } => "geometry_distance_squared",
        Request::GeometryTriangleTwiceArea { .. } => "geometry_triangle_twice_area",
        Request::GeometryPythagoreanCheck { .. } => "geometry_pythagorean_check",
        Request::ProbabilityDisjointUnion { .. } => "probability_disjoint_union",
        Request::WordRateDistance { .. } => "word_rate_distance",
        Request::WordUnitRate { .. } => "word_unit_rate",
        Request::WordPercentOf { .. } => "word_percent_of",
    }
}

fn runtime(request: &Request) -> Result<Value, FormalError> {
    match request {
        Request::ArithmeticAdd { left, right } => Ok(Value::Rational(left.checked_add(*right)?)),
        Request::ArithmeticSubtract { left, right } => {
            Ok(Value::Rational(left.checked_sub(*right)?))
        }
        Request::ArithmeticMultiply { left, right } => {
            Ok(Value::Rational(left.checked_mul(*right)?))
        }
        Request::ArithmeticDivide { dividend, divisor } => {
            Ok(Value::Rational(dividend.checked_div(*divisor)?))
        }
        Request::AlgebraSolveLinear {
            coefficient,
            offset,
            result,
        } => {
            if coefficient.numerator == 0 {
                return Err(FormalError::Undefined("linear coefficient is zero"));
            }
            Ok(Value::Rational(
                result.checked_sub(*offset)?.checked_div(*coefficient)?,
            ))
        }
        Request::AlgebraPolynomialValue { coefficients, x } => {
            validate_coefficients(coefficients)?;
            let mut accumulator = 0i128;
            for coefficient in coefficients.iter().rev() {
                accumulator = accumulator
                    .checked_mul(*x)
                    .and_then(|value| value.checked_add(*coefficient))
                    .ok_or(FormalError::Overflow)?;
            }
            Ok(Value::Integer(accumulator))
        }
        Request::CalculusPolynomialDerivative { coefficients } => {
            validate_coefficients(coefficients)?;
            let derivative = coefficients
                .iter()
                .enumerate()
                .skip(1)
                .map(|(power, coefficient)| {
                    coefficient
                        .checked_mul(i128::try_from(power).map_err(|_| FormalError::Overflow)?)
                        .ok_or(FormalError::Overflow)
                })
                .collect::<Result<Vec<_>, _>>()?;
            Ok(Value::IntegerList(derivative))
        }
        Request::CalculusDefiniteIntegral {
            coefficients,
            lower,
            upper,
        } => {
            validate_coefficients(coefficients)?;
            let mut total = Rational::integer(0);
            for (power, coefficient) in coefficients.iter().enumerate() {
                let exponent = u32::try_from(power + 1).map_err(|_| FormalError::Overflow)?;
                let upper_term = Rational::integer(*upper).checked_pow(exponent)?;
                let lower_term = Rational::integer(*lower).checked_pow(exponent)?;
                let delta = upper_term.checked_sub(lower_term)?;
                total = total.checked_add(
                    delta.checked_mul(Rational::new(*coefficient, i128::from(exponent))?)?,
                )?;
            }
            Ok(Value::Rational(total))
        }
        Request::GeometryDistanceSquared { left, right } => {
            let dx = left.x.checked_sub(right.x).ok_or(FormalError::Overflow)?;
            let dy = left.y.checked_sub(right.y).ok_or(FormalError::Overflow)?;
            Ok(Value::Integer(
                dx.checked_mul(dx)
                    .and_then(|value| {
                        dy.checked_mul(dy)
                            .and_then(|other| value.checked_add(other))
                    })
                    .ok_or(FormalError::Overflow)?,
            ))
        }
        Request::GeometryTriangleTwiceArea { a, b, c } => {
            let abx = b.x.checked_sub(a.x).ok_or(FormalError::Overflow)?;
            let aby = b.y.checked_sub(a.y).ok_or(FormalError::Overflow)?;
            let acx = c.x.checked_sub(a.x).ok_or(FormalError::Overflow)?;
            let acy = c.y.checked_sub(a.y).ok_or(FormalError::Overflow)?;
            let cross = abx
                .checked_mul(acy)
                .and_then(|left| {
                    aby.checked_mul(acx)
                        .and_then(|right| left.checked_sub(right))
                })
                .ok_or(FormalError::Overflow)?;
            Ok(Value::Integer(
                cross.checked_abs().ok_or(FormalError::Overflow)?,
            ))
        }
        Request::GeometryPythagoreanCheck {
            side_a,
            side_b,
            hypotenuse,
        } => {
            if *side_a <= 0 || *side_b <= 0 || *hypotenuse <= 0 {
                return Err(FormalError::InvalidInput("triangle sides must be positive"));
            }
            let left = side_a
                .checked_mul(*side_a)
                .and_then(|value| {
                    side_b
                        .checked_mul(*side_b)
                        .and_then(|other| value.checked_add(other))
                })
                .ok_or(FormalError::Overflow)?;
            let right = hypotenuse
                .checked_mul(*hypotenuse)
                .ok_or(FormalError::Overflow)?;
            Ok(Value::Boolean(left == right))
        }
        Request::ProbabilityDisjointUnion { left, right } => {
            validate_probability(*left)?;
            validate_probability(*right)?;
            let total = left.checked_add(*right)?;
            validate_probability(total)?;
            Ok(Value::Rational(total))
        }
        Request::WordRateDistance { rate, time } => Ok(Value::Rational(rate.checked_mul(*time)?)),
        Request::WordUnitRate { total, units } => Ok(Value::Rational(total.checked_div(*units)?)),
        Request::WordPercentOf { part, whole } => Ok(Value::Rational(
            part.checked_div(*whole)?
                .checked_mul(Rational::integer(100))?,
        )),
    }
}

fn oracle(request: &Request) -> Result<Value, FormalError> {
    match request {
        Request::ArithmeticAdd { left, right } => Rational::new(
            left.numerator
                .checked_mul(right.denominator)
                .and_then(|value| {
                    right
                        .numerator
                        .checked_mul(left.denominator)
                        .and_then(|other| value.checked_add(other))
                })
                .ok_or(FormalError::Overflow)?,
            left.denominator
                .checked_mul(right.denominator)
                .ok_or(FormalError::Overflow)?,
        )
        .map(Value::Rational),
        Request::ArithmeticSubtract { left, right } => oracle(&Request::ArithmeticAdd {
            left: *left,
            right: Rational::new(
                right.numerator.checked_neg().ok_or(FormalError::Overflow)?,
                right.denominator,
            )?,
        }),
        Request::ArithmeticMultiply { left, right } => Rational::new(
            left.numerator
                .checked_mul(right.numerator)
                .ok_or(FormalError::Overflow)?,
            left.denominator
                .checked_mul(right.denominator)
                .ok_or(FormalError::Overflow)?,
        )
        .map(Value::Rational),
        Request::ArithmeticDivide { dividend, divisor } => {
            if divisor.numerator == 0 {
                return Err(FormalError::DivisionByZero);
            }
            Rational::new(
                dividend
                    .numerator
                    .checked_mul(divisor.denominator)
                    .ok_or(FormalError::Overflow)?,
                dividend
                    .denominator
                    .checked_mul(divisor.numerator)
                    .ok_or(FormalError::Overflow)?,
            )
            .map(Value::Rational)
        }
        Request::AlgebraSolveLinear {
            coefficient,
            offset,
            result,
        } => {
            if coefficient.numerator == 0 {
                return Err(FormalError::Undefined("linear coefficient is zero"));
            }
            let candidate = result.checked_sub(*offset)?.checked_div(*coefficient)?;
            let check = coefficient.checked_mul(candidate)?.checked_add(*offset)?;
            if check != *result {
                return Err(FormalError::Undefined(
                    "linear solution failed substitution",
                ));
            }
            Ok(Value::Rational(candidate))
        }
        Request::AlgebraPolynomialValue { coefficients, x } => {
            validate_coefficients(coefficients)?;
            let mut sum = 0i128;
            let mut power = 1i128;
            for coefficient in coefficients {
                sum = sum
                    .checked_add(
                        coefficient
                            .checked_mul(power)
                            .ok_or(FormalError::Overflow)?,
                    )
                    .ok_or(FormalError::Overflow)?;
                power = power.checked_mul(*x).ok_or(FormalError::Overflow)?;
            }
            Ok(Value::Integer(sum))
        }
        Request::CalculusPolynomialDerivative { coefficients } => {
            validate_coefficients(coefficients)?;
            let mut derivative = Vec::new();
            for (power, coefficient) in coefficients.iter().enumerate().skip(1) {
                let factor = i128::try_from(power).map_err(|_| FormalError::Overflow)?;
                derivative.push(
                    coefficient
                        .checked_mul(factor)
                        .ok_or(FormalError::Overflow)?,
                );
            }
            Ok(Value::IntegerList(derivative))
        }
        Request::CalculusDefiniteIntegral {
            coefficients,
            lower,
            upper,
        } => {
            fn antiderivative_at(coefficients: &[i128], x: i128) -> Result<Rational, FormalError> {
                let mut total = Rational::integer(0);
                for (power, coefficient) in coefficients.iter().enumerate() {
                    let exponent = u32::try_from(power + 1).map_err(|_| FormalError::Overflow)?;
                    total = total.checked_add(
                        Rational::new(*coefficient, i128::from(exponent))?
                            .checked_mul(Rational::integer(x).checked_pow(exponent)?)?,
                    )?;
                }
                Ok(total)
            }
            validate_coefficients(coefficients)?;
            Ok(Value::Rational(
                antiderivative_at(coefficients, *upper)?
                    .checked_sub(antiderivative_at(coefficients, *lower)?)?,
            ))
        }
        Request::GeometryDistanceSquared { left, right } => {
            let expanded = left
                .x
                .checked_mul(left.x)
                .and_then(|value| {
                    right
                        .x
                        .checked_mul(right.x)
                        .and_then(|term| value.checked_add(term))
                })
                .and_then(|value| {
                    left.x
                        .checked_mul(right.x)
                        .and_then(|term| term.checked_mul(2))
                        .and_then(|term| value.checked_sub(term))
                })
                .and_then(|value| {
                    left.y
                        .checked_mul(left.y)
                        .and_then(|term| value.checked_add(term))
                })
                .and_then(|value| {
                    right
                        .y
                        .checked_mul(right.y)
                        .and_then(|term| value.checked_add(term))
                })
                .and_then(|value| {
                    left.y
                        .checked_mul(right.y)
                        .and_then(|term| term.checked_mul(2))
                        .and_then(|term| value.checked_sub(term))
                })
                .ok_or(FormalError::Overflow)?;
            Ok(Value::Integer(expanded))
        }
        Request::GeometryTriangleTwiceArea { a, b, c } => {
            let first =
                a.x.checked_mul(b.y.checked_sub(c.y).ok_or(FormalError::Overflow)?)
                    .ok_or(FormalError::Overflow)?;
            let second =
                b.x.checked_mul(c.y.checked_sub(a.y).ok_or(FormalError::Overflow)?)
                    .ok_or(FormalError::Overflow)?;
            let third =
                c.x.checked_mul(a.y.checked_sub(b.y).ok_or(FormalError::Overflow)?)
                    .ok_or(FormalError::Overflow)?;
            Ok(Value::Integer(
                first
                    .checked_add(second)
                    .and_then(|value| value.checked_add(third))
                    .and_then(i128::checked_abs)
                    .ok_or(FormalError::Overflow)?,
            ))
        }
        Request::GeometryPythagoreanCheck {
            side_a,
            side_b,
            hypotenuse,
        } => {
            if *side_a <= 0 || *side_b <= 0 || *hypotenuse <= 0 {
                return Err(FormalError::InvalidInput("triangle sides must be positive"));
            }
            let mut sides = [*side_a, *side_b, *hypotenuse];
            sides.sort_unstable();
            let check = sides[0]
                .checked_mul(sides[0])
                .and_then(|value| {
                    sides[1]
                        .checked_mul(sides[1])
                        .and_then(|other| value.checked_add(other))
                })
                .ok_or(FormalError::Overflow)?
                == sides[2]
                    .checked_mul(sides[2])
                    .ok_or(FormalError::Overflow)?;
            Ok(Value::Boolean(check))
        }
        Request::ProbabilityDisjointUnion { left, right } => {
            validate_probability(*left)?;
            validate_probability(*right)?;
            oracle(&Request::ArithmeticAdd {
                left: *left,
                right: *right,
            })
            .and_then(|value| match value {
                Value::Rational(total) => {
                    validate_probability(total)?;
                    Ok(Value::Rational(total))
                }
                _ => Err(FormalError::Undefined("oracle returned wrong value type")),
            })
        }
        Request::WordRateDistance { rate, time } => oracle(&Request::ArithmeticMultiply {
            left: *rate,
            right: *time,
        }),
        Request::WordUnitRate { total, units } => oracle(&Request::ArithmeticDivide {
            dividend: *total,
            divisor: *units,
        }),
        Request::WordPercentOf { part, whole } => {
            let ratio = match oracle(&Request::ArithmeticDivide {
                dividend: *part,
                divisor: *whole,
            })? {
                Value::Rational(value) => value,
                _ => return Err(FormalError::Undefined("oracle returned wrong value type")),
            };
            oracle(&Request::ArithmeticMultiply {
                left: ratio,
                right: Rational::integer(100),
            })
        }
    }
}

fn validate_coefficients(coefficients: &[i128]) -> Result<(), FormalError> {
    if coefficients.is_empty() || coefficients.len() > 1024 {
        Err(FormalError::InvalidInput(
            "polynomial coefficients must contain 1..=1024 values",
        ))
    } else {
        Ok(())
    }
}

fn validate_probability(value: Rational) -> Result<(), FormalError> {
    if value.numerator < 0 || value.numerator > value.denominator {
        Err(FormalError::InvalidInput(
            "probability must lie within [0, 1]",
        ))
    } else {
        Ok(())
    }
}

fn gcd(mut left: u128, mut right: u128) -> u128 {
    while right != 0 {
        let remainder = left % right;
        left = right;
        right = remainder;
    }
    left.max(1)
}

#[derive(Clone, Debug, Error, PartialEq, Eq)]
pub enum FormalError {
    #[error("division by zero")]
    DivisionByZero,
    #[error("exact arithmetic overflow")]
    Overflow,
    #[error("invalid input: {0}")]
    InvalidInput(&'static str),
    #[error("undefined operation: {0}")]
    Undefined(&'static str),
    #[error("formal runtime and oracle disagreed: runtime={runtime:?}, oracle={oracle:?}")]
    OracleDisagreement { runtime: Value, oracle: Value },
}

#[cfg(test)]
mod tests {
    use super::*;

    fn r(numerator: i128, denominator: i128) -> Rational {
        Rational::new(numerator, denominator).unwrap()
    }

    #[test]
    fn rational_normalization_and_arithmetic_are_exact() {
        assert_eq!(r(-2, -4), r(1, 2));
        assert_eq!(r(1, 3).checked_add(r(1, 6)).unwrap(), r(1, 2));
        assert_eq!(r(7, 9).checked_div(r(14, 3)).unwrap(), r(1, 6));
    }

    #[test]
    fn division_by_zero_fails_closed() {
        assert_eq!(
            r(1, 2).checked_div(Rational::integer(0)),
            Err(FormalError::DivisionByZero)
        );
    }

    #[test]
    fn linear_solution_is_dual_checked() {
        let receipt = execute_checked(&Request::AlgebraSolveLinear {
            coefficient: r(3, 2),
            offset: r(-7, 3),
            result: r(13, 6),
        })
        .unwrap();
        assert_eq!(receipt.value, Value::Rational(r(3, 1)));
        assert!(receipt.oracle_agreement);
    }

    #[test]
    fn polynomial_horner_matches_naive_oracle() {
        let receipt = execute_checked(&Request::AlgebraPolynomialValue {
            coefficients: vec![13, -47, 61, -9],
            x: 17,
        })
        .unwrap();
        assert_eq!(receipt.value, Value::Integer(-27_374));
    }

    #[test]
    fn derivative_is_exact() {
        let receipt = execute_checked(&Request::CalculusPolynomialDerivative {
            coefficients: vec![3, -5, 7, 11],
        })
        .unwrap();
        assert_eq!(receipt.value, Value::IntegerList(vec![-5, 14, 33]));
    }

    #[test]
    fn definite_integral_uses_exact_rationals() {
        let receipt = execute_checked(&Request::CalculusDefiniteIntegral {
            coefficients: vec![3, -5, 7],
            lower: -2,
            upper: 4,
        })
        .unwrap();
        assert_eq!(receipt.value, Value::Rational(r(156, 1)));
    }

    #[test]
    fn geometry_primitives_agree_with_independent_forms() {
        let distance = execute_checked(&Request::GeometryDistanceSquared {
            left: Point { x: -3, y: 7 },
            right: Point { x: 5, y: -2 },
        })
        .unwrap();
        assert_eq!(distance.value, Value::Integer(145));

        let area = execute_checked(&Request::GeometryTriangleTwiceArea {
            a: Point { x: 0, y: 0 },
            b: Point { x: 5, y: 0 },
            c: Point { x: 2, y: 7 },
        })
        .unwrap();
        assert_eq!(area.value, Value::Integer(35));
    }

    #[test]
    fn pythagorean_boundary_rejects_nonpositive_sides() {
        assert_eq!(
            execute_checked(&Request::GeometryPythagoreanCheck {
                side_a: 0,
                side_b: 4,
                hypotenuse: 5,
            }),
            Err(FormalError::InvalidInput("triangle sides must be positive"))
        );
        assert_eq!(
            execute_checked(&Request::GeometryPythagoreanCheck {
                side_a: 3,
                side_b: 4,
                hypotenuse: 5,
            })
            .unwrap()
            .value,
            Value::Boolean(true)
        );
    }

    #[test]
    fn probability_union_checks_bounds() {
        assert_eq!(
            execute_checked(&Request::ProbabilityDisjointUnion {
                left: r(1, 3),
                right: r(1, 6),
            })
            .unwrap()
            .value,
            Value::Rational(r(1, 2))
        );
        assert!(
            execute_checked(&Request::ProbabilityDisjointUnion {
                left: r(3, 4),
                right: r(3, 4),
            })
            .is_err()
        );
    }

    #[test]
    fn typed_word_problems_do_not_need_model_arithmetic() {
        let distance = execute_checked(&Request::WordRateDistance {
            rate: r(55, 1),
            time: r(5, 2),
        })
        .unwrap();
        assert_eq!(distance.value, Value::Rational(r(275, 2)));

        let unit = execute_checked(&Request::WordUnitRate {
            total: r(189, 4),
            units: r(7, 1),
        })
        .unwrap();
        assert_eq!(unit.value, Value::Rational(r(27, 4)));

        let percent = execute_checked(&Request::WordPercentOf {
            part: r(7, 1),
            whole: r(32, 1),
        })
        .unwrap();
        assert_eq!(percent.value, Value::Rational(r(175, 8)));
    }
}
