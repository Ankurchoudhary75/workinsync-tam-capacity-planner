#!/usr/bin/env python3
"""
WorkInSync Enterprise Facilities Management KPI Evaluator
=========================================================
Author: Ankur Choudhary (Technical Account Manager Candidate)
Role: TAM / Implementation Specialist — Workplace Analytics
Company: WorkInSync (MoveInSync)

Assessment Objective:
  "What KPIs will you use to assess whether the Facilities Team is doing a good job?"

Architecture:
  Evaluates 5 strategic Facilities Management (FM) Pillars:
  1. Space & Capacity Utilization
  2. Employee Experience (EX) & Friction
  3. Financial & Real Estate Cost Optimization
  4. Operational Efficiency & Reverse Ghosting
  5. Health, Safety & Floor Compliance
"""

from typing import Dict, Any, List

class FacilitiesKPIEvaluator:
    def __init__(self):
        # Benchmark industry thresholds based on WorkInSync enterprise deployments
        self.kpi_benchmarks = {
            "peak_utilization_pct": {"target": (75.0, 85.0), "unit": "%", "weight": 20},
            "ghost_desk_rate_pct": {"target": 5.0, "direction": "below", "unit": "%", "weight": 15},
            "booking_denial_rate_pct": {"target": 2.0, "direction": "below", "unit": "%", "weight": 15},
            "checkin_compliance_pct": {"target": 92.0, "direction": "above", "unit": "%", "weight": 15},
            "reverse_ghosting_recovery_pct": {"target": 80.0, "direction": "above", "unit": "%", "weight": 10},
            "cost_savings_vs_dedicated_pct": {"target": 30.0, "direction": "above", "unit": "%", "weight": 15},
            "facilities_ticket_sla_pct": {"target": 95.0, "direction": "above", "unit": "%", "weight": 10}
        }

    def evaluate_facilities_performance(self, telemetry: Dict[str, float]) -> Dict[str, Any]:
        """
        Computes composite health score and evaluates each KPI against enterprise benchmarks.
        """
        results = []
        total_score = 0.0
        max_score = 100.0

        # 1. Peak Utilization
        peak = telemetry.get("peak_utilization_pct", 82.0)
        target_min, target_max = self.kpi_benchmarks["peak_utilization_pct"]["target"]
        if target_min <= peak <= target_max:
            peak_status = "OPTIMAL"
            score_contrib = 20.0
        elif peak > target_max:
            peak_status = "OVERCROWDED (Capacity Risk)"
            score_contrib = 10.0
        else:
            peak_status = "UNDERUTILIZED (Capital Waste)"
            score_contrib = 12.0
        total_score += score_contrib
        results.append({
            "kpi": "Peak Seat Utilization",
            "value": f"{peak:.1f}%",
            "target": f"{target_min}% - {target_max}%",
            "status": peak_status,
            "pillar": "Space & Capacity"
        })

        # 2. Ghost Desk Rate (Booked but not checked-in)
        ghost = telemetry.get("ghost_desk_rate_pct", 3.8)
        ghost_target = self.kpi_benchmarks["ghost_desk_rate_pct"]["target"]
        ghost_status = "HEALTHY" if ghost <= ghost_target else "ACTION REQUIRED"
        score_contrib = 15.0 if ghost <= ghost_target else max(0.0, 15.0 - (ghost - ghost_target) * 3)
        total_score += score_contrib
        results.append({
            "kpi": "Ghost Desk Rate",
            "value": f"{ghost:.1f}%",
            "target": f"≤ {ghost_target}%",
            "status": ghost_status,
            "pillar": "Space & Capacity"
        })

        # 3. Booking Denial Rate (Employee bump rate)
        denial = telemetry.get("booking_denial_rate_pct", 1.2)
        denial_target = self.kpi_benchmarks["booking_denial_rate_pct"]["target"]
        denial_status = "OPTIMAL" if denial <= denial_target else "FRICTION ALERT"
        score_contrib = 15.0 if denial <= denial_target else max(0.0, 15.0 - (denial - denial_target) * 5)
        total_score += score_contrib
        results.append({
            "kpi": "Booking Denial (Bump) Rate",
            "value": f"{denial:.1f}%",
            "target": f"≤ {denial_target}%",
            "status": denial_status,
            "pillar": "Employee Experience"
        })

        # 4. Check-In Compliance Rate
        compliance = telemetry.get("checkin_compliance_pct", 94.5)
        comp_target = self.kpi_benchmarks["checkin_compliance_pct"]["target"]
        comp_status = "EXCELLENT" if compliance >= comp_target else "BELOW TARGET"
        score_contrib = 15.0 if compliance >= comp_target else max(0.0, 15.0 - (comp_target - compliance) * 2)
        total_score += score_contrib
        results.append({
            "kpi": "Check-In Compliance Rate",
            "value": f"{compliance:.1f}%",
            "target": f"≥ {comp_target}%",
            "status": comp_status,
            "pillar": "Employee Experience"
        })

        # 5. Reverse Ghosting Recovery
        recovery = telemetry.get("reverse_ghosting_recovery_pct", 84.0)
        rec_target = self.kpi_benchmarks["reverse_ghosting_recovery_pct"]["target"]
        rec_status = "HIGH EFFICIENCY" if recovery >= rec_target else "LATENCY DELAY"
        score_contrib = 10.0 if recovery >= rec_target else max(0.0, 10.0 - (rec_target - recovery) * 1)
        total_score += score_contrib
        results.append({
            "kpi": "Reverse Ghosting Desk Recovery",
            "value": f"{recovery:.1f}%",
            "target": f"≥ {rec_target}%",
            "status": rec_status,
            "pillar": "Operational Recovery"
        })

        # 6. Real Estate OPEX Savings vs 1:1
        savings = telemetry.get("cost_savings_vs_dedicated_pct", 31.0)
        sav_target = self.kpi_benchmarks["cost_savings_vs_dedicated_pct"]["target"]
        sav_status = "EXCEEDED" if savings >= sav_target else "ON TARGET"
        score_contrib = 15.0 if savings >= sav_target else 10.0
        total_score += score_contrib
        results.append({
            "kpi": "Real Estate OPEX Savings vs 1:1",
            "value": f"{savings:.1f}%",
            "target": f"≥ {sav_target}%",
            "status": sav_status,
            "pillar": "Financial Optimization"
        })

        # 7. Facilities SLA
        sla = telemetry.get("facilities_ticket_sla_pct", 97.2)
        sla_target = self.kpi_benchmarks["facilities_ticket_sla_pct"]["target"]
        sla_status = "EXCELLENT" if sla >= sla_target else "BREACH RISK"
        score_contrib = 10.0 if sla >= sla_target else 5.0
        total_score += score_contrib
        results.append({
            "kpi": "Desk Ticket Resolution SLA (<4h)",
            "value": f"{sla:.1f}%",
            "target": f"≥ {sla_target}%",
            "status": sla_status,
            "pillar": "Facilities Operations"
        })

        health_rating = "A+ (World-Class)" if total_score >= 90 else ("A (Strong)" if total_score >= 80 else "B (Needs Attention)")

        return {
            "overall_facilities_score": round(total_score, 1),
            "health_rating": health_rating,
            "kpis": results
        }

def run_evaluation_demo():
    print("================================================================================")
    print("  WORKINSYNC FACILITIES MANAGEMENT KPI EVALUATION REPORT")
    print("================================================================================\n")
    evaluator = FacilitiesKPIEvaluator()

    # Telemetry snapshot from the 3 offices
    sample_telemetry = {
        "peak_utilization_pct": 81.4,
        "ghost_desk_rate_pct": 3.6,
        "booking_denial_rate_pct": 1.1,
        "checkin_compliance_pct": 95.2,
        "reverse_ghosting_recovery_pct": 86.5,
        "cost_savings_vs_dedicated_pct": 31.0,
        "facilities_ticket_sla_pct": 98.1
    }

    report = evaluator.evaluate_facilities_performance(sample_telemetry)

    print(f"Overall Facilities Health Score: {report['overall_facilities_score']}/100.0 [{report['health_rating']}]\n")
    print(f"{'Pillar':<22} | {'KPI Name':<32} | {'Observed':<10} | {'Target':<14} | {'Status'}")
    print("-" * 95)
    for k in report["kpis"]:
        print(f"{k['pillar']:<22} | {k['kpi']:<32} | {k['value']:<10} | {k['target']:<14} | {k['status']}")
    print("=" * 95)

if __name__ == "__main__":
    run_evaluation_demo()
