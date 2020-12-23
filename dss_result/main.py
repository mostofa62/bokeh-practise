import sqlite3 as sql
import pandas.io.sql as psql
from os.path import dirname, join, abspath

from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Select

from bokeh.models.widgets import DataTable, TableColumn

db_path = join(dirname(dirname(abspath(__file__))), 'dss/dss.db')
conn = sql.connect(db_path)
query = open(join(dirname(__file__), 'query.sql')).read()
dssdata = psql.read_sql(query, conn)
dssdata.fillna(0, inplace=True)  # just replace missing values with zero

#print(dssdata.to_string())



#print(selected.to_string())


year_range = {
	'0':'All',
 	'100': 'Base Line',
    '2017': '2017',
    '2018': '2018',
    '2019': '2019'
}

year_control = Select(title="Year", options=sorted(year_range.keys()), value='0')

#ploting related
sourcetable = ColumnDataSource(data=dict(union=[], age_1to4=[]))


def select_dssdata():	
    year_val = year_control.value
    selected = dssdata
    if (year_val != '0'):
        selected = dssdata[(dssdata.Year == int(year_val))]
	
    return selected

def update():
	df = select_dssdata()

	sourcetable.data = dict(
        union=df["Union"],
        age_1to4=df["1_to_4"]        
    )



year_control.on_change('value', lambda attr, old, new: update())


#table data

columns = [
    TableColumn(field="union", title="Union"),
    TableColumn(field="age_1to4", title="1 to 4")
]

data_table = DataTable(source=sourcetable, columns=columns, width=400, height=280, index_position=None)

#ploting

update()  # initial load of the data
curdoc().add_root(column(year_control,data_table))
curdoc().title = "DSS RESULT"