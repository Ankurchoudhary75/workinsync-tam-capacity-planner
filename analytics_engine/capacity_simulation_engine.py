#!/usr/bin/env python3
"""
WorkInSync (by MoveInSync) Multi-Country Workplace Capacity Simulation Engine
=============================================================================
Author: Ankur Choudhary (Technical Account Manager Candidate)
Role: TAM / Implementation Specialist — Workplace Analytics
Company: WorkInSync (MoveInSync)

Assessment Scenario:
  Facility Manager running 3 offices across 3 countries.
  Total headcount: 2,000 employees.
  Policy: Hybrid attendance of 3 days/week.
  Goal: Determine Min-Max seats required with rigorous reasoning, and define
        enterprise Facilities Management KPIs.

Models Simulated:
  1. Theoretical Minimum (Uniform Cohorting): Perfect scheduling across 5 days.
  2. Realistic Enterprise Peak (Organic TWaT Clustering): Tue-Wed-Thu peak clustering.
  3. Theoretical Maximum (Synchronized / Dedicated): 100% headcount on all-hands.
  4. Recommended WorkInSync Hot-Desking Model: Cohorting + 15% dynamic buffer.
"""

import json
from dataclasses import dataclass
from typing import Dict, List, Tuple, Any

@dataclass
class OfficeProfile:
    country: str
    city: str
    headcount: int
    annual_cost_per_desk_usd: float

class WorkplaceCapacityPlanner:
    def __init__(self, offices: List[OfficeProfile] = None):
        if offices is None:
            # Representative 3-country enterprise split totaling 2,000 headcount
            self.offices = [
                OfficeProfile(country="India", city="Bangalore", headcount=1000, annual_cost_per_desk_usd=2500.0),
                OfficeProfile(country="USA", city="New York", headcount=600, annual_cost_per_desk_usd=8500.0),
                OfficeProfile(country="UK", city="London", headcount=400, annual_cost_per_desk_usd=7200.0)
            ]
        else:
            self.offices = offices

        self.total_headcount = sum(o.headcount for o in self.offices)
        self.days_per_week = 3  # Required in-office days per employee
        self.workdays_per_week = 5  # Standard Mon-Fri operating week

    def calculate_bounds(self, dynamic_buffer_pct: float = 0.15) -> Dict[str, Any]:
        """
        Calculates the complete mathematical range from theoretical floor to ceiling.
        """
        # Total person-days of desk demand per week
        total_person_days = self.total_headcount * self.days_per_week  # 2000 * 3 = 6000

        # Model 1: Theoretical Absolute Minimum (Uniform Staggering)
        # S_min = Total Person Days / Operating Days = 6,000 / 5 = 1,200
        min_seats_uniform = total_person_days / self.workdays_per_week
        min_sharing_ratio = self.total_headcount / min_seats_uniform  # 1.67:1

        # Model 2: Recommended WorkInSync Managed Hybrid (Uniform + Dynamic Buffer)
        # S_optimal = 1,200 * (1 + 0.15) = 1,380 seats
        optimal_seats = min_seats_uniform * (1.0 + dynamic_buffer_pct)
        optimal_sharing_ratio = self.total_headcount / optimal_seats  # 1.45:1

        # Model 3: Unmanaged Organic Peak (TWaT Effect: Tue/Wed/Thu ~ 85% peak)
        peak_attendance_rate = 0.85
        unmanaged_peak_seats = self.total_headcount * peak_attendance_rate  # 1,700 seats
        unmanaged_sharing_ratio = self.total_headcount / unmanaged_peak_seats  # 1.18:1

        # Model 4: Theoretical Absolute Maximum (Fully Synchronized / 1:1 Dedicated)
        max_seats_dedicated = float(self.total_headcount)  # 2,000 seats
        max_sharing_ratio = 1.0  # 1:1

        # Financial Calculations (Real Estate OPEX Savings)
        # Blended annual cost per desk across the 3 countries
        total_cost_1to1 = sum(o.headcount * o.annual_cost_per_desk_usd for o in self.offices)
        blended_cost_per_desk = total_cost_1to1 / self.total_headcount

        cost_at_dedicated = max_seats_dedicated * blended_cost_per_desk
        cost_at_optimal = optimal_seats * blended_cost_per_desk
        cost_at_uniform = min_seats_uniform * blended_cost_per_desk

        annual_savings_optimal = cost_at_dedicated - cost_at_optimal
        annual_savings_min = cost_at_dedicated - cost_at_uniform

        # Per-Office Breakdown
        office_breakdown = []
        for o in self.offices:
            o_min = (o.headcount * self.days_per_week) / self.workdays_per_week
            o_opt = o_min * (1.0 + dynamic_buffer_pct)
            o_peak = o.headcount * peak_attendance_rate
            o_max = o.headcount
            o_savings = (o_max - o_opt) * o.annual_cost_per_desk_usd

            office_breakdown.append({
                "country": o.country,
                "city": o.city,
                "headcount": o.headcount,
                "min_seats": int(round(o_min)),
                "optimal_seats": int(round(o_opt)),
                "unmanaged_peak_seats": int(round(o_peak)),
                "max_dedicated_seats": int(round(o_max)),
                "annual_savings_usd": round(o_savings, 2)
            })

        return {
            "headcount_total": self.total_headcount,
            "days_per_week_policy": self.days_per_week,
            "weekly_person_days": int(total_person_days),
            "theoretical_min_seats": int(min_seats_uniform),
            "theoretical_min_sharing_ratio": round(min_sharing_ratio, 2),
            "optimal_managed_seats": int(optimal_seats),
            "optimal_sharing_ratio": round(optimal_sharing_ratio, 2),
            "unmanaged_peak_seats": int(unmanaged_peak_seats),
            "unmanaged_sharing_ratio": round(unmanaged_sharing_ratio, 2),
            "theoretical_max_seats": int(max_seats_dedicated),
            "blended_cost_per_desk_usd": round(blended_cost_per_desk, 2),
            "annual_opex_savings_optimal_usd": round(annual_savings_optimal, 2),
            "annual_opex_savings_min_usd": round(annual_savings_min, 2),
            "office_distribution": office_breakdown
        }

def run_cli():
    print("================================================================================")
    print("  WORKINSYNC (BY MOVEINSYNC) MULTI-COUNTRY CAPACITY SIZING ENGINE")
    print("================================================================================\n")
    planner = WorkplaceCapacityPlanner()
    res = planner.calculate_bounds()

    print(f"Total Enterprise Headcount: {res['headcount_total']} employees across 3 countries")
    print(f"Policy: {res['days_per_week_policy']} days in-office per week -> {res['weekly_person_days']} desk-days/week\n")

    print(f"1. THEORETICAL MINIMUM (Perfect Cohorting):    {res['theoretical_min_seats']:,} Seats (Sharing Ratio {res['theoretical_min_sharing_ratio']}:1)")
    print(f"2. RECOMMENDED OPTIMAL (WorkInSync + 15% Buffer): {res['optimal_managed_seats']:,} Seats (Sharing Ratio {res['optimal_sharing_ratio']}:1)")
    print(f"3. UNMANAGED ORGANIC PEAK (TWaT Effect 85%):   {res['unmanaged_peak_seats']:,} Seats (Sharing Ratio {res['unmanaged_sharing_ratio']}:1)")
    print(f"4. THEORETICAL MAXIMUM (1:1 Dedicated Desks):   {res['theoretical_max_seats']:,} Seats (Sharing Ratio 1.00:1)\n")

    print(f"💰 Financial Real Estate Optimization:")
    print(f"   • Total Annual OPEX at 1:1 Dedicated:  ${res['theoretical_max_seats'] * res['blended_cost_per_desk_usd']:,.2f}")
    print(f"   • Total Annual OPEX with WorkInSync:   ${res['optimal_managed_seats'] * res['blended_cost_per_desk_usd']:,.2f}")
    print(f"   • Net Annual Real Estate Savings:       ${res['annual_opex_savings_optimal_usd']:,.2f}/year\n")

    print("📊 Multi-Country Office Allocation Table:")
    print(f"{'Country':<10} | {'City':<12} | {'Headcount':<10} | {'Min':<6} | {'Optimal':<8} | {'Peak':<6} | {'Max':<6} | {'Annual Savings'}")
    print("-" * 88)
    for o in res["office_distribution"]:
        print(f"{o['country']:<10} | {o['city']:<12} | {o['headcount']:<10} | {o['min_seats']:<6} | {o['optimal_seats']:<8} | {o['unmanaged_peak_seats']:<6} | {o['max_dedicated_seats']:<6} | ${o['annual_savings_usd']:,.2f}")
    print("=" * 88)

if __name__ == "__main__":
    run_cli()
