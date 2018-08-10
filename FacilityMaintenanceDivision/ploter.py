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

#### PM to CM ####
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

##### Customer Satisfaction ######
def satisfcation_piechart(df,column,title):
    """
    Function takes 3 required arguments--a dataframe, column with
    data for charting, chart title and takes an optional list of
    colors. The default colors argument is set to a list with 5 colors
    as there are 4 to 5 labels in the relevant satisfaction columns in
    the survey monkey data: satisfied, very satisfied, dis-satisfied,
    very dis-satisfied and nuetral.

    It creates a donut chart to be produced for the relevant service
    satisfaction questions asked in the DGS FMD survey.
    Example useage:

            satisfaction_piechart(df=df,column='service_quality',
                                title='satisfaction in service')

    Note: the 5th color is dropped in columns with only 4 or fewer unique
    satisfaction response types. The default Plotly colors kick in instances
    where the number of unique satisfaction types in a colum exceeds 5.
    """
    colors=dict(zip(sorted(df['wait_satisfaction'].value_counts().index),
                    ['#DB8B87','#F4EEEF','#B0C1A8','#C70039','#749A64']))
    trace = go.Pie(
        labels = df[column].value_counts().index,
        values = df[column].value_counts().values,
        hole = .3,
        marker = dict(colors = [colors[status] for status in df[column].value_counts().index])
    )
    layout = go.Layout(
        title = title,
        legend = dict(orientation = 'h'),
        plot_bgcolor = '#efefea',
        paper_bgcolor = '#efefea'
    )
    fig = dict(data=[trace],layout=layout)
    return fig


def create_satisfaction_figures(df):
    """
    Function takes 1 argument, a dataframe of survey monkey data returned
    from the fletecher module method for getting and handling
    this data.

    It creates a list of the Plotly figure objects of data and trace
    elements for the pie charts for satisfaction response distribution
    for each of the 5 service element satisfaction survey questions.

    Example useage:
            create_satisfaction_figures(df=df)

    Note: The object returned from the function is a list of figures. Each
    figure can be passed to a plotly.plotly method for visualizing a
    chart in a notebook, saving as a png or using in a dashboard
    """
    fig_list = []
    cols = ['past90_acknowledge_satisfaction','wait_satisfaction',
            'communication_satisfaction','duration_satisfaction',
            'past90_quality_satisfaction']
    titles = ['Satisfaction: Timeframe for<br>Acknowledging Work Order',
         'Satisfaction: Wait Time for<br>Work to Start',
         'Satisfaction: Communication w/ Agency<br> While Work Underway',
         'Satisfaction: Duration of Work Order',
         'Satisfaction : Qualtiy of the Work Performed']
    charts = dict(zip(cols,titles))
    for col in cols:
        fig_list.append(satisfcation_piechart(df=df,column=col,title=charts[col]))
    return fig_list
