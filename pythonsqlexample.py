import sqlite3 as sql
import pandas.io.sql as psql
from os.path import dirname, join

conn = sql.connect("dss/dss.db")
query = open(join(dirname(__file__), 'query.sql')).read()
dssdata = psql.read_sql(query, conn)
dssdata.fillna(0, inplace=True)  # just replace missing values with zero

#print(dssdata.to_string())



#print(selected.to_string())


year_range = {
	"all":"All",
 	100: 'Base Line',
    2017: '2017',
    2018: '2018',
    2019: '2019'
}

year_control = Select(title="Year", options=sorted(year_range.keys()), value="all")

#ploting related
sourcetable = ColumnDataSource(data=dict(union=[], age_1to4=[]))


def select_dssdata():	
	year_val = year_control.value
	if (year_val != "all"):
		selected = dssdata[(dssdata.Year == year_val)]
	return selected

def update():
	df = select_dssdata()

	sourcetable.data = dict(
        union=df["Union"],
        age_1to4=df["1_to_4"]        
    )






#table data

columns = [
    TableColumn(field="union", title="Union"),
    TableColumn(field="age_1to4", title="1 to 4")
]

data_table = DataTable(source=sourcetable, columns=columns, width=400, height=280, index_position=None)

#ploting


curdoc().add_root(column(data_table))
curdoc().title = "DSS RESULT"