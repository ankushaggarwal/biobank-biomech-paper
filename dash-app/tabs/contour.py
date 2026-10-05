import pickle
import numpy as np
import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc

from gmmtools import GMM_Custom

# ==========================================================
# Utility: GMM plot controller
# ==========================================================

class GMMPlotController:
    """
    Maintains a set of GMMs reduced on conditioning variables
    and exposes contour data for plotting.
    """
    def __init__(self, gmms, cond_vars, init_values):
        self.gmms = gmms
        self.cond_vars = cond_vars

        for gmm in self.gmms:
            gmm.verbose = False
            gmm.reduce(condition=cond_vars, x_cond=init_values)

    def update(self, values):
        for gmm in self.gmms:
            gmm.update_reduced_gmm(values)

    def contour_data(self):
        #return [gmm.contour_levels_from_percentiles() for gmm in self.gmms]
        return [gmm.get_gmm_contour_data() for gmm in self.gmms]


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

def make_initial_figure(titles, contour_data, x_transform):
    n = len(contour_data)
    rows = cols = int(np.ceil(np.sqrt(n)))

    fig = make_subplots(
        rows=rows,
        cols=cols,
        subplot_titles=titles,
        shared_xaxes='all',
        shared_yaxes='all',
        horizontal_spacing=0.05,
        vertical_spacing=0.05,
    )
    xpos = [0.47, 0.99]
    ypos = [0.95, 0.425]

    #for i, (X, Y, Z, levels) in enumerate(contour_data):
    for i, (X, Y, Z) in enumerate(contour_data):
        r, c = divmod(i, cols)
        zmin, zmax = np.min(Z), np.max(Z)
        fig.add_trace(
            go.Contour(
                x=x_transform(X[0, :]),
                y=Y[:, 0],
                z=Z,
                #colorscale='Viridis',
                contours_coloring="lines",
                showscale=False,
                line_width=2,
                contours=dict(
                    start=zmin,
                    end=zmax,
                    size=(zmax-zmin)/10
                    ),
            ),
            row=r + 1,
            col=c + 1,
        )
        fig.layout.annotations[i].update(x=xpos[c],y=ypos[r],xanchor='right')

    fig.update_layout(
        plot_bgcolor="#202330",
        paper_bgcolor="#111111",
        font=dict(color="white"),
        height=600,
        width=750,
        margin=dict(l=20, r=20, t=40, b=20),
    )

    fig.update_xaxes(gridcolor='rgba(255,255,255,0.1)')
    fig.update_yaxes(gridcolor='rgba(255,255,255,0.1)')
    fig.update_yaxes(
            range=[0.1,10.5],
            row=1,
            col=1
        )
    fig.update_xaxes(
            range=[17,42],
            row=1,
            col=1
        )

    fig['layout'][f'xaxis{3}']['title'] = "Diameter [mm]"
    fig['layout'][f'xaxis{4}']['title'] = "Diameter [mm]"
    fig['layout'][f'yaxis{1}']['title'] = 'Distensibility (10<sup>-3</sup> mm-Hg<sup>-1</sup>)'
    fig['layout'][f'yaxis{3}']['title'] = 'Distensibility (10<sup>-3</sup> mm-Hg<sup>-1</sup>)'
    fig.update_xaxes(autorange=False)
    fig.update_yaxes(autorange=False)
    return fig


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
                            dcc.Graph(id="contour-gmm-plot", figure=fig),
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
        Output("contour-gmm-plot", "figure"),
        [Input(cfg["id"], "value") for cfg in spec["conditioning"]],
        State("contour-gmm-plot", "figure"),
    )
    def update_contours(*args):
        values = list(args[:-1])

        if "derived_conditioning" in spec:
            values = spec["derived_conditioning"](values)

        controller.update(values)
        updated = controller.contour_data()

        fig_dict = args[-1]
        for i, (_, _, Z) in enumerate(updated):
            zmin, zmax = np.min(Z), np.max(Z)
            fig_dict["data"][i]["z"] = Z.tolist()
            fig_dict["data"][i]["contours"] = dict(
                    start=zmin,
                    end=zmax,
                    size=(zmax-zmin)/10,
                    coloring="lines"
                    )

        return fig_dict

# ==========================================================
# App specification 
# ==========================================================

with open("../create-gmms/gmm_asc_fem.pkl", "rb") as f:
    fem_asc = pickle.load(f)
with open("../create-gmms/gmm_dsc_fem.pkl", "rb") as f:
    fem_dsc = pickle.load(f)
with open("../create-gmms/gmm_asc_mal.pkl", "rb") as f:
    mal_asc = pickle.load(f)
with open("../create-gmms/gmm_dsc_mal.pkl", "rb") as f:
    mal_dsc = pickle.load(f)

spec = {
    "title": "Human aortic properties",
    "gmms": [
        {"gmm": fem_asc, "title": "Female Ascending Aorta"},
        {"gmm": fem_dsc, "title": "Female Descending Aorta"},
        {"gmm": mal_asc, "title": "Male Ascending Aorta"},
        {"gmm": mal_dsc, "title": "Male Descending Aorta"},
    ],
    "cond_vars": ["Age", "Bod_Sur", "DBP", "SBP"],
    "conditioning": [
        {"id": "c-age", "label": "Age (years)", "min": 45, "max": 85, "step": 1, "default": 65, "marks":{i: str(i) for i in range(45,86,10)}},
        {"id": "c-height", "label": "Height (cm)", "min": 120, "max": 200, "step": 2, "default": 170, "marks":{i: str(i) for i in range(120,205,20)}},
        {"id": "c-weight", "label": "Weight (kg)", "min": 40, "max": 160, "step": 2, "default": 70, "marks":{i: str(i) for i in range(40,165,40)}},
        {"id": "c-dbp", "label": "DBP (mmHg)", "min": 30, "max": 100, "step": 2, "default": 80, "marks":{i: str(i) for i in range(30,105,10)}},
        {"id": "c-sbp", "label": "SBP (mmHg)", "min": 100, "max": 150, "step": 2, "default": 120, "marks":{i: str(i) for i in range(100,155,10)}},
    ],
    "derived_conditioning": lambda v: [
        v[0],
        0.007184 * (v[2] ** 0.425) * (v[1] ** 0.725),  # BSA
        v[3],
        v[4],
    ],
    "plot": {
        "x_transform": lambda X: np.sqrt(X / np.pi) * 2,
    },
}
# Initial conditioning values
init_vals = [cfg["default"] for cfg in spec["conditioning"]]

# Optional derived variable hook (e.g. BSA)
if "derived_conditioning" in spec:
    init_vals = spec["derived_conditioning"](init_vals)

controller = GMMPlotController(
    gmms=[entry["gmm"] for entry in spec["gmms"]],
    cond_vars=spec["cond_vars"],
    init_values=init_vals,
)

contour_data = controller.contour_data()

fig = make_initial_figure(
    titles=[entry["title"] for entry in spec["gmms"]],
    contour_data=contour_data,
    x_transform=spec["plot"]["x_transform"],
)
