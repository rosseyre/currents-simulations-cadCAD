

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
    grouped = df.groupby(["hosts", "clients", "network_allocation"])

    x = df.groupby(["run"]).first()["hosts"].unique()
    y = df.groupby(["run"]).first()["clients"].unique()
    z = df.groupby(["run"]).first()["network_allocation"].unique()

    fig = go.Figure(
        data=[
            go.Surface(
                x=x,
                y=y,
                z=z,
                colorbar=dict(
                    title="Allocation",
                    titleside="right",
                    titlefont=dict(size=14),
                ),
                colorscale=cadlabs_colors,
            )
        ]
    )

    fig.update_traces(contours_z=dict(show=True, usecolormap=True, project_z=True))


    fig.update_layout(
        title="Phase-space (Hosts vs Clients)",
        autosize=False,
        legend_title="",
        margin=dict(l=65, r=50, b=65, t=90),
        scene={
            "xaxis": {"title": {"text": "Hosts"},},
            "yaxis": {"title": {"text": "Clients"}},
            "zaxis": {"title": {"text": "Mbps"}},
        },
    )

    return fig