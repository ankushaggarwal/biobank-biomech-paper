import pickle
import numpy as np
import dash
from dash import dcc, html, Input, Output, State, ALL
import dash_bootstrap_components as dbc

# ==========================================================
# Load GMMs
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
# Utilities
# ==========================================================

def compute_bsa(height_cm, weight_kg):
    return 0.007184 * (weight_kg**0.425) * (height_cm**0.725)

def get_area_name(region):
    return "Asc_D_Area" if region == "Ascending" else "Dsc_D_Area"

def get_dist_name(region):
    return "Asc_Dist" if region == "Ascending" else "Dsc_Dist"

def input_block(label, component):
    return html.Div([
        html.Label(label),
        component
    ], style={"marginBottom": "10px"})

def make_roles():

    vars_all = [
        "Age", "BSA", "DBP", "SBP",
        "Size", "Distensibility"
    ]

    children = []

    for v in vars_all:
        children.append(html.Div([
            html.Label(v),
            dcc.RadioItems(
                [
                    {"label": "Condition", "value": "cond"},
                    {"label": "Marginalise", "value": "marg"},
                    {"label": "Likelihood (target)", "value": "none"},
                ],
                value="none",
                id="role-"+v,
            ),
        ]))

    return children

def layout():
    return html.Div([

        html.H3("Patient likelihood explorer"),

        # -------------------------
        # Patient inputs
        # -------------------------
        html.Div([
            html.Label("Sex"),
            #dcc.Dropdown(["Male", "Female"], "Female", id="sex"),
            dcc.RadioItems(
                ["Male", "Female"],
                "Female",
                id="sex"
            ),

            html.Label("Region"),
            #dcc.Dropdown(["Ascending", "Descending"], "Ascending", id="region"),
            dcc.RadioItems(
                ["Ascending", "Descending"],
                "Ascending",
                id="region"
            ),
            input_block(
            dcc.Input(id="age", type="number", value=50),
            html.Label("Age [years]")),

            input_block(
            dcc.Input(id="height", type="number", value=170),
            html.Label("Height [cm]")),

            input_block(
            dcc.Input(id="weight", type="number", value=70),
            html.Label("Weight [kg]")),

            input_block(
            dcc.Input(id="dbp", type="number", value=80),
            html.Label("DBP [mm-Hg]")),

            input_block(
            dcc.Input(id="sbp", type="number", value=120),
            html.Label("SBP [mm-Hg]")),

            # -------------------------
            # Geometry inputs
            # -------------------------
            html.Div([html.Label("Aortic size"),
            dcc.RadioItems(
                ["Diameter (mm)", "Area (mm²)"],
                "Diameter (mm)",
                id="geom-type"
            ),

            dcc.Input(id="size", type="number", value=30)], style={"marginBottom": "10px"}),

            input_block(html.Label([
                "Distensibility (10", html.Sup("-3"),
                " mmHg", html.Sup("-1"), ")"
            ]),
            dcc.Input(id="dist", type="number", value=3)),
        ], style={"width": "25%", "display": "inline-block", "padding": "20px", "verticalAlign": "top"}),

        # -------------------------
        # Variable roles
        # -------------------------
        html.Div([
            html.H4("Variable roles"),
            html.Div(
                make_roles(),
                id="var-selectors")
        ], style={"width": "25%", "display": "inline-block", "padding": "20px", "verticalAlign": "top"}),

        # -------------------------
        # Output
        # -------------------------
        html.Div([
            html.H4("Results"),
            html.Div(id="logllh"),
            html.Div(id="zscore"),
        ], style={"width": "25%", "display": "inline-block", "padding": "20px", "verticalAlign": "top"})
    ])


# ==========================================================
# Main computation
# ==========================================================

def register_callbacks(app):
    @app.callback(
        Output("logllh", "children"),
        Output("zscore", "children"),

        Input("age", "value"),
        Input("height", "value"),
        Input("weight", "value"),
        Input("dbp", "value"),
        Input("sbp", "value"),
        Input("size", "value"),
        #Input("area", "value"),
        Input("dist", "value"),
        Input("geom-type", "value"),
        Input("sex", "value"),
        Input("region", "value"),

        # roles
        Input("role-Age", "value"),
        Input("role-BSA", "value"),
        Input("role-DBP", "value"),
        Input("role-SBP", "value"),
        Input("role-Size", "value"),
        Input("role-Distensibility", "value"),
        #Input("role-Dsc_D_Area", "value"),
        #Input("role-Dsc_Dist", "value"),
    )
    def compute(age, height, weight, dbp, sbp,
                size, dist, geom_type,
                sex, region,
                role_Age, role_Bod_Sur, role_DBP, role_SBP,
                role_size, role_dist,
                ):

        try:
            gmm = GMM_MAP[(sex, region)]

            # ---------------------
            # Derived variables
            # ---------------------
            bsa = compute_bsa(height, weight)

            if geom_type == "Diameter":
                A = size
            else:
                A = np.pi * (size / 2.0)**2

            area_name = get_area_name(region)
            dist_name = get_dist_name(region)

            x_dict = {
                "Age": age,
                "Bod_Sur": bsa,
                "DBP": dbp,
                "SBP": sbp,
                area_name: A,
                dist_name: dist
            }

            role_map = {
                "Age": role_Age,
                "Bod_Sur": role_Bod_Sur,
                "DBP": role_DBP,
                "SBP": role_SBP,
                "Asc_D_Area": role_size,
                "Asc_Dist": role_dist,
                "Dsc_D_Area": role_size,
                "Dsc_Dist": role_dist,
            }

            cond_vars = []
            cond_vals = []
            marg_vars = []
            target_vars = []
            target_vals = []

            for v in x_dict.keys():
                role = role_map[v]

                if role == "cond":
                    cond_vars.append(v)
                    cond_vals.append(x_dict[v])
                elif role == "marg":
                    marg_vars.append(v)
                elif role == "none":
                    target_vars.append(v)
                    target_vals.append(x_dict[v])

            #must have targets
            if len(target_vars) == 0:
                return ("Error", "Select at least one 'Likelihood (target)' variable")
            gmm.verbose=False
            gmm.reduce(condition=cond_vars, x_cond=cond_vals, marginalise=marg_vars)

            logllh = gmm.prob_reduced(x=target_vals, log=True)
            try:
                z = gmm.z_score_reduced(x=target_vals)
            except:
                z = [np.nan]

            return (
                f"Log-likelihood: {float(logllh[0]):.3f}",
                f"Z-score: {float(z[0]):.2f}"
            )

        except Exception as e:
            return ("Error", str(e))

