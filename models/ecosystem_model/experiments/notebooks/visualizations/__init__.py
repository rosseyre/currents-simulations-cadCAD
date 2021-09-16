

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from ipywidgets import widgets
from plotly.subplots import make_subplots

from experiments.notebooks.visualizations.plotly_theme import (
    cadlabs_colors,
    cadlabs_colorway_sequence,
)
from model.system_parameters import parameters


# Set plotly as the default plotting backend for pandas
pd.options.plotting.backend = "plotly"





# 3D Surface

def plot_surface(df):
        grouped = df.groupby(["avg_price", "clients"]).last()["hosts"]

        x = df.groupby(["run"]).first()["avg_price"].unique()
        y = df.groupby(["run"]).first()["clients"].unique()
        z = []

        for avg_price in y:
            row = []
            for clients in x:
                z_value = grouped[avg_price][clients]
                row.append(z_value)
            z.append(row)

        fig = go.Figure(
            data=[
                go.Surface(
                    x=x,
                    y=y,
                    z=z,
                    colorbar=dict(
                        title="3D Plot",
                        titleside="right",
                        titlefont=dict(size=14),
                    ),
                    colorscale=cadlabs_colors,
                )
            ]
        )

        fig.update_traces(contours_z=dict(show=True, usecolormap=True, project_z=True))

        #update_legend_names(fig)

        fig.update_layout(
            title="3D Plot",
            autosize=False,
            legend_title="",
            margin=dict(l=65, r=50, b=65, t=90),
            scene={
                "xaxis": {
                    "title": {"text": "AVG Price (ZAR/Mbps/Day)"},
                    "type": "log",
                },
                "yaxis": {"title": {"text": "Clients"}},
                "zaxis": {"title": {"text": "Hosts"}},
            },
        )

        return fig



"""
    def plot_validator_environment_yield_surface(df):
        grouped = df.groupby(["eth_price", "eth_staked"]).last()["total_profit_yields_pct"]

        x = df.groupby(["run"]).first()["eth_price"].unique()
        y = df.groupby(["run"]).first()["eth_staked"].unique()
        z = []

        for eth_staked in y:
            row = []
            for eth_price in x:
                z_value = grouped[eth_price][eth_staked]
                row.append(z_value)
            z.append(row)

        fig = go.Figure(
            data=[
                go.Surface(
                    x=x,
                    y=y,
                    z=z,
                    colorbar=dict(
                        title="Profit Yields (%/year)",
                        titleside="right",
                        titlefont=dict(size=14),
                    ),
                    colorscale=cadlabs_colors,
                )
            ]
        )

        fig.update_traces(contours_z=dict(show=True, usecolormap=True, project_z=True))

        update_legend_names(fig)

        fig.update_layout(
            title="Profit Yields Over ETH Price vs. ETH Staked",
            autosize=False,
            legend_title="",
            margin=dict(l=65, r=50, b=65, t=90),
            scene={
                "xaxis": {
                    "title": {"text": "ETH Price (USD/ETH)"},
                    "type": "log",
                },
                "yaxis": {"title": {"text": "ETH Staked (ETH)"}},
                "zaxis": {"title": {"text": "Profit Yields (%/year)"}},
            },
        )

        return fig
"""