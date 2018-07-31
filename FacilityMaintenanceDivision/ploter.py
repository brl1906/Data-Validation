"""
This module handles creation of the standard visualizations for the Facility
Maintenance Division Key Performance Indicators. Each method returns a
figure dictionary with data and layout for Plotly plot.  The purpose of This
module is to provide greater flexibility and reuse of charting objects or
visualizations produced with Facility Maintenance data and envisions the
functions being passed to Plotly methods visualization, analysis or dashboards
in other projects, notebooks or applications.
"""

import plotly.graph_objs as go

def pm2cm_barchart(years,values,dataframes):
    """
    """
    pm2cm_trace = go.Bar(
        x = years,
        y = [round(val, 1) for val in values],
        marker = dict(color = '#3c5a89'),
        name = 'pm:cm<br>kpi'
    )
    wo_volume_trace = go.Bar(
        x = years,
        y = [dataframes[yr]['wo_id'].count() for yr in years],
        marker = dict(color = 'grey',
                     line = dict(color = 'black',
                                width = 1.5)),
        opacity = .2,
        yaxis = 'y2',
        name = 'total<br>work orders'
    )

    layout = go.Layout(
        hovermode = 'closest',
        legend = dict(orientation = 'h'),
        title =' HVAC PM:CM KPI<br>FY{} -- FY{}'.format(min(years),max(years)),
        yaxis=dict(title='pct %',
                  showgrid = False,
                   titlefont = dict(color = '#3c5a89'),
                  tickfont = dict(color = '#3c5a89')),
        yaxis2=dict(title='total work order volume',
                    showgrid = False,
                    titlefont=dict(color='grey'),
            tickfont=dict(
                color='grey'
            ),
            overlaying='y',
            side='right'
        ),
        plot_bgcolor = '#efefea',
        paper_bgcolor = '#efefea'
    )
    fig = dict(data=[pm2cm_trace,wo_volume_trace],layout=layout)
    return fig
