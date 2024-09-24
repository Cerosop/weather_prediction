import os
import pandas as pd
import sqlite3

y = 2011
yr = 2024 - y

conn = sqlite3.connect('期末/data.db')
cur = conn.cursor()
cur.execute(f"DELETE FROM record")
conn.commit()

data = {}

for k in range(yr):
    csv_folder = '期末/csv/' + str(y + yr - k - 1)

    csv_files = [f for f in os.listdir(csv_folder) if f.endswith('.csv')]

    for csv_file in csv_files:
        csv_path = os.path.join(csv_folder, csv_file)
        df = pd.read_csv(csv_path)
        
        for j in range(1, 13):
            for i in range(31):
                d = (j * 31 + i) * yr + k
                
                if not data.get(d):
                    data[d] = [d]
                tmp = []
                if df.iloc[i, j] == '--' or df.iloc[i, j] == 'T':
                    tmp = 0
                elif type(df.iloc[i, j]) == str:
                    if df.iloc[i, j].find('/') != -1:
                        tmp = df.iloc[i, j].replace(' ', '').split('/')
                        if tmp[0] == '--' or tmp[0] == 'T':
                            tmp[0] = 0
                        else:
                            tmp[0] = float(tmp[0])
                        if tmp[1] == '--' or tmp[1] == 'T':
                            tmp[1] = 0
                        else:
                            tmp[1] = float(tmp[1])
                    else:
                        tmp = float(df.iloc[i, j])
                        
                if tmp == []:
                    data[d].append(df.iloc[i, j])
                elif type(tmp) == list:
                    data[d].append(tmp[0])
                    data[d].append(tmp[1])
                    
                else:
                    data[d].append(tmp)
                
data = {k: data[k] for k in data if data[k][5] != 0}
data = dict(sorted(data.items()))
# print(data)
for k in data:
    d = data[k]
    cur.execute(f'insert into record values({d[0]}, {d[5]}, {d[8]}, {d[7]}, {d[6]}, {d[1]}, {d[2]}, {d[4]}, {d[3]})')
    conn.commit()
conn.close()
