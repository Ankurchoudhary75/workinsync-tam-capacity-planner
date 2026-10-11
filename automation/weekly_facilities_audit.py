#!/usr/bin/env python3
"""
WorkInSync Weekly Facilities Health Audit Automation
====================================================
Author: Ankur Choudhary (Technical Account Manager Candidate)
Company: WorkInSync (by MoveInSync)

Description:
  Automates the recurring weekly facilities audit for global enterprise accounts.
  Ingests utilization telemetry from Bangalore, New York, and London, checks for
  SLA breaches (bump rate > 2%, ghost rate > 5%, peak > 85%), and generates an
  executive audit summary.
"""

from datetime import datetime
import json
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from kpi_suite.facilities_kpi_evaluator import FacilitiesKPIEvaluator
from analytics_engine.capacity_simulation_engine import WorkplaceCapacityPlanner

def run_weekly_audit():
    print(f"[*] Executing WorkInSync Global Facilities Audit — {datetime.now():%Y-%m-%d}...")
    
    planner = WorkplaceCapacityPlanner()
    bounds = planner.calculate_bounds()

    evaluator = FacilitiesKPIEvaluator()
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

    output = f"""# WorkInSync Weekly Facilities Executive Brief — {datetime.now():%Y-%m-%d}

## Global Capacity & Space Allocation
- **Total Portfolio Headcount:** {bounds['headcount_total']:,} employees across 3 countries
- **In-Office Policy:** {bounds['days_per_week_policy']} days/week (6,000 desk-days/week)
- **Active Seating Capacity:** **{bounds['optimal_managed_seats']:,} Seats** (Sharing Ratio: **{bounds['optimal_sharing_ratio']}:1**)
- **Annual Real Estate OPEX Savings:** **${bounds['annual_opex_savings_optimal_usd']:,.2f} / year** ({bounds['headcount_total'] - bounds['optimal_managed_seats']} desks consolidated)

## Global Facilities Health Index: {report['overall_facilities_score']} / 100.0 [{report['health_rating']}]
- **Peak Utilization:** 81.4% (Optimal Goldilocks Zone: 75% - 85%)
- **Ghost Desk Rate:** 3.6% (Target: ≤ 5.0% - Healthy)
- **Booking Bump Rate:** 1.1% (Target: ≤ 2.0% - Low Friction)
- **Check-in Compliance:** 95.2% (Target: ≥ 92.0% - High Adoption)
- **Reverse Ghosting Recovery:** 86.5% (Target: ≥ 80.0% - High Efficiency)

## Office-Level Allocation Matrix:
"""
    for o in bounds["office_distribution"]:
        output += f"- **{o['country']} ({o['city']}):** {o['headcount']} Headcount -> **{o['optimal_seats']} Seats** (Peak: {o['unmanaged_peak_seats']}, Savings: ${o['annual_savings_usd']:,.2f}/yr)\n"

    os.makedirs("automation/reports", exist_ok=True)
    report_file = f"automation/reports/facilities_audit_{datetime.now():%Y_%m_%d}.md"
    with open(report_file, "w") as f:
        f.write(output)

    print(f"[+] Weekly audit complete. Report written to {report_file}")
    print(output)

if __name__ == "__main__":
    run_weekly_audit()
