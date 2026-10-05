import pickle
import numpy as np
import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc

from gmmtools import GMM_Custom
import sys
sys.path.append("../arterial-compliance/")
from StressTransform import *


# ==========================================================
# Utility: GMM plot controller
# ==========================================================

class GMMPlotController:
    """
    Maintains a set of GMMs reduced on conditioning variables
    and exposes contour data for plotting.
    """
    def __init__(self, gmms, cond_vars, stress_transform, init_values):
        self.gmm = gmms[0]
        self.cond_vars = cond_vars
        self.stress_transform = stress_transform

        self.gmm.verbose = False
        self.gmm.reduce(condition=cond_vars, x_cond=init_values)

    def update(self, values):
        self.gmm.update_reduced_gmm(values)

    def pca2vals(self,values):
        m, high, low = values
        s1_mean, s2_mean = self.stress_transform.i_transform(m)
        high1, high2 = self.stress_transform.i_transform(high)
        low1, low2 = self.stress_transform.i_transform(low)
        #print(s1_mean)
        return [[[s1_mean[0,:10],   high1[0,:10],   low1[0,:10]],
                 [s1_mean[0,10:20], high1[0,10:20], low1[0,10:20]],
                 [s1_mean[0,20:],   high1[0,20:],   low1[0,20:]]],
                [[s2_mean[0,:10],   high2[0,:10],   low2[0,:10]],
                 [s2_mean[0,10:20], high2[0,10:20], low2[0,10:20]],
                 [s2_mean[0,20:],   high2[0,20:],   low2[0,20:]]],
                ]

    def stress_data(self):
        return self.pca2vals(self.gmm.mean_std(reduced=True))


# ==========================================================
# Layout factories
# ==========================================================

def make_slider(cfg):
    return html.Div(
        [
            html.Label(cfg["label"]),
            dcc.Slider(
                id=cfg["id"],
                min=cfg["min"],
                max=cfg["max"],
                step=cfg["step"],
                value=cfg["default"],
                marks=cfg.get("marks", None),
                updatemode="drag",
            ),
        ],
        style={"marginBottom": "20px"},
    )


def make_control_panel(slider_cfgs):
    return html.Div(
        [make_slider(cfg) for cfg in slider_cfgs],
        style={
            "width": "20%",
            "padding": "20px",
            "backgroundColor": "#202330",
            "color": "white",
        },
    )


# ==========================================================
# Plot creation
# ==========================================================

def make_initial_figure(titles, stress_data):
    fig = make_subplots(
        rows=2,
        cols=3,
        subplot_titles=titles,
        shared_xaxes='all',
        shared_yaxes='columns',
        horizontal_spacing=0.05,
        vertical_spacing=0.05,
    )
    xpos = [0.28, 0.64, 0.99]
    ypos = [0.95, 0.425]
    t = np.linspace(0,1,10)
    rgba_map = {
        "red":   "rgba(255,0,0,0.4)",
        "green": "rgba(0,255,0,0.2)",
        "blue":  "rgba(0,0,255,0.4)"
    }
    colors = ['red','blue','green']

    for r, data in enumerate(stress_data):
        for c, (mean, high, low) in enumerate(data):
            fig.add_trace(
                go.Scatter(
                    x=t,
                    y=mean,
                    mode='lines',
                    line=dict(color=colors[c], width=2),
                    showlegend=False,
                ),
                row=r + 1,
                col=c + 1,
            )
            fig.add_trace(
                go.Scatter(
                    x = t,
                    y = high,
                    mode = "lines",
                    line = dict(width=0),
                    showlegend=False,
                ),
                row=r + 1,
                col=c + 1,
            )
            fig.add_trace(
                go.Scatter(
                    x=t,
                    y=low, #np.concatenate([high, low]),
                    mode = "lines",
                    fill= "tonexty",
                    line=dict(width=0),
                    fillcolor=rgba_map[colors[c]],
                    hoverinfo='skip',
                    showlegend=False,
                ),
                row=r + 1,
                col=c + 1,
            )
            i = r*3 + c
            if c == 0:
                fig.layout.annotations[i].update(x=xpos[c],y=ypos[r],xanchor='right')
            else:
                fig.layout.annotations[i].update(x=xpos[c],y=ypos[r],xanchor='right')

    fig.update_layout(
        plot_bgcolor="#202330",
        paper_bgcolor="#111111",
        font=dict(color="white"),
        height=600,
        width=900,
        margin=dict(l=20, r=20, t=40, b=20),
    )
    fig.update_yaxes(
            range=[-1.1,0],
            row=1,
            col=1
        )
    fig.update_yaxes(
            range=[0,100],
            row=1,
            col=2
        )
    fig.update_yaxes(
            range=[-25,45],
            row=1,
            col=3
        )
    fig.update_xaxes(
            range=[0,1],
            row=1,
            col=1
        )

    fig.update_xaxes(gridcolor='rgba(255,255,255,0.1)')
    fig.update_yaxes(gridcolor='rgba(255,255,255,0.1)')

    fig['layout'][f'xaxis{4}']['title'] = "Normalised position [-]"
    fig['layout'][f'xaxis{5}']['title'] = "Normalised position [-]"
    fig['layout'][f'xaxis{6}']['title'] = "Normalised position [-]"
    fig['layout'][f'yaxis{1}']['title'] = "Diastolic stress (normalised) [-]"
    fig['layout'][f'yaxis{4}']['title'] = "Systolic stress (normalised) [-]"

    fig.update_xaxes(autorange=False)
    fig.update_yaxes(autorange=False)

    return fig


# ==========================================================
# Main app builder
# ==========================================================


def layout():

    # --------------------------------------------------
    # Layout
    # --------------------------------------------------

    return html.Div(
        [
            html.Div(
                [
                    make_control_panel(spec["conditioning"]),
                    html.Div(
                        [
                            html.H4(spec["title"], style={"color": "white"}),
                            dcc.Graph(id="stress-gmm-plot", figure=fig),
                        ],
                        style={"width": "80%", "padding": "20px"},
                    ),
                ],
                style={"display": "flex", "backgroundColor": "#111111"},
            ),
        ]
    )

# --------------------------------------------------
# Callbacks
# --------------------------------------------------
def register_callbacks(app):
    @app.callback(
        Output("stress-gmm-plot", "figure"),
        [Input(cfg["id"], "value") for cfg in spec["conditioning"]],
        State("stress-gmm-plot", "figure"),
    )
    def update_stresses(*args):
        values = list(args[:-1])

        if "derived_conditioning" in spec:
            values = spec["derived_conditioning"](values)

        controller.update(values)
        updated_data = controller.stress_data()

        fig_dict = args[-1]
        i = 0
        for data in updated_data:
            for d in data:
                for y in d:
                    fig_dict["data"][i]["y"] = y.tolist()
                    i += 1

        return fig_dict

# ==========================================================
# App specification (ONLY thing you change per app)
# ==========================================================

with open("../arterial-compliance/gmm_stress.pkl", "rb") as f:
    gmm_stress = pickle.load(f)
    
with open("../arterial-compliance/stress_transform.pkl", "rb") as f:
    stress_transform = pickle.load(f)

spec = {
    "title": "Human aortic stresses",
    "gmms": [gmm_stress],
    "cond_vars": ["DBP", "SBP", "Area", "Dist"],
    "stress_transform": stress_transform,
    "conditioning": [
        {"id": "s-dbp", "label": "DBP (mmHg)", "min": 30, "max": 100, "step": 2, "default": 80, "marks":{i: str(i) for i in range(30,105,10)}},
        {"id": "s-sbp", "label": "SBP (mmHg)", "min": 100, "max": 150, "step": 2, "default": 120, "marks":{i: str(i) for i in range(100,155,10)}},
        {"id": "s-dia", "label": "Diameter (mm)", "min": 20, "max": 40, "step": 1, "default": 30, "marks":{i: str(i) for i in range(20,41,5)}},
        {"id": "s-dist", "label": ["Distensibility (10", html.Sup("-3"), " mmHg", html.Sup("-1"), ")"], "min": 1, "max": 4, "step": 0.2, "default": 2.5, "marks":{i: str(i) for i in range(1,5,1)}},
    ],
    "derived_conditioning": lambda v: [
        v[0],
        v[1], 
        np.pi*(v[2]/2.)**2,
        v[3],
    ],
    "plot": {
        "area2dia": lambda X: np.sqrt(X / np.pi) * 2,
        "dia2area": lambda X: np.pi*(X/2) ** 2,
    },
    "labels" : ["Radial", "Circumferential", "Longitudinal",
                "Radial", "Circumferential", "Longitudinal"]
}

# Initial conditioning values
init_vals = [cfg["default"] for cfg in spec["conditioning"]]

# Optional derived variable hook (e.g. BSA)
if "derived_conditioning" in spec:
    init_vals = spec["derived_conditioning"](init_vals)

controller = GMMPlotController(
    gmms = spec["gmms"],
    cond_vars=spec["cond_vars"],
    stress_transform=spec["stress_transform"],
    init_values=init_vals,
)

stress_data = controller.stress_data()

fig = make_initial_figure(
    titles = spec["labels"],
    stress_data=stress_data,
)
