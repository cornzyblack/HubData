import re
import requests
import numpy as np
import pandas as pd
from datetime import date
from dateparser import parse
from datetime import datetime
from bs4 import BeautifulSoup
from typing import List, Dict, Optional, Tuple
from dateutil.relativedelta import relativedelta


class HubData:
    """
    The HubData object contains a Scraper that scrapes the hub-data page

    Args:
        period (str): The period (Day, Week, Year)
        url (str): The Url for the selected Period (Day, Week, Year)
        df (pd.DataFrame): The DataFrame for the selected Period


    Attributes:
        url (str): This is the URL page for the specific period
    """

    def __init__(self, period: str = "day"):
        self.period = period
        self.url = self.get_url()
        pg_content = self.get_html()
        df_tables = self.get_tables(pg_content)

        self.df = self.normalize_tables(df_tables)
        self.save_to_csv()

    def get_url(self):
        """Get the URL for a period

        Returns:
            cars: A car mileage
        """
        period_dict = {
            "day": "rngwhhdD",
            "year": "rngwhhdA",
            "month": "rngwhhdM",
            "week": "rngwhhdW",
        }

        select_period = period_dict.get(self.period, None)
        url = f"http://www.eia.gov/dnav/ng/hist/{select_period}.htm"
        return url

    def get_year(self, date: str) -> Optional[str]:
        """Get the Year from string

        Args:
            date (str): The string that contains the year

        Returns:
            cars: A car mileage
        """
        year = None
        year_match = re.search("^\d{4}", date)
        if year_match:
            year = year_match.group(0)
        return year

    def clean_date(self, date: str) -> str:
        """Clean the the Date String
        Returns:
            cars: A car mileage
        """
        return "".join(date.split())

    def get_html(self) -> bytes:
        """Get the raw HTML page

        Returns:
            bytes: the raw html page in bytes
        """
        page_content = None
        soup = None
        try:
            req = requests.get(self.url)
            if req.status_code == 200:
                page_content = req.content

        except requests.exceptions.RequestException as e:
            print("Error parsing", e)
        return page_content

    def get_tables(self, page_content: bytes) -> Optional[pd.DataFrame]:
        """Transform the Page Content into a DataFrame

        Args:
            page_content (bytes): The page content that contains tables

        Returns:
            Optional[pd.DataFrame]: The Page content in the form of a DataFrame
        """
        df = None
        try:
            if page_content:
                soup = BeautifulSoup(page_content, features="lxml")
                table_data = soup.select(
                    'table[Summary="Henry Hub Natural Gas Spot Price (Dollars per Million Btu)"]'
                )[0]
                df = pd.read_html(str(table_data))[0].dropna(how="all").reset_index()
        except Exception as e:
            print(e)
        return df

    def get_date_range(self, date_range_str: str) -> Tuple[datetime, datetime]:
        """Generate the Date Range from a Date String

        Args:
            date_range_str (str): A Date Range in String format

        Returns:
            Tuple[datetime, datetime]: The Start Date and End date of a date string range
        """
        date_range_str = self.clean_date(date_range_str)
        end_date = None
        start_date = None

        year = get_year(date_range_str)
        # Search for Date Match
        start_date_match = re.search("^\d{4}[JFADMONDS]\w{2}\-\d{1,2}", date_range_str)
        end_date_match = re.search("[JFADMONDS]\w{2}\-\d{1,2}$", date_range_str)

        if start_date_match and end_date_match:
            start_date_str = start_date_match.group(0)
            end_date_str = year + end_date_match.group(0)

            start_date = parse(start_date_str).date()
            end_date = parse(end_date_str).date()

            if end_date < start_date:
                end_date += relativedelta(years=+1)

        return start_date, end_date

    def normalize_monthly_tables(self, df: pd.DataFrame) -> pd.DataFrame:
        """normalize the monthly table

        Args:
            df (pd.DataFrame): The DataFrame of the momthly table from the HTML page

        Returns:
            pd.DataFrame: A Transformed monthly Dataframe
        """
        df = df.melt(["Year"], var_name="month", value_name="Price")
        df = df.rename(columns={"Year": "Date"})
        df["Date"] = pd.to_datetime(
            "01/" + df["month"] + "/" + df.Date.astype(int).astype(str)
        )
        return df

    def normalize_yearly_tables(self, df: pd.DataFrame) -> pd.DataFrame:
        """normalize the yearly table

        Args:
            df (pd.DataFrame): The DataFrame of the yearly table from the HTML page

        Returns:
            pd.DataFrame: A Transformed yearly Dataframe
        """
        df = df.melt(["Decade"], var_name="Year", value_name="Price")
        df["Decade"] = df["Decade"].str.replace("'s", "", regex=True).astype(int)
        df["Year"] = df["Year"].str.replace("Year\-", "", regex=True).astype(int)
        df["Date"] = df["Decade"] + df["Year"]
        df = df.sort_values(by="Date")[["Date", "Price"]]
        return df

    def normalize_daily_tables(self, df: pd.DataFrame) -> pd.DataFrame:
        """normalize the daily table

        Args:
            df (pd.DataFrame): The DataFrame of the daily table from the HTML page

        Returns:
            pd.DataFrame: A Transformed daily Dataframe
        """
        dates = []
        daily_arr = np.array(df[["Mon", "Tue", "Wed", "Thu", "Fri"]]).flatten()
        date_range_list = list(
            pd.bdate_range(*self.get_date_range(week)) for week in df["Week Of"]
        )
        for date_range in date_range_list:
            dates.extend(date_range)

        df = pd.DataFrame({"Date": dates, "Price": daily_arr})
        return df

    def normalize_tables(self, df: pd.DataFrame) -> pd.DataFrame:
        """Normalize any Table from any period

        Args:
            df (pd.DataFrame): The normalized Table

        Returns:
            pd.DataFrame: A DataFrame that contains the normalized Table
        """
        try:
            df = df.replace({"--": np.nan, "W": np.nan})

            if self.period == "year":
                df = self.normalize_yearly_tables(df)
            if self.period == "week":
                pass
            if self.period == "month":
                df = self.normalize_monthly_tables(df)
            if self.period == "day":
                df = self.normalize_daily_tables(df)

            df = df[["Date", "Price"]].sort_values(by="Date")
            df = df.reset_index(drop=True)
        except Exception as e:
            print(e)
        return df

    def save_to_csv(self, filename: str = None):
        """Save the Table to a CSV format

        Args:
            df (pd.DataFrame): The normalized DataFrame
            filename (str): The name of the file
        """
        if not filename:
            str_name = datetime.now().strftime("%Y%m%d")
            filename = self.period + "_" + str_name + ".csv"
        if not self.df.empty:
            self.df.to_csv(filename, index=False)
            print(f"File has been saved as {filename}")
