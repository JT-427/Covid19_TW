from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import datetime as dt

from model.get_data import get_data
data = get_data(dt.date(2022, 1, 1))

fig = px.line(data, x=data.index, y='法定傳染病通報')

# fig.show()
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.SANDSTONE]
    )
server = app.server
app.layout = dbc.Container([
    dbc.Row(id='info', className='my-3', style={'text-align': 'center'}), 
    dbc.Card([
        html.Div([
            dcc.DatePickerRange(
                id='my-date-picker-range',
                min_date_allowed=dt.date(2020, 1, 15),
                max_date_allowed=dt.date.today(),
                initial_visible_month=dt.date.today(),
                start_date = dt.date.today() - dt.timedelta(weeks=4),
                end_date=dt.date.today()
            ),
            html.Div(id='fig')
        ],
        className='m-3')
    ])
])


@app.callback(
    Output('info', 'children'),
    Output('fig', 'children'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'))
def update_output(start_date, end_date):
    start_date = dt.datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = dt.datetime.strptime(end_date, '%Y-%m-%d').date()

    data = get_data(start_date, end_date)
    last_ = data.index[-1].date()
    fig = px.line(data, x=data.index, y='法定傳染病通報')

    data = data.to_numpy()[:, 0]
    end_date_num = int(data[-1])
    growth_rate = round((data[-1]-data[-2])/data[-2]*100, 2)
    week_average = round(data[-7:].mean(), 2)
    
    end_date_num_color = 'red' if end_date_num > week_average else 'blue'
    growth_rate_color = 'red' if growth_rate > 0 else 'green' if growth_rate < 0 else 'black'
    return [
        [dbc.Col([
            dbc.Card([
                html.H1([end_date_num], style={'font-size':'5rem', 'color': end_date_num_color}),
                html.P([str(last_) + ' 通報人數'])
            ], className='my-2')
        ]),
        dbc.Col([
            dbc.Card([
                html.H1([str(growth_rate)+'%'], style={'font-size':'5rem', 'color': growth_rate_color}),
                html.P(['單日成長率'])
            ], className='my-2')
        ]),
        dbc.Col([
            dbc.Card([
                html.H1([week_average], style={'font-size':'5rem'}),
                html.P(['近７日平均'])
            ], className='my-2')
        ])],
        dcc.Graph(
            id='example-graph',
            figure=fig
        ),
    ]

app.run_server(debug=False, port="21343")