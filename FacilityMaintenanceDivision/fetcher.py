"""
This module provides helper methods for getting and returning
the dataframes and related objects to support the Facilty Maintenance
Division Key Performance Indicator reporting and exploratory analysis.
"""

import numpy as np
import pandas as pd


def create_pm2cm_dataframe(filepath):
    """
    Function takes filepath for the excel spreadsheet with archibus data
    located on the Zdrive. It returns a dataframe with a datetime index
    of work order date_requested and filters out all 'Test' work orders.

    The function also filters down to the most useful columns for analysis
    related to this indicator and establishes useful columns for exploratory
    data analysis such as a fiscal year column based on the City of Baltimore
    fiscal year and a column indicating the number of each type of work order
    for each fiscal year.

    Example usage:
        create_pm2cm_dataframe('Data/archibus_maintenance_data.xlsx')
    """
    df = pd.read_excel(io=filepath,index_col='date_requested',
                       usecols=['bl_id','date_requested','completed_by',
                       'date_assigned','date_closed','date_completed','prob_type',
                       'time_completed','wo_id','time_start','time_end'])
    df = df[df.prob_type != 'TEST(DO NOT USE)']
    df['duration'] = df['date_completed'] - df.index
    df['fiscal_year'] = np.where(df.index.month >= 7,df.index.year+1, df.index.year)
    # add column for volume by problem type per fiscal year
    df['problem_type_count_fiscal_year'] = df.groupby(['fiscal_year','prob_type'])['prob_type'].transform('count')
    return df

def create_pm2cm_kpi_values_dicts(df):
    """
    Function takes dataframe object returned from the create_pm2cm_dataframe
    function in the fetcher module which returns a cleaned and formatted
    dataframe for analysis related to pm to cm kpi and other exploratory
    data analysis related to this hvac measure.

    The return value of this function is a tuple which lenght or size is
    determined by the number of fiscal years in the dataset such that the
    tupple size will always have x+1 dictionary items where x is the number of
    fiscal years present in the data. The first item in the tuple is
    a dictionary of the key: fiscal year and value: the pm to cm ratio for
    that fiscal year, the preceding dictionary item(s) returned by the fuction
    is a dictionary with key: fiscal year and value: dataframe subset filtered
    for the corresponding fiscal year. This is simply a subset of the main dataframe
    returned from the create_pm2cm_dataframe function or, in other words, a
    dataframe for each fiscal year.
    """
    fiscal_years, fiscal_year_dataframes,pm2cm_kpi = [],[],[]
    corrective_maintenance = ['BOILER','CHILLERS','COOLING TOWERS','HVAC',
                                'HVAC INFRASTRUCTURE','HVAC|REPAIR']
    preventative_maintenance = ['PREVENTIVE MAINT','HVAC|PM']
    hvac_problemtypes = corrective_maintenance + preventative_maintenance

    for yr in df['fiscal_year'].unique():
        fiscal_years.append(yr)
        fiscal_year_dataframes.append(df[df['fiscal_year']==yr])
    fiscal_year_dataframes = dict(zip(fiscal_years,fiscal_year_dataframes))

    for key,value in fiscal_year_dataframes.items():
        # divide sum of pm counts by sum of cm counts & get pct%
        pm2cm_kpi.append(
            value[value['prob_type'].isin(preventative_maintenance)]['prob_type'].value_counts().sum()\
            /
            value[value['prob_type'].isin(corrective_maintenance)]['prob_type'].value_counts().sum() *100
        )
    pm2cm_dict = dict(zip(fiscal_years,pm2cm_kpi))
    return pm2cm_dict, fiscal_year_dataframes
