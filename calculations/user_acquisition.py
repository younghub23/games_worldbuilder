#!/usr/bin/env python3
"""
User Acquisition Cost Calculator
Calculate and project user acquisition costs and effectiveness
"""

import json
import argparse
from pathlib import Path


class UACalculator:
    """Calculate user acquisition metrics and costs"""

    def __init__(self, data_path="../data"):
        self.data_path = Path(data_path)
        self.load_data()

    def load_data(self):
        """Load cost and revenue data from JSON files"""
        with open(self.data_path / "cost_projections.json") as f:
            self.costs = json.load(f)

        with open(self.data_path / "revenue_models.json") as f:
            self.revenues = json.load(f)

        with open(self.data_path / "market_benchmarks.json") as f:
            self.benchmarks = json.load(f)

    def calculate_effective_cpi(self, blended_cpi, d1_retention):
        """
        Calculate effective CPI based on D1 retention

        Args:
            blended_cpi: Average cost per install across all channels
            d1_retention: Day 1 retention rate (0-1)

        Returns:
            float: Effective cost per retained user
        """
        return blended_cpi / d1_retention if d1_retention > 0 else float('inf')

    def calculate_ltv(self, d30_users, paying_conversion, arppu, lifetime_months=12):
        """
        Calculate Lifetime Value (LTV) for a cohort

        Args:
            d30_users: Number of D30 retained users
            paying_conversion: Percentage of users who pay (0-1)
            arppu: Average Revenue Per Paying User (monthly)
            lifetime_months: Average user lifetime in months

        Returns:
            dict: LTV analysis
        """
        paying_users = d30_users * paying_conversion
        total_lifetime_revenue = paying_users * arppu * lifetime_months
        ltv_per_user = total_lifetime_revenue / d30_users if d30_users > 0 else 0
        ltv_per_paying_user = arppu * lifetime_months

        return {
            "d30_users": d30_users,
            "paying_users": int(paying_users),
            "paying_conversion": paying_conversion,
            "arppu": arppu,
            "lifetime_months": lifetime_months,
            "total_lifetime_revenue": total_lifetime_revenue,
            "ltv_per_user": ltv_per_user,
            "ltv_per_paying_user": ltv_per_paying_user
        }

    def calculate_payback_period(self, cpi, ltv_per_user, monthly_revenue_per_user):
        """
        Calculate time to recover user acquisition cost

        Args:
            cpi: Cost per install
            ltv_per_user: Lifetime value per user
            monthly_revenue_per_user: Average monthly revenue per user

        Returns:
            dict: Payback analysis
        """
        if monthly_revenue_per_user <= 0:
            return {
                "pays_back": False,
                "reason": "No revenue per user"
            }

        months_to_payback = cpi / monthly_revenue_per_user

        if ltv_per_user < cpi:
            return {
                "pays_back": False,
                "reason": "LTV is less than CPI",
                "ltv": ltv_per_user,
                "cpi": cpi,
                "deficit": cpi - ltv_per_user
            }

        return {
            "pays_back": True,
            "months": months_to_payback,
            "cpi": cpi,
            "ltv": ltv_per_user,
            "total_profit_per_user": ltv_per_user - cpi,
            "roi_multiple": ltv_per_user / cpi if cpi > 0 else 0
        }

    def calculate_ua_budget(self, target_dau, d1_retention, d30_retention,
                           cpi, months_to_reach_target=6):
        """
        Calculate required UA budget to reach target DAU

        Args:
            target_dau: Target daily active users
            d1_retention: Day 1 retention rate (0-1)
            d30_retention: Day 30 retention rate (0-1)
            cpi: Cost per install
            months_to_reach_target: Time to reach target

        Returns:
            dict: UA budget analysis
        """
        # Need to account for churn, so we need continuous acquisition
        # Assume target_dau represents D30 users
        installs_needed = target_dau / d30_retention if d30_retention > 0 else float('inf')

        # Total installs over the period
        total_installs = installs_needed

        # Budget calculation
        total_budget = total_installs * cpi
        monthly_budget = total_budget / months_to_reach_target

        # Installs per month
        monthly_installs = total_installs / months_to_reach_target
        monthly_d1_retained = monthly_installs * d1_retention
        monthly_d30_retained = monthly_installs * d30_retention

        return {
            "target_dau": target_dau,
            "months_to_reach": months_to_reach_target,
            "total_installs_needed": int(total_installs),
            "cpi": cpi,
            "total_budget": total_budget,
            "monthly_budget": monthly_budget,
            "monthly_installs": int(monthly_installs),
            "monthly_d1_retained": int(monthly_d1_retained),
            "monthly_d30_retained": int(monthly_d30_retained),
            "d1_retention": d1_retention,
            "d30_retention": d30_retention
        }

    def calculate_channel_mix(self, total_budget, channels):
        """
        Calculate optimal channel mix for UA budget

        Args:
            total_budget: Total UA budget
            channels: Dict of channel names to CPI and expected volume

        Returns:
            dict: Channel allocation recommendations
        """
        # Sort channels by CPI (ascending)
        sorted_channels = sorted(channels.items(),
                                key=lambda x: x[1]['cpi'])

        allocations = []
        remaining_budget = total_budget

        for channel_name, channel_data in sorted_channels:
            cpi = channel_data['cpi']
            max_monthly_volume = channel_data.get('max_monthly_volume', float('inf'))

            # Calculate max spend for this channel
            max_channel_spend = max_monthly_volume * cpi

            # Allocate proportionally or up to max
            if remaining_budget > max_channel_spend:
                allocation = max_channel_spend
            else:
                allocation = remaining_budget

            installs = int(allocation / cpi) if cpi > 0 else 0

            allocations.append({
                "channel": channel_name,
                "cpi": cpi,
                "budget_allocation": allocation,
                "expected_installs": installs,
                "percentage_of_budget": (allocation / total_budget * 100) if total_budget > 0 else 0
            })

            remaining_budget -= allocation

            if remaining_budget <= 0:
                break

        total_expected_installs = sum(a['expected_installs'] for a in allocations)
        blended_cpi = total_budget / total_expected_installs if total_expected_installs > 0 else 0

        return {
            "total_budget": total_budget,
            "total_expected_installs": total_expected_installs,
            "blended_cpi": blended_cpi,
            "channel_allocations": allocations
        }

    def format_currency(self, amount):
        """Format amount as currency"""
        if amount >= 1_000_000:
            return f"${amount / 1_000_000:.2f}M"
        elif amount >= 1_000:
            return f"${amount / 1_000:.0f}K"
        else:
            return f"${amount:.2f}"

    def print_ua_budget_analysis(self, target_dau, cpi=2.5, d1_retention=0.40,
                                 d30_retention=0.08, months=6):
        """Print UA budget analysis"""
        result = self.calculate_ua_budget(
            target_dau, d1_retention, d30_retention, cpi, months
        )

        print(f"\n{'='*60}")
        print("USER ACQUISITION BUDGET ANALYSIS")
        print(f"{'='*60}")
        print(f"\nTarget: {result['target_dau']:,} D30 users in {months} months")
        print(f"\nRetention Assumptions:")
        print(f"  D1 Retention:  {d1_retention*100:.1f}%")
        print(f"  D30 Retention: {d30_retention*100:.1f}%")
        print(f"  CPI:           ${cpi:.2f}")

        print(f"\nBudget Requirements:")
        print(f"  Total Installs Needed: {result['total_installs_needed']:,}")
        print(f"  Total Budget:          {self.format_currency(result['total_budget'])}")
        print(f"  Monthly Budget:        {self.format_currency(result['monthly_budget'])}")

        print(f"\nMonthly Metrics:")
        print(f"  Installs:      {result['monthly_installs']:,}")
        print(f"  D1 Retained:   {result['monthly_d1_retained']:,}")
        print(f"  D30 Retained:  {result['monthly_d30_retained']:,}")
        print(f"{'='*60}\n")

    def print_ltv_analysis(self, d30_users=10000, paying_conversion=0.03,
                          arppu=100, lifetime_months=12):
        """Print LTV analysis"""
        result = self.calculate_ltv(d30_users, paying_conversion, arppu, lifetime_months)

        print(f"\n{'='*60}")
        print("LIFETIME VALUE (LTV) ANALYSIS")
        print(f"{'='*60}")
        print(f"\nCohort Size: {d30_users:,} D30 users")
        print(f"Paying Conversion: {paying_conversion*100:.1f}%")
        print(f"ARPPU: {self.format_currency(arppu)}/month")
        print(f"Lifetime: {lifetime_months} months")

        print(f"\nResults:")
        print(f"  Paying Users:          {result['paying_users']:,}")
        print(f"  LTV per User:          {self.format_currency(result['ltv_per_user'])}")
        print(f"  LTV per Paying User:   {self.format_currency(result['ltv_per_paying_user'])}")
        print(f"  Total Cohort Revenue:  {self.format_currency(result['total_lifetime_revenue'])}")
        print(f"{'='*60}\n")

    def print_payback_analysis(self, cpi=2.5, ltv_per_user=15,
                              monthly_revenue_per_user=1.5):
        """Print payback period analysis"""
        result = self.calculate_payback_period(cpi, ltv_per_user, monthly_revenue_per_user)

        print(f"\n{'='*60}")
        print("PAYBACK PERIOD ANALYSIS")
        print(f"{'='*60}")
        print(f"\nInputs:")
        print(f"  CPI:                     ${cpi:.2f}")
        print(f"  LTV per User:            {self.format_currency(ltv_per_user)}")
        print(f"  Monthly Revenue/User:    {self.format_currency(monthly_revenue_per_user)}")

        print(f"\nResults:")
        if result["pays_back"]:
            print(f"  ✓ Pays back!")
            print(f"  Payback Period:        {result['months']:.1f} months")
            print(f"  Profit per User:       {self.format_currency(result['total_profit_per_user'])}")
            print(f"  ROI Multiple:          {result['roi_multiple']:.2f}x")
        else:
            print(f"  ✗ Does not pay back")
            print(f"  Reason: {result['reason']}")
            if 'deficit' in result:
                print(f"  Loss per User:         {self.format_currency(result['deficit'])}")

        print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Calculate user acquisition costs and metrics"
    )
    parser.add_argument(
        "--analysis",
        choices=["budget", "ltv", "payback", "all"],
        default="all",
        help="Type of analysis to run"
    )
    parser.add_argument(
        "--target-dau",
        type=int,
        default=100000,
        help="Target D30 DAU for budget analysis"
    )
    parser.add_argument(
        "--cpi",
        type=float,
        default=2.5,
        help="Cost per install"
    )
    parser.add_argument(
        "--d1-retention",
        type=float,
        default=0.40,
        help="D1 retention rate (0-1)"
    )
    parser.add_argument(
        "--d30-retention",
        type=float,
        default=0.08,
        help="D30 retention rate (0-1)"
    )
    parser.add_argument(
        "--months",
        type=int,
        default=6,
        help="Months to reach target"
    )
    parser.add_argument(
        "--paying-conversion",
        type=float,
        default=0.03,
        help="Paying conversion rate (0-1)"
    )
    parser.add_argument(
        "--arppu",
        type=float,
        default=100,
        help="Average revenue per paying user (monthly)"
    )
    parser.add_argument(
        "--lifetime-months",
        type=int,
        default=12,
        help="Average user lifetime in months"
    )

    args = parser.parse_args()

    calculator = UACalculator()

    if args.analysis in ["budget", "all"]:
        calculator.print_ua_budget_analysis(
            args.target_dau,
            args.cpi,
            args.d1_retention,
            args.d30_retention,
            args.months
        )

    if args.analysis in ["ltv", "all"]:
        d30_users = int(args.target_dau * args.d30_retention / args.d1_retention)
        calculator.print_ltv_analysis(
            d30_users,
            args.paying_conversion,
            args.arppu,
            args.lifetime_months
        )

    if args.analysis in ["payback", "all"]:
        # Calculate LTV and monthly revenue per user
        ltv_result = calculator.calculate_ltv(
            10000,  # Sample size
            args.paying_conversion,
            args.arppu,
            args.lifetime_months
        )
        ltv_per_user = ltv_result['ltv_per_user']
        monthly_revenue_per_user = ltv_per_user / args.lifetime_months

        calculator.print_payback_analysis(
            args.cpi,
            ltv_per_user,
            monthly_revenue_per_user
        )


if __name__ == "__main__":
    main()
