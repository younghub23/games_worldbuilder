#!/usr/bin/env python3
"""
ROI Calculator for Mobile Game Development
Calculates return on investment based on various success scenarios
"""

import json
import argparse
from pathlib import Path


class ROICalculator:
    """Calculate ROI for mobile game investments"""

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

    def calculate_scenario_roi(self, scenario="moderate_success", years=5):
        """
        Calculate ROI for a given success scenario

        Args:
            scenario: One of 'failure', 'modest_success', 'moderate_success',
                     'major_success', 'breakout_hit'
            years: Number of years to project

        Returns:
            dict: ROI analysis with costs, revenue, profit, and ROI percentage
        """
        prob_data = self.revenues["outcome_probabilities"][scenario]

        # Get scenario parameters
        if scenario == "failure":
            total_loss = (prob_data["total_loss"]["min"] +
                         prob_data["total_loss"]["max"]) / 2
            return {
                "scenario": scenario,
                "probability": prob_data["probability"],
                "years": years,
                "total_investment": abs(total_loss),
                "total_revenue": 0,
                "net_profit": total_loss,
                "roi_percentage": -100,
                "outcome": "Failure - Total Loss"
            }

        # Calculate for success scenarios
        if scenario == "modest_success":
            yearly_revenue = (prob_data["monthly_revenue_range"]["min"] +
                             prob_data["monthly_revenue_range"]["max"]) / 2 * 12
            break_even_year = (prob_data["break_even_years"]["min"] +
                              prob_data["break_even_years"]["max"]) / 2
        elif scenario == "moderate_success":
            yearly_revenue = (prob_data["monthly_revenue_range"]["min"] +
                             prob_data["monthly_revenue_range"]["max"]) / 2 * 12
            break_even_year = (prob_data["break_even_years"]["min"] +
                              prob_data["break_even_years"]["max"]) / 2
        elif scenario == "major_success":
            yearly_revenue = (prob_data["monthly_revenue_range"]["min"] +
                             prob_data["monthly_revenue_range"]["max"]) / 2 * 12
            break_even_year = (prob_data["break_even_years"]["min"] +
                              prob_data["break_even_years"]["max"]) / 2
        else:  # breakout_hit
            yearly_revenue = 240000000  # $20M/month average
            break_even_year = 0.83  # ~10 months

        # Estimate costs
        year_1_costs = self.revenues["yearly_financials"]["year_1_moderate_path"]["costs"]["total"]
        year_2_costs = self.revenues["yearly_financials"]["year_2_moderate_path"]["costs"]["total"]
        year_3_plus_costs = self.revenues["yearly_financials"]["year_3_moderate_path"]["costs"]["total"]

        # Scale costs based on scenario
        if scenario in ["major_success", "breakout_hit"]:
            year_3_plus_costs *= 1.5  # Higher operational costs at scale

        # Calculate total costs and revenue
        total_costs = year_1_costs + year_2_costs + (year_3_plus_costs * (years - 2))

        # Revenue ramps up over time
        total_revenue = 0
        for year in range(1, years + 1):
            if year <= break_even_year:
                # Ramp up period
                year_revenue = yearly_revenue * (year / break_even_year) * 0.5
            else:
                # Post break-even
                year_revenue = yearly_revenue * (1 + (year - break_even_year) * 0.1)  # 10% growth
            total_revenue += year_revenue

        net_profit = total_revenue - total_costs
        roi_percentage = (net_profit / total_costs) * 100 if total_costs > 0 else 0

        return {
            "scenario": scenario,
            "probability": prob_data["probability"],
            "years": years,
            "total_investment": total_costs,
            "total_revenue": total_revenue,
            "net_profit": net_profit,
            "roi_percentage": roi_percentage,
            "break_even_year": break_even_year,
            "outcome": "Success" if net_profit > 0 else "Loss"
        }

    def calculate_expected_value(self, years=5):
        """
        Calculate probability-weighted expected value across all scenarios

        Returns:
            dict: Expected value analysis
        """
        scenarios = ["failure", "modest_success", "moderate_success",
                    "major_success", "breakout_hit"]

        weighted_results = []
        total_expected_profit = 0
        total_expected_revenue = 0
        total_expected_investment = 0

        for scenario in scenarios:
            result = self.calculate_scenario_roi(scenario, years)
            weighted_profit = result["net_profit"] * result["probability"]
            weighted_revenue = result["total_revenue"] * result["probability"]
            weighted_investment = result["total_investment"] * result["probability"]

            total_expected_profit += weighted_profit
            total_expected_revenue += weighted_revenue
            total_expected_investment += weighted_investment

            weighted_results.append({
                "scenario": scenario,
                "probability": result["probability"],
                "net_profit": result["net_profit"],
                "weighted_profit": weighted_profit
            })

        expected_roi = (total_expected_profit / total_expected_investment * 100
                       if total_expected_investment > 0 else 0)

        return {
            "years": years,
            "expected_investment": total_expected_investment,
            "expected_revenue": total_expected_revenue,
            "expected_profit": total_expected_profit,
            "expected_roi_percentage": expected_roi,
            "scenario_breakdown": weighted_results
        }

    def calculate_break_even_time(self, monthly_revenue, monthly_costs,
                                  initial_investment):
        """
        Calculate time to break even given revenue and cost projections

        Args:
            monthly_revenue: Average monthly revenue after platform fees
            monthly_costs: Average monthly operational costs
            initial_investment: Total pre-launch investment

        Returns:
            dict: Break-even analysis
        """
        monthly_profit = monthly_revenue - monthly_costs

        if monthly_profit <= 0:
            return {
                "breaks_even": False,
                "reason": "Monthly costs exceed revenue",
                "monthly_loss": abs(monthly_profit)
            }

        months_to_break_even = initial_investment / monthly_profit
        years_to_break_even = months_to_break_even / 12

        return {
            "breaks_even": True,
            "months": round(months_to_break_even, 1),
            "years": round(years_to_break_even, 2),
            "monthly_profit": monthly_profit,
            "initial_investment": initial_investment,
            "cumulative_profit_year_3": monthly_profit * 36 - initial_investment,
            "cumulative_profit_year_5": monthly_profit * 60 - initial_investment
        }

    def format_currency(self, amount):
        """Format amount as currency"""
        if amount >= 1_000_000:
            return f"${amount / 1_000_000:.2f}M"
        elif amount >= 1_000:
            return f"${amount / 1_000:.0f}K"
        else:
            return f"${amount:.2f}"

    def print_scenario_analysis(self, scenario="moderate_success", years=5):
        """Print detailed analysis for a scenario"""
        result = self.calculate_scenario_roi(scenario, years)

        print(f"\n{'='*60}")
        print(f"ROI Analysis: {scenario.upper().replace('_', ' ')}")
        print(f"{'='*60}")
        print(f"Probability: {result['probability']*100:.1f}%")
        print(f"Time Period: {years} years")
        print(f"\nFinancial Summary:")
        print(f"  Total Investment: {self.format_currency(result['total_investment'])}")
        print(f"  Total Revenue:    {self.format_currency(result['total_revenue'])}")
        print(f"  Net Profit/Loss:  {self.format_currency(result['net_profit'])}")
        print(f"  ROI:              {result['roi_percentage']:.1f}%")

        if result.get('break_even_year'):
            print(f"  Break-Even:       Year {result['break_even_year']:.1f}")

        print(f"  Outcome:          {result['outcome']}")
        print(f"{'='*60}\n")

    def print_expected_value_analysis(self, years=5):
        """Print expected value analysis across all scenarios"""
        result = self.calculate_expected_value(years)

        print(f"\n{'='*60}")
        print(f"EXPECTED VALUE ANALYSIS ({years} years)")
        print(f"{'='*60}")
        print(f"\nProbability-Weighted Outcome:")
        print(f"  Expected Investment: {self.format_currency(result['expected_investment'])}")
        print(f"  Expected Revenue:    {self.format_currency(result['expected_revenue'])}")
        print(f"  Expected Profit:     {self.format_currency(result['expected_profit'])}")
        print(f"  Expected ROI:        {result['expected_roi_percentage']:.1f}%")

        print(f"\nScenario Breakdown:")
        print(f"{'Scenario':<20} {'Probability':<15} {'Profit':<20} {'Weighted':<20}")
        print(f"{'-'*75}")

        for item in result['scenario_breakdown']:
            print(f"{item['scenario']:<20} "
                  f"{item['probability']*100:>6.1f}%         "
                  f"{self.format_currency(item['net_profit']):>15} "
                  f"{self.format_currency(item['weighted_profit']):>15}")

        print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Calculate ROI for mobile game development"
    )
    parser.add_argument(
        "--scenario",
        choices=["failure", "modest_success", "moderate_success",
                "major_success", "breakout_hit", "all", "expected"],
        default="expected",
        help="Success scenario to analyze"
    )
    parser.add_argument(
        "--years",
        type=int,
        default=5,
        help="Number of years to project"
    )
    parser.add_argument(
        "--break-even",
        action="store_true",
        help="Calculate break-even time with custom parameters"
    )
    parser.add_argument(
        "--monthly-revenue",
        type=float,
        help="Monthly revenue for break-even calculation"
    )
    parser.add_argument(
        "--monthly-costs",
        type=float,
        help="Monthly costs for break-even calculation"
    )
    parser.add_argument(
        "--investment",
        type=float,
        help="Initial investment for break-even calculation"
    )

    args = parser.parse_args()

    calculator = ROICalculator()

    if args.break_even:
        if not all([args.monthly_revenue, args.monthly_costs, args.investment]):
            print("Error: --break-even requires --monthly-revenue, --monthly-costs, and --investment")
            return

        result = calculator.calculate_break_even_time(
            args.monthly_revenue,
            args.monthly_costs,
            args.investment
        )

        print(f"\n{'='*60}")
        print("BREAK-EVEN ANALYSIS")
        print(f"{'='*60}")

        if result["breaks_even"]:
            print(f"✓ Break-even achieved!")
            print(f"  Time to break-even: {result['months']} months ({result['years']} years)")
            print(f"  Monthly profit: {calculator.format_currency(result['monthly_profit'])}")
            print(f"  Cumulative profit (Year 3): {calculator.format_currency(result['cumulative_profit_year_3'])}")
            print(f"  Cumulative profit (Year 5): {calculator.format_currency(result['cumulative_profit_year_5'])}")
        else:
            print(f"✗ Does not break even")
            print(f"  Reason: {result['reason']}")
            print(f"  Monthly loss: {calculator.format_currency(result['monthly_loss'])}")

        print(f"{'='*60}\n")
        return

    if args.scenario == "expected":
        calculator.print_expected_value_analysis(args.years)
    elif args.scenario == "all":
        scenarios = ["failure", "modest_success", "moderate_success",
                    "major_success", "breakout_hit"]
        for scenario in scenarios:
            calculator.print_scenario_analysis(scenario, args.years)
    else:
        calculator.print_scenario_analysis(args.scenario, args.years)


if __name__ == "__main__":
    main()
