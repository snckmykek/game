from sqlite_requests import db
import pandas as pd


df = pd.read_excel(r'speech.xlsx', sheet_name='Sheet1')

values = df.values

for s in values:
    s2 = list()
    for val in s:
        try:
            val = int(val)
        except:
            pass
        val = str(val)
        if val == 'nan':
            val = str()
        s2.append(val)
    s2[-1] = 0 if s2[-1] == '' else s2[-1]
    db.insert_speech(s2)
