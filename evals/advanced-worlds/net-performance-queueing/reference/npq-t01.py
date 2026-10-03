"""Analytic stationary FCFS M/M/1 and IID wait-for-all calculations."""
import math


def queue_report(arrival_rate, service_rate, threshold_seconds, percentile, fanout=1):
    gap = service_rate - arrival_rate
    rho = arrival_rate / service_rate
    system_tail = math.exp(-gap * threshold_seconds)
    if system_tail == 1.0:
        fanout_tail = 1.0
    else:
        fanout_tail = -math.expm1(fanout * math.log1p(-system_tail))
    return {
        "utilization": rho,
        "mean_system_count": arrival_rate / gap,
        "mean_queue_count": rho * arrival_rate / gap,
        "mean_system_seconds": 1.0 / gap,
        "mean_queue_seconds": rho / gap,
        "probability_zero_wait": gap / service_rate,
        "system_tail": system_tail,
        "queue_tail": rho * system_tail,
        "system_percentile_seconds": -math.log1p(-percentile) / gap,
        "fanout_tail": fanout_tail,
    }


def little_mean_time(mean_count, throughput):
    return mean_count / throughput
