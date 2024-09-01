from dataclasses import dataclass, field
import pandas as pd


@dataclass
class Portfolio:
    """
    The Portfolio class is responsible for storing and managing the results of multiple DCA simulations.
    """

    results_df: pd.DataFrame = field(
        default_factory=lambda: pd.DataFrame(
            columns=["Company", "Start Date", "Frequency", "Percentage Increase"]
        )
    )

    def add_simulation_result(
        self,
        company_name: str,
        start_date: pd.Timestamp,
        investment: float,
        frequency: str,
        custom_interval: int,
        percentage_increase: float,
        fee: float,
    ):
        """
        Add the result of a new DCA simulation to the portfolio.
        """
        new_row = pd.DataFrame(
            {
                "Company": [company_name],
                "Start Date": [start_date],
                "Investment": [investment],
                "Frequency": [frequency],
                "Custom Interval": [custom_interval],
                "Fee": [fee],
                "Percentage Increase": [percentage_increase],
            }
        )
        self.results_df = pd.concat([self.results_df, new_row], ignore_index=True)

        # Reorder the columns to ensure the specified order
        self.results_df = self.results_df[
            [
                "Company",
                "Start Date",
                "Investment",
                "Frequency",
                "Custom Interval",
                "Fee",
                "Percentage Increase",
            ]
        ]

    def get_results(self) -> pd.DataFrame:
        """
        Return the DataFrame containing all simulation results.
        """
        return self.results_df

    def clear_results(self):
        """
        Clear all results from the portfolio.
        """
        self.results_df = pd.DataFrame(
            columns=["Company", "Start Date", "Frequency", "Percentage Increase"]
        )
