from dash import html, dcc, Input, Output, State, ALL
import plotly.graph_objects as go
import numpy as np

# ----------------------------------------------------------

def layout():
    return html.Div(
        [
            html.Div(
            [
                html.H4("Inputs", style={"color": "white"}),
                html.Label("Aortic diameter (mm)", style={"color": "white"}),
                dcc.Input(id="tangent-dia", type="number", value=30.0, style={"width": "100%"}),
                html.Br(),
                html.Br(),
                html.Label(
                    ["Distensibility (10", html.Sup("-3"), " mmHg", html.Sup("-1"), ")"],
                    style={"color": "white"},
                ),
                dcc.Input(
                    id="tangent-distensibility",
                    type="number",
                    value=3.0,
                    style={"width": "100%"},
                ),
                html.Br(),
                html.Br(),
                html.Button("Generate Plot", id="tangent-generate-button"),
            ],
            style={
                "width": "20%",
                "maxWidth": "400px",
                "padding": "20px",
                "backgroundColor": "#202330",
            },
            ),
            html.Div(
                    [dcc.Graph(id="tangent-plot"),
                dcc.Markdown(
                r"""

                The relationship between distensibility and wall stiffness is approximated by:

                $$
                \delta \approx \frac{(1+\bar{H})^2}{2 \mu \bar{H} (2+\bar{H})}
                $$

                where:

                - $\delta$ is the distensibility
                - $\mu$ is the shear modulus (tangent stiffness at diastole)
                - $\bar{H}$ is the normalised wall thickness (thickness/radius)

                This approximation is based on axisymmetric incompressible wall with neo-Hookean material with the reference state at diastole. 

                Reference:
                [Aggarwal et al. (2024), doi:10.1007/978-3-031-81743-4_14](https://doi.org/10.1007/978-3-031-81743-4_14)
                """, style={
                    "color": "white",
                    "backgroundColor": "#202330",
                    "padding": "10px",
                    "borderRadius": "5px",
                    "border": "1px solid #333",
                    "marginBottom": "15px",
                    }, mathjax=True)
                    ],
                    style={"width": "80%", "padding": "20px"},
                ),
            ],
            style={"display": "flex", "backgroundColor": "#111111"},
    )

# ----------------------------------------------------------

def register_callbacks(app):
    @app.callback(
        Output("tangent-plot", "figure"),
        Input("tangent-generate-button", "n_clicks"),
        State("tangent-dia", "value"),
        State("tangent-distensibility", "value"),
    )
    def update_secondary_plot(_, dia, dist):
        MPa_mmHg = 7500.61682823
        rad = dia / 2
        h = np.linspace(0.2, 3, 30)
        hbar = h / rad
        mu = (1 + hbar) ** 2 / (2 * hbar * (2 + hbar)) / dist * 1000
        mu = mu / MPa_mmHg

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=h, y=mu, mode="lines"))
        fig.update_layout(
            plot_bgcolor="#202330",
            paper_bgcolor="#111111",
            font=dict(color="white"),
            height=500,
            width=600,
            xaxis_title="Thickness (mm)",
            yaxis_title="Tangent stiffness (MPa)",
        )
        fig.update_xaxes(gridcolor='rgba(255,255,255,0.1)')
        fig.update_yaxes(gridcolor='rgba(255,255,255,0.1)')
        return fig
