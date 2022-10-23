# -*- coding: utf-8 -*-
"""
Date: Sun October 23 2022
Author: Chinedu Onyeka
"""

# Import require libraries
import pandas as pd
import numpy as np
import plotly.express as px

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

print("Use the Socrata API to obtain the data : API token not actually required")
print()

url_address = "https://data.cityofnewyork.us/resource/uvpi-gqnh.json"
select = ["spc_common", "boroname", "steward", "health", "count(health)"]
group = ["spc_common", "boroname", "steward", "health"]
limit = 9999 # Socrato puts a 1000 limit on API calls

trees_url =url_address + "?$select="+",".join(select) + "&$group="+",".join(group) +\
            "&$limit=" + str(limit) 

trees_nyc = pd.read_json(trees_url)

#data pre-processing/cleaning
print("data pre-processing/cleaning")
trees_nyc.rename(columns={'count_health':'count'},inplace=True)
trees_nyc.dropna(inplace=True)
trees_nyc.replace("None","0(None)",inplace=True)

# Display the head of the data
print()
print(trees_nyc.head(10))

# check for all the column names
print()
print(trees_nyc.columns)

# check all the species
print()
print(trees_nyc["spc_common"].unique())

# determine all the borough names
print()
print(trees_nyc["boroname"].unique())

# find all possible health status of trees
print()
print(trees_nyc["health"].unique())

# what steward categories
print()
print(trees_nyc["steward"].unique())

# assign the spc_common, boroname, steward, and health to meaningful variable names
species = trees_nyc['spc_common'].unique()
species = np.insert(species,0,'All')
boroname = trees_nyc['boroname'].unique()
steward = trees_nyc['steward'].unique()
health = trees_nyc['health'].unique()

print()
print("Functions to answer question1 and question2")

# function for question1
def question1(df, boroname, specie):
    """
    A function that generates a plot for question1
    """
    try:
        if specie != "All":
            df = df[df["spc_common"] == specie]
        if boroname != "All":
            df = df[df["boroname"] == boroname]
        df = df.groupby(["health"],as_index=False).sum()
        total_count = sum(df["count"])
        df['percent'] = df["count"]/total_count

        # generate the plot using plotly
        figure = px.bar(df, x="health", y="percent", hover_data=["count", "percent"])    
        if (len(df) == 0):
            figure.update_layout(yaxis={"visible": False, 
                                     "showticklabels": False},
                              xaxis={"visible": False, 
                                     "showticklabels": False},
                              title={
                                "text": "No Data for " + boroname,
                                "y":0.5,
                                "x":0.5,
                                "xanchor": "center",
                                "yanchor": "top"}
                             )                         
        else: 
            figure.update_layout(
            width=400,
            height=300,
            title={
                'text': boroname,
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'})
        return figure
    
    except TypeError:
        print("You have entered the wrong type")
    
    
# function for question2
def question2(df, boroname, specie):
    """
    A function that generates the plot for question2
    """
    try:
        if specie != 'All':
            df = df[df['spc_common'] == specie] 
        if boroname != 'All':
            df = df[df['boroname'] == boroname]

        # generate the plot using plotly
        df = df.groupby(['health','steward'],as_index=False).sum()
        df = df.pivot(index='health', columns='steward', values='count')
        df.fillna(0, inplace=True)
        for steward in df.columns: 
            df[steward] = df[steward]/sum(df[steward])
        figure = px.imshow(df, color_continuous_scale="Teal", labels=dict(color="percentage"))        
        if (len(df) == 0):
            figure.update_layout(yaxis={"visible": False, 
                                     "showticklabels": False},
                              xaxis={"visible": False, 
                                     "showticklabels": False},
                              title={
                                "text": "No Data for " + boroname,
                                "y":0.5,
                                "x":0.5,
                                "xanchor": "center",
                                "yanchor": "top"}
                             )                         
        else: 
            figure.update_layout(
            width=400,
            height=300,
            title={
                "text": boroname,
                "y":0.9,
                "x":0.5,
                "xanchor": "center",
                "yanchor": "top"})
        return figure

    except TypeError:
        print("You have entered the wrong type")

print()
print("Build the Dash App")

SIDEBAR_STYLE = {
    "display": "inline-block",
    "width": "15vw",
    "background-color": "#f8f9fa",
    "vertical-align": "top"
}

CONTENT_STYLE_1 = {
    "display": "inline-block",
    "width": "27vw"
}

CONTENT_STYLE_2 = {
    "display": "inline-block",
    "width": "27vw"
}

CONTENT_STYLE_3 = {
    "display": "inline-block",
    "width": "27vw"
}

app = dash.Dash(__name__,suppress_callback_exceptions=True)
server=app.server

app.layout = html.Div([
    dcc.Tabs(id="data_608_module4", value='tab_1', children=[
        dcc.Tab(label='Q1:Proportion of trees in good, fair, or poor health condition', value='tab_1'),
        dcc.Tab(label='Q2:Stewards vs. health conditions', value='tab_2'),
    ]),
    html.Div(id='tabs_content')
])

@app.callback(Output('tabs_content', 'children'),
              Input('data_608_module4', 'value'))
def render_content(tab):
    if tab == 'tab_1':
        return html.Div([
            html.Div([
                html.H4("Species",style={'font-weight': 'bold',"text-align": "center"}),
                dcc.Dropdown(
                    id="question1",
                    options=[{"label": x, "value": x} for x in species],
                    value=species[0],
                    clearable=False,
                )
            ],style=SIDEBAR_STYLE),
            html.Div([
                dcc.Graph(id="q1_chart1"),
                dcc.Graph(id="q1_chart4"),
            ],style=CONTENT_STYLE_1),
            html.Div([
                dcc.Graph(id="q1_chart2"),
                dcc.Graph(id="q1_chart5"),
            ],style=CONTENT_STYLE_2),
            html.Div([
                dcc.Graph(id="q1_chart3"),
                dcc.Graph(id="q1_chart6"),
            ],style=CONTENT_STYLE_3),
        ])
    elif tab == 'tab_2':
        return html.Div([
            html.Div([
                html.H4("Species",style={'font-weight': 'bold',"text-align": "center"}),
                dcc.Dropdown(
                    id="question2",
                    options=[{"label": x, "value": x} for x in species],
                    value=species[0],
                    clearable=False,
                )
            ],style=SIDEBAR_STYLE),
            html.Div([
                dcc.Graph(id="q2_chart1"),
                dcc.Graph(id="q2_chart4"),
            ],style=CONTENT_STYLE_1),
            html.Div([
                dcc.Graph(id="q2_chart2"),
                dcc.Graph(id="q2_chart5"),
            ],style=CONTENT_STYLE_2),
            html.Div([
                dcc.Graph(id="q2_chart3"),
                dcc.Graph(id="q2_chart6"),
            ],style=CONTENT_STYLE_3),
        ])
    

@app.callback(
    Output("q1_chart1", "figure"), Output("q1_chart2", "figure"),
    Output("q1_chart3", "figure"), Output("q1_chart4", "figure"),
    Output("q1_chart5", "figure"), Output("q1_chart6", "figure"),
    [Input("q1_dropdown", "value")])
def q1_update_bar_chart(specie):      
    fig1 = question1(trees_nyc, 'All',specie) 
    fig2 = question1(trees_nyc, boroname[0],specie) 
    fig3 = question1(trees_nyc, boroname[1],specie) 
    fig4 = question1(trees_nyc, boroname[2],specie) 
    fig5 = question1(trees_nyc, boroname[3],specie) 
    fig6 = question1(trees_nyc, boroname[4],specie) 
    return fig1, fig2, fig3, fig4, fig5, fig6

@app.callback(
    Output("q2_chart1", "figure"), Output("q2_chart2", "figure"),
    Output("q2_chart3", "figure"), Output("q2_chart4", "figure"),
    Output("q2_chart5", "figure"), Output("q2_chart6", "figure"),
    [Input("q2_dropdown", "value")])
def q2_update_bar_chart(specie):
    fig1 = question2(trees_nyc, 'All',specie) 
    fig2 = question2(trees_nyc, boroname[0],specie) 
    fig3 = question2(trees_nyc, boroname[1],specie) 
    fig4 = question2(trees_nyc, boroname[2],specie) 
    fig5 = question2(trees_nyc, boroname[3],specie) 
    fig6 = question2(trees_nyc, boroname[4],specie) 
    return fig1, fig2, fig3, fig4, fig5, fig6

if __name__ == '__main__':
    app.run_server(debug=True)
