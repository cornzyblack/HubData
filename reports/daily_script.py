import os
import pandas as pd
import altair as alt
import datapane as dp
from datetime import date


api_token = os.getenv("TOKEN", cli_login=False)
dp.login(token=api_token)

df = pd.read_csv("../data/daily_prices.csv")

plot = (
    alt.Chart(df)
    .mark_line()
    .encode(x="Date", y="Price")
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

# dataset = pd.read_csv("https://covid.ourworldindata.org/data/owid-covid-data.csv")
# df = (
#     dataset.groupby(["continent", "date"])["new_cases_smoothed_per_million"]
#     .mean()
#     .reset_index()
# )

# plot = (
#     alt.Chart(df)
#     .mark_area(opacity=0.4, stroke="black")
#     .encode(
#         x="date:T",
#         y=alt.Y("new_cases_smoothed_per_million:Q", stack=None),
#         color=alt.Color("continent:N", scale=alt.Scale(scheme="set1")),
#         tooltip="continent:N",
#     )
#     .interactive()
#     .properties(width="container")
# )

# report = dp.Report(dp.Plot(plot), dp.DataTable(df))
# # report.save(path='report.html', open=True)
# report.publish(name="Covid Report", open=True)
