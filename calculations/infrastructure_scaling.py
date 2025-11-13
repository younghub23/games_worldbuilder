#!/usr/bin/env python3
"""
Infrastructure Scaling Cost Calculator
Project infrastructure costs based on DAU growth
"""

import json
import argparse
from pathlib import Path


class InfrastructureCalculator:
    """Calculate infrastructure scaling costs"""

    def __init__(self, data_path="../data"):
        self.data_path = Path(data_path)
        self.load_data()

    def load_data(self):
        """Load cost and benchmark data from JSON files"""
        with open(self.data_path / "cost_projections.json") as f:
            self.costs = json.load(f)

        with open(self.data_path / "market_benchmarks.json") as f:
            self.benchmarks = json.load(f)

    def estimate_infrastructure_cost(self, dau):
        """
        Estimate monthly infrastructure cost based on DAU

        Args:
            dau: Daily active users

        Returns:
            dict: Cost breakdown by service
        """
        # Use benchmark cost per DAU
        benchmarks = self.benchmarks['infrastructure_benchmarks']['cost_per_dau']

        # Start with average efficiency
        cost_per_dau = benchmarks['average']['per_dau_monthly']

        # Scale factors (economies of scale)
        if dau < 10000:
            scale_factor = 1.2  # Less efficient at small scale
        elif dau < 50000:
            scale_factor = 1.0
        elif dau < 200000:
            scale_factor = 0.9
        elif dau < 500000:
            scale_factor = 0.8
        else:
            scale_factor = 0.7  # More efficient at large scale

        base_cost = dau * cost_per_dau * scale_factor

        # Breakdown by service (rough percentages)
        return {
            "dau": dau,
            "total_monthly_cost": base_cost,
            "cost_per_dau": base_cost / dau if dau > 0 else 0,
            "breakdown": {
                "compute": base_cost * 0.40,
                "database": base_cost * 0.25,
                "storage": base_cost * 0.10,
                "cdn": base_cost * 0.15,
                "other_services": base_cost * 0.10
            },
            "scale_factor": scale_factor
        }

    def project_growth_costs(self, starting_dau, target_dau, months):
        """
        Project infrastructure costs during growth period

        Args:
            starting_dau: Starting DAU
            target_dau: Target DAU
            months: Months to reach target

        Returns:
            dict: Month-by-month cost projections
        """
        # Linear growth assumption (could be made more sophisticated)
        monthly_growth = (target_dau - starting_dau) / months

        projections = []
        total_cost = 0

        for month in range(1, months + 1):
            current_dau = starting_dau + (monthly_growth * month)
            month_cost = self.estimate_infrastructure_cost(int(current_dau))

            projections.append({
                "month": month,
                "dau": int(current_dau),
                "monthly_cost": month_cost['total_monthly_cost'],
                "cost_per_dau": month_cost['cost_per_dau']
            })

            total_cost += month_cost['total_monthly_cost']

        average_monthly_cost = total_cost / months

        return {
            "starting_dau": starting_dau,
            "target_dau": target_dau,
            "months": months,
            "total_infrastructure_cost": total_cost,
            "average_monthly_cost": average_monthly_cost,
            "final_monthly_cost": projections[-1]['monthly_cost'],
            "monthly_projections": projections
        }

    def calculate_optimization_savings(self, dau, current_efficiency="average"):
        """
        Calculate potential savings from infrastructure optimization

        Args:
            dau: Daily active users
            current_efficiency: Current efficiency level
                              ('inefficient', 'average', 'efficient')

        Returns:
            dict: Optimization opportunities and savings
        """
        benchmarks = self.benchmarks['infrastructure_benchmarks']['cost_per_dau']

        current_cost_per_dau = benchmarks[current_efficiency]['per_dau_monthly']
        efficient_cost_per_dau = benchmarks['efficient']['per_dau_monthly']

        current_monthly_cost = dau * current_cost_per_dau
        optimized_monthly_cost = dau * efficient_cost_per_dau

        monthly_savings = current_monthly_cost - optimized_monthly_cost
        annual_savings = monthly_savings * 12
        savings_percentage = (monthly_savings / current_monthly_cost * 100
                             if current_monthly_cost > 0 else 0)

        optimizations = [
            {
                "strategy": "Reserved Instances",
                "potential_savings": monthly_savings * 0.30,
                "implementation_effort": "Low"
            },
            {
                "strategy": "Aggressive Caching",
                "potential_savings": monthly_savings * 0.25,
                "implementation_effort": "Medium"
            },
            {
                "strategy": "Database Query Optimization",
                "potential_savings": monthly_savings * 0.20,
                "implementation_effort": "Medium"
            },
            {
                "strategy": "Asset CDN Optimization",
                "potential_savings": monthly_savings * 0.15,
                "implementation_effort": "Low"
            },
            {
                "strategy": "Auto-scaling Tuning",
                "potential_savings": monthly_savings * 0.10,
                "implementation_effort": "Medium"
            }
        ]

        return {
            "dau": dau,
            "current_efficiency": current_efficiency,
            "current_monthly_cost": current_monthly_cost,
            "optimized_monthly_cost": optimized_monthly_cost,
            "monthly_savings": monthly_savings,
            "annual_savings": annual_savings,
            "savings_percentage": savings_percentage,
            "optimization_strategies": optimizations
        }

    def calculate_third_party_costs(self, dau, paying_users):
        """
        Calculate third-party service costs

        Args:
            dau: Daily active users
            paying_users: Number of paying users

        Returns:
            dict: Third-party service costs
        """
        # Base costs from data
        base_costs = self.costs['third_party_services']['breakdown']

        # Analytics scales with DAU
        analytics_base = (base_costs['analytics_monitoring']['firebase_google_analytics'] +
                         base_costs['analytics_monitoring']['mixpanel_amplitude'] +
                         base_costs['analytics_monitoring']['crash_reporting'] +
                         base_costs['analytics_monitoring']['performance_monitoring'])

        # Scale analytics costs
        if dau < 50000:
            analytics_cost = analytics_base
        elif dau < 200000:
            analytics_cost = analytics_base * 1.5
        elif dau < 500000:
            analytics_cost = analytics_base * 2.5
        else:
            analytics_cost = analytics_base * 4.0

        # Backend services scale with active users
        backend_base = (base_costs['backend_services']['authentication'] +
                       base_costs['backend_services']['push_notifications'] +
                       base_costs['backend_services']['customer_support'])

        if dau < 50000:
            backend_cost = backend_base
        elif dau < 200000:
            backend_cost = backend_base * 2
        elif dau < 500000:
            backend_cost = backend_base * 3
        else:
            backend_cost = backend_base * 5

        # Payment processing (2.9% of revenue)
        # Estimate based on paying users
        estimated_monthly_revenue = paying_users * 100  # Rough estimate
        payment_processing = estimated_monthly_revenue * 0.029

        # Development tools (relatively fixed)
        dev_tools = (base_costs['development_tools']['github_enterprise'] +
                    base_costs['development_tools']['ci_cd'] +
                    base_costs['development_tools']['testing_platforms'])

        total = analytics_cost + backend_cost + payment_processing + dev_tools

        return {
            "dau": dau,
            "paying_users": paying_users,
            "total_monthly_cost": total,
            "breakdown": {
                "analytics_monitoring": analytics_cost,
                "backend_services": backend_cost,
                "payment_processing": payment_processing,
                "development_tools": dev_tools
            }
        }

    def format_currency(self, amount):
        """Format amount as currency"""
        if amount >= 1_000_000:
            return f"${amount / 1_000_000:.2f}M"
        elif amount >= 1_000:
            return f"${amount / 1_000:.0f}K"
        else:
            return f"${amount:.2f}"

    def print_infrastructure_estimate(self, dau):
        """Print infrastructure cost estimate for given DAU"""
        result = self.estimate_infrastructure_cost(dau)

        print(f"\n{'='*60}")
        print(f"INFRASTRUCTURE COST ESTIMATE")
        print(f"{'='*60}")
        print(f"\nDAU: {result['dau']:,}")
        print(f"Total Monthly Cost: {self.format_currency(result['total_monthly_cost'])}")
        print(f"Cost per DAU: ${result['cost_per_dau']:.2f}")
        print(f"Scale Efficiency: {result['scale_factor']:.2f}x")

        print(f"\nCost Breakdown:")
        for service, cost in result['breakdown'].items():
            percentage = (cost / result['total_monthly_cost'] * 100
                         if result['total_monthly_cost'] > 0 else 0)
            print(f"  {service.replace('_', ' ').title():<20} "
                  f"{self.format_currency(cost):>10} ({percentage:>5.1f}%)")

        print(f"{'='*60}\n")

    def print_growth_projection(self, starting_dau, target_dau, months):
        """Print infrastructure cost projections during growth"""
        result = self.project_growth_costs(starting_dau, target_dau, months)

        print(f"\n{'='*60}")
        print(f"INFRASTRUCTURE GROWTH PROJECTION")
        print(f"{'='*60}")
        print(f"\nGrowth Plan: {starting_dau:,} → {target_dau:,} DAU over {months} months")

        print(f"\nSummary:")
        print(f"  Total Infrastructure Cost: {self.format_currency(result['total_infrastructure_cost'])}")
        print(f"  Average Monthly Cost:      {self.format_currency(result['average_monthly_cost'])}")
        print(f"  Final Monthly Cost:        {self.format_currency(result['final_monthly_cost'])}")

        print(f"\nMonthly Breakdown:")
        print(f"{'Month':<8} {'DAU':<12} {'Monthly Cost':<15} {'Cost/DAU':<12}")
        print(f"{'-'*50}")

        for proj in result['monthly_projections']:
            if proj['month'] % 3 == 1 or proj['month'] == months:  # Show every 3 months
                print(f"{proj['month']:<8} "
                      f"{proj['dau']:<12,} "
                      f"{self.format_currency(proj['monthly_cost']):<15} "
                      f"${proj['cost_per_dau']:<11.2f}")

        print(f"{'='*60}\n")

    def print_optimization_analysis(self, dau, current_efficiency="average"):
        """Print optimization opportunities"""
        result = self.calculate_optimization_savings(dau, current_efficiency)

        print(f"\n{'='*60}")
        print(f"INFRASTRUCTURE OPTIMIZATION ANALYSIS")
        print(f"{'='*60}")
        print(f"\nCurrent State:")
        print(f"  DAU:               {result['dau']:,}")
        print(f"  Efficiency Level:  {result['current_efficiency'].title()}")
        print(f"  Monthly Cost:      {self.format_currency(result['current_monthly_cost'])}")

        print(f"\nOptimized State:")
        print(f"  Monthly Cost:      {self.format_currency(result['optimized_monthly_cost'])}")
        print(f"  Monthly Savings:   {self.format_currency(result['monthly_savings'])} "
              f"({result['savings_percentage']:.1f}%)")
        print(f"  Annual Savings:    {self.format_currency(result['annual_savings'])}")

        print(f"\nOptimization Strategies:")
        print(f"{'Strategy':<30} {'Savings':<15} {'Effort':<15}")
        print(f"{'-'*60}")

        for opt in result['optimization_strategies']:
            print(f"{opt['strategy']:<30} "
                  f"{self.format_currency(opt['potential_savings']):<15} "
                  f"{opt['implementation_effort']:<15}")

        print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Calculate infrastructure scaling costs"
    )
    parser.add_argument(
        "--analysis",
        choices=["estimate", "growth", "optimize", "all"],
        default="estimate",
        help="Type of analysis to run"
    )
    parser.add_argument(
        "--dau",
        type=int,
        default=100000,
        help="Current or target DAU"
    )
    parser.add_argument(
        "--starting-dau",
        type=int,
        default=10000,
        help="Starting DAU for growth projection"
    )
    parser.add_argument(
        "--target-dau",
        type=int,
        default=200000,
        help="Target DAU for growth projection"
    )
    parser.add_argument(
        "--months",
        type=int,
        default=12,
        help="Months for growth projection"
    )
    parser.add_argument(
        "--efficiency",
        choices=["inefficient", "average", "efficient"],
        default="average",
        help="Current infrastructure efficiency level"
    )

    args = parser.parse_args()

    calculator = InfrastructureCalculator()

    if args.analysis in ["estimate", "all"]:
        calculator.print_infrastructure_estimate(args.dau)

    if args.analysis in ["growth", "all"]:
        calculator.print_growth_projection(
            args.starting_dau,
            args.target_dau,
            args.months
        )

    if args.analysis in ["optimize", "all"]:
        calculator.print_optimization_analysis(args.dau, args.efficiency)


if __name__ == "__main__":
    main()
