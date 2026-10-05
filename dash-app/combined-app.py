import pickle
import numpy as np
import dash
from dash import dcc, html, Input, Output, State, ALL
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc
from gmmtools import GMM_Custom
from tabs import contour, stress, llh, tangent

# ==========================================================
# App
# ==========================================================

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.CYBORG],
    suppress_callback_exceptions=True
)

# register callbacks (pass app into each module)
contour.register_callbacks(app)
stress.register_callbacks(app)
llh.register_callbacks(app)
tangent.register_callbacks(app)

# ==========================================================
# Load models ONCE
# ==========================================================

with open("../create-gmms/gmm_asc_fem.pkl", "rb") as f:
    fem_asc = pickle.load(f)

with open("../create-gmms/gmm_dsc_fem.pkl", "rb") as f:
    fem_dsc = pickle.load(f)

with open("../create-gmms/gmm_asc_mal.pkl", "rb") as f:
    mal_asc = pickle.load(f)

with open("../create-gmms/gmm_dsc_mal.pkl", "rb") as f:
    mal_dsc = pickle.load(f)

GMM_MAP = {
    ("Female", "Ascending"): fem_asc,
    ("Female", "Descending"): fem_dsc,
    ("Male", "Ascending"): mal_asc,
    ("Male", "Descending"): mal_dsc,
}

# ==========================================================
# ROOT LAYOUT
# ==========================================================

TAB_STYLE = {
    "backgroundColor": "#202330",
    "color": "white",
    "border": "none"
}

TAB_SELECTED_STYLE = {
    "backgroundColor": "#EDECEA",
    "color": "black",
    "border": "none"
}

app.layout = html.Div([
    dcc.Tabs(
        id="tabs",
        value="contour",
        colors={
            "background": "#111111",
            "border": "#111111",
            "primary": "#00adb5"   # active tab highlight
        },
        children=[
            dcc.Tab(label="Probability distributions", value="contour",
                    style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
            dcc.Tab(label="Stresses", value="stress",
                    style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
            dcc.Tab(label="Likelihood calculator", value="llh",
                    style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
            dcc.Tab(label="Tangent stiffness calculator", value="tangent",
                    style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
        ]
    ),
    html.Div(id="tab-content")
])


# ==========================================================
# TAB SWITCHING
# ==========================================================

@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "value")
)
def render_tab(tab):
    if tab == "contour":
        return contour.layout()
    elif tab == "stress":
        return stress.layout()
    elif tab == "llh":
        return llh.layout()
    elif tab == "tangent":
        return tangent.layout()

# ==========================================================
# RUN
# ==========================================================

if __name__ == "__main__":
    app.run(debug=True)
