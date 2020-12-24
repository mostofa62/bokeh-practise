import sqlite3 as sql
import pandas.io.sql as psql
from os.path import dirname, join, abspath

from bokeh.io import curdoc
from bokeh.layouts import column, row, layout
from bokeh.models import ColumnDataSource, Select

from bokeh.models.widgets import DataTable, TableColumn

db_path = join(dirname(dirname(abspath(__file__))), 'dss/dss.db')
conn = sql.connect(db_path)
query = open(join(dirname(__file__), 'query.sql')).read()
dssdata = psql.read_sql(query, conn)
dssdata.fillna(0, inplace=True)  # just replace missing values with zero

import numpy as np



dssdata = dssdata.astype({'Union': 'int', 'Year':'int'})

#print(selected.to_string())

'''
year_range = {
	'0':np.nan,
 	'100': 'Base Line',
    '2017': '2017',
    '2018': '2018',
    '2019': '2019'
}
'''

year_range = {    
    'Base Line':{        
        'value':100
    },
    '2017':{
        'value':2017
    },
    '2018':{
        'value':2018
    },
    '2019':{
        'value':2019
    },
    '2020':{
        'value':2020
    }
}



'''
unions = {  
    '0': np.nan,  
    '1': "Nawabpur",
    '2': "Baharpur",
    '3': "Jamalpur",
    '4': "Islampur",
    '5': "Baliakandi",
    '6': "Jangal",
    '7': "Narua"
}
'''
unions = {
    'All':{
        'value':np.nan
    },  
    'Nawabpur':{
        'value':1
    },
    'Baharpur':{
        'value':2
    },
    'Jamalpur':{
        'value':3
    },
    'Islampur':{
        'value':4
    },
    'Baliakandi':{
        'value':5
    },
    'Jangal':{
        'value':6
    },
    'Narua':{
        'value':7
    }    
}


#dssdata["Union"]=dssdata["Union"].map(unions)

#print(dssdata.to_string())

year_control = Select(title="Year", options=sorted(year_range.keys()), value='2020')

union_control = Select(title="Union", options=sorted(unions.keys()), value='All')

#ploting related
sourcetable = ColumnDataSource(data=dict(union=[], age_1to4=[], year=[]))


def select_dssdata():	
    year_val = year_control.value
    union_val = union_control.value
    selected = dssdata
    if (year_val != 'All'):
        selected = selected[(dssdata.Year == year_range[year_val]['value'])]
    
    if (union_val != 'All'):
        selected = selected[(dssdata.Union == unions[union_val]['value'])]
    
	
    return selected

def update():
	df = select_dssdata()

	sourcetable.data = dict(
        union=df["Union"],
        age_1to4=df["1_to_4"],
        year=df["Year"]        
    )



#year_control.on_change('value', lambda attr, old, new: update())


#table data

columns = [
    TableColumn(field="union", title="Union"),
    TableColumn(field="age_1to4", title="1 to 4"),
    TableColumn(field="year", title="Year")
]

data_table = DataTable(source=sourcetable, columns=columns, width=400, height=280, index_position=None)




#ploting
controls = [year_control, union_control]
for control in controls:
    control.on_change('value', lambda attr, old, new: update())

inputs = column(*controls, width=320, height=1000)
l = layout([    
    [inputs, data_table],
], sizing_mode="scale_both")


update()  # initial load of the data
#curdoc().add_root(row(year_control,data_table))
curdoc().add_root(l)
curdoc().title = "DSS RESULT"