import os
import pandas as pd
import datapane as dp
from datetime import date
import plotly.express as px


df = pd.read_csv("data/daily_prices.csv")
datefrom = "1997-01-01"
fig2 = px.line(df, x="Date", y="Price")

fig2.update_layout(
    height=600, title_text="Daily Oil Prices",
)

fig2.write_html("plot.html")
