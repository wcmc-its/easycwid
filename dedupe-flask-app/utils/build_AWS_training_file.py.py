import pandas as pd
import json
from pandas.io.json import json_normalize

def json():
  my_df = pd.read_table('data.csv', sep=',')
  data = my_df.to_json(orient='columns')

  with open('aws_labeled_json.txt', 'w') as outfile:
    json.dump(data, outfile)

def prepare_aws():

  df = pd.read_table('data.csv', sep=',')

  df.drop(columns=['id', 'sorid', 'prefix', 'suffix', 'departmentcode', 'npi', 'mobilephone', 'email', 'postalcode', 'startdate', 'createtimestamp',
                 'modifytimestamp', 'location', 'type', 'visibility',	'genderscore', 'additionaltitle', 'additionalorganization', 'additionalorganizationid'], inplace=True)

  df['cluster_id'] = df['cluster id'].replace('null', np.NaN)

  labeled_matches = df[df.match != False]
  labeled_distinct = df[df.match != True]

  train_match = labeled_matches.head(600)
  train_distinct = labeled_distinct.sample(n=500, random_state=1)

  td = pd.concat([train_distinct, train_match]).reset_index(drop=True)

  ## This class handles the Negative examples through the groupby
  # df = df[df['label'] == True]

  class fillna_special_class():
      def __init__(self, max_cluster):
          self.cluster_max = max_cluster-1

      def fillna_special(self, x):
          if np.isnan(x):
              self.cluster_max += 1
              return self.cluster_max+1
          else:
              return x

  fillna_special = fillna_special_class(td['cluster_id'].max())
  td['cluster_id'] = td['cluster_id'].apply(
      lambda x: fillna_special.fillna_special(x))

  df_group = td.groupby('cluster_id').agg(list).reset_index()

  NUM_PER_SET = 10

  def unpack_list(col_names, record):
      z = list(zip(col_names, record))
      d = {key: val for key, val in z}
      return pd.DataFrame(d)

  col_names = ['cluster_id', 'cwid', 'surname', 'middlename', 'givenname' 'title', 'departmentlabel', 'monthofbirth', 'dayofbirth', 'source',
               'cluster id', 'labeling_set_id', 'label']
  df_cat = pd.DataFrame(columns=col_names)

  labeling_set_count = 0
  labeling_set_id = 0
  for cluster in df_group.values:
      new_items = unpack_list(col_names, cluster)
      new_items['labeling_set_id'] = labeling_set_id
      labeling_set_count += len(new_items)
      df_cat = pd.concat([df_cat, new_items], sort=False)
      if labeling_set_count >= NUM_PER_SET:
          labeling_set_count = 0
          labeling_set_id += 1

  df_cat = df_cat.reset_index(drop=True)
  df_cat.to_csv('aws-new-labels.csv')

prepare_aws()
