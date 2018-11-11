import pandas as pd
from pandas import DataFrame,Series
from sqlalchemy import create_engine

def find_id():
    engine = create_engine('sqlite:///database.db', echo=False)
    id =list(set(pd.read_sql_table('relation',con=engine)['id']))
    ids=[]
    for i in id:
        x=(i,i)
        ids.append(x)
    print(ids)
    return ids

def relation_to_database(filename=''):
    filedir = 'static/csvfile/'+filename
    engine = create_engine('sqlite:///database.db', echo=False)
    df=pd.read_csv(filedir,dtype=str)
    df['id']= filename
    df.columns=['phone_num','depart','id']
    df.to_sql('relation',con=engine,if_exists='append',index=False)