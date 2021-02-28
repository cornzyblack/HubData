import os
import pandas as pd
import altair as alt
import datapane as dp
from datetime import date


api_token = os.getenv("token")
dp.login(token=api_token)

df = pd.read_csv("data/daily_prices.csv")

plot = (
    alt.Chart(df)
    .mark_line()
    .encode(x="Date", y="Price ($)")
    .interactive()
    .properties(width="container")
)

# Create report
r = dp.Report(
    f"### Line plot Showing Daily Oil Prices World in Data](http://www.eia.gov/naturalgas) on {date.today()}_",
    dp.Plot(plot),
    dp.DataTable(df),
)

# Publish
r.publish(
    name=f"Daily Oil Prices World in Data",
    open=True,
    description=f"Daily Oil Prices from Hub Data",
)
