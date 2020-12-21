import datetime
from os.path import dirname, join

import pandas as pd

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, DataRange1d, Select
from bokeh.plotting import figure
from bokeh.palettes import Spectral6

from bokeh.models.widgets import DataTable, TableColumn


"""
#year_range select
year = '1000'

year_range = {
    '1000': {
        'year': '1000',
        'title': 'Base Line',
    },
    '2017': {
        'year': '2017',
        'title': '2017',
    },
    '2018': {
        'year': '2018',
        'title': '2018',
    }
}

#year_select = Select(value=year, title='Year', options=sorted(year_range.keys()))


#year_select.on_change('value', update_plot)
"""
fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
years = ["2015", "2016", "2017"]
colors = ["#c9d9d3", "#718dbf", "#e84d60"]

'''
source = ColumnDataSource(data=dict(
    x=[10, 20, 30, 40, 50,60],
    x1=[11, 21, 44, 32, 41,56],
    x2=[22, 42, 23, 25, 35,45],
    x3=[21, 44, 22, 21, 35,41],
))
'''

data = {'fruits' : fruits,
        '2015'   : [2, 1, 4, 3, 2, 4],
        '2016'   : [5, 3, 4, 2, 4, 6],
        '2017'   : [3, 2, 4, 4, 5, 3]}

#s1 = figure(plot_width=400, plot_height=400)
s1 = figure(x_range=fruits, plot_height=250, title="Fruit Counts by Year",
           toolbar_location=None, tools="hover", tooltips="$name @fruits: @$name")

#s1.vbar_stack(['x1', 'x2','x3'], x='x', width=1, color=colors, source=source,legend_label=years)
s1.vbar_stack(years, x='fruits', width=0.9, color=colors, source=data,
             legend_label=years)

s1.y_range.start = 0
s1.x_range.range_padding = 0.1
s1.xgrid.grid_line_color = None
s1.axis.minor_tick_line_color = None
s1.outline_line_color = None
s1.legend.location = "top_left"
s1.legend.orientation = "horizontal"

##below will interrelated duo to same data source
counts = [5, 3, 4, 2, 4, 6]
s2source = ColumnDataSource(data=dict(fruits=fruits, counts=counts, color=Spectral6))
s2 = figure(x_range=fruits, y_range=(0,9), plot_height=250, title="Fruit Counts",
           toolbar_location=None, tools="")

s2.vbar(x='fruits', top='counts', width=0.9, color='color', legend_field="fruits", source=s2source)
s2.xgrid.grid_line_color = None
s2.legend.orientation = "horizontal"
s2.legend.location = "top_center"


columns = [
    TableColumn(field="fruits", title="Fruits"),
    TableColumn(field="counts", title="Counts")
]
data_table = DataTable(source=s2source, columns=columns, width=400, height=280, index_position=None)


curdoc().add_root(column(s1,s2,data_table))
curdoc().title = "BAR"