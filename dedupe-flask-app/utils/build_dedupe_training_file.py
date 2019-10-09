import pandas as pd
import json

trainingDict = {}
trainingDict['distinct'] = []
trainingDict['match'] = []

df = pd.read_table('clean_copy_combined_8-14-19.csv', sep=',')

df2 = df.astype(str)

df3 = df2.sample(frac=0.10, random_state=200)

df3['match'] = df3['cwid'].duplicated(keep=False)

labeled_matches = df3[df3.match != False]
labeled_distinct = df3[df3.match == False]

distinct_list = labeled_distinct.T.to_dict().values()

fields = {
  'feild_1': 'givenName',
  'feild_2': 'surname',
  'feild_3': 'middleName',
  'feild_4': 'monthOfBirth',
  'feild_5': 'dayOfBirth',
  'feild_6': 'source',
  'feild_7': 'title',
  'feild_8': 'departmentLabel'
}
# Loop through all df rows that have Match == true
# create dictionary with the keys being the cwid

matchesDict = {}
for i in labeled_matches['cwid'].unique():
  matchesDict[i] = [{
    fields['feild_1']: labeled_matches[fields['feild_1']][j],
    fields['feild_2']: labeled_matches[fields['feild_2']][j],
    fields['feild_3']: labeled_matches[fields['feild_3']][j]
  } for j in labeled_matches[labeled_matches['cwid'] == i].index][:2]

matchList = []
for key, value in matchesDict.items():
  matchList.append((value[0],value[1]))
trainingDict['match'] = matchList

data = list(distinct_list)
distinctList = []
for i, k in zip(data[0::2], data[1::2]):
  record_1 = {
    fields['feild_1']: k[fields['feild_1']],
    fields['feild_2']: k[fields['feild_2']],
    fields['feild_3']: k[fields['feild_3']]
  }
  record_2 = {
    fields['feild_1']: i[fields['feild_1']],
    fields['feild_2']: i[fields['feild_2']],
    fields['feild_3']: i[fields['feild_3']]
  }
  
  distinctList.append((record_1, record_2))

trainingDict['distinct'] = distinctList

with open('pairs_training_file.json', 'w') as fp:
    json.dump(trainingDict, fp)
