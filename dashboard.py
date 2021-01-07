# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 10:47:09 2021

@author: Administrator
"""

import pandas as pd     #(version 1.0.0)
import plotly           #(version 4.5.4) pip install plotly==4.5.4
import plotly.express as px

import dash             #(version 1.9.1) pip install dash==1.9.1
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)
server = app.server
#---------------------------------------------------------------
#Taken from https://www.ecdc.europa.eu/en/geographical-distribution-2019-ncov-cases
dff = pd.read_csv("D:/Python Anywhere/NSE_Normalize.csv")
df=dff.copy()
#---------------------------------------------------------------
app.layout = html.Div([
    html.Div([
        dash_table.DataTable(
            id='datatable_id',
            data=dff.to_dict('records'),
            columns=[
                {"name": i, "id": i, "deletable": False, "selectable": False} for i in dff.columns
            ],
            editable=False,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            row_selectable="multi",
            row_deletable=False,
            selected_rows=[],
            page_action="native",
            page_current= 0,
            page_size= 6,
            # page_action='none',
            # style_cell={
            # 'whiteSpace': 'normal'
            # },
            # fixed_rows={ 'headers': True, 'data': 0 },
            # virtualization=False,
            style_cell_conditional=[
                {'if': {'column_id': 'symbols'},
                 'width': '40%', 'textAlign': 'left'},
                {'if': {'column_id': 'close'},
                 'width': '30%', 'textAlign': 'left'},
                {'if': {'column_id': 'normalize'},
                 'width': '30%', 'textAlign': 'left'},
            ],
        ),
    ],className='row'),

    html.Div([
        html.Div([
            dcc.Dropdown(id='linedropdown',
                options=[
                         {'label': 'normalize', 'value': 'Normalize_NSE'},
                         {'label': 'close', 'value': 'Close_NSE'}
                ],
                value='Close_NSE',
                multi=False,
                clearable=False
            ),
        ],className='six columns'),

        html.Div([
        dcc.Dropdown(id='piedropdown',
            options=[
                     {'label': 'close', 'value': 'Close_NSE'},
                     {'label': 'normalize', 'value': 'Normalize_NSE'}
            ],
            value='Normalize_NSE',
            multi=False,
            clearable=False
        ),
        ],className='six columns'),

    ],className='row'),

    html.Div([
        html.Div([
            dcc.Graph(id='linechart'),
        ],className='six columns'),

        html.Div([
            dcc.Graph(id='piechart'),
        ],className='six columns'),

    ],className='row'),


])

#------------------------------------------------------------------
@app.callback(
    [Output('piechart', 'figure'),
     Output('linechart', 'figure')],
    [Input('datatable_id', 'selected_rows'),
     Input('piedropdown', 'value'),
     Input('linedropdown', 'value')]
)
def update_data(chosen_rows,piedropval,linedropval):
    if len(chosen_rows)==0:
        df_filterd = dff[dff['Symbol'].isin(['Nifty50','APLAPOLLO','AUBANK','INFY'])]
    else:
        print(chosen_rows)
        df_filterd = dff[dff.index.isin(chosen_rows)]

   
       
    line_chart1=px.line(
            data_frame=df_filterd,
            x='Date',
            y=piedropval,
            color='Symbol',
            labels={'Symbol':'symbol'},
           
            )


    #extract list of chosen symbols
    list_chosen_symbols=df_filterd['Symbol'].tolist()
    #filter original df according to chosen symbols
    #because original df has all the complete dates
    df_line = df[df['Symbol'].isin(list_chosen_symbols)]

    line_chart = px.line(
            data_frame=df_line,
            x='Date',
            y=linedropval,
            color='Symbol',
            labels={'Symbol':'symbol'},
            )
    line_chart.update_layout(uirevision='foo')

    return (line_chart,line_chart1)
# #------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=False)
