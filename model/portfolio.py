from dataclasses import dataclass, field
import pandas as pd

@dataclass
class Portfolio:
    """
    The Portfolio class is responsible for storing and managing the results of multiple DCA simulations.
    """

    # Define columns as an instance variable
    COLUMNS: list = field(default_factory=lambda: [
        "Company",
        "Start Date",
        "Investment",
        "Frequency",
        "Custom Interval",
        "Fee",
        "Percentage Increase",
    ])

    results_df: pd.DataFrame = field(init=False)

    def __post_init__(self):
        # Initialize the results_df DataFrame with the defined columns
        self.results_df = pd.DataFrame(columns=self.COLUMNS)

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
        self.results_df = self.results_df[self.COLUMNS]

    def get_results(self) -> pd.DataFrame:
        """
        Return the DataFrame containing all simulation results.
        """
        return self.results_df

    def clear_results(self):
        """
        Clear all results from the portfolio.
        """
        self.results_df = pd.DataFrame(columns=self.COLUMNS)
