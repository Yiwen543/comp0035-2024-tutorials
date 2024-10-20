import pathlib
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def describe_dataframe(events_csv_df):
     # print(events_csv_df.shape)
     # print(events_csv_df.head , events_csv_df.tail)
     # print(events_csv_df.columns)
     print(events_csv_df.dtypes)
     # print(events_csv_df.info)
     # print(events_csv_df.describe)


def prepare_data(events_csv_df):
     #task2.04 dtype
     events_csv_df['start'] = pd.to_datetime(events_csv_df['start'], format='%d/%m/%Y')
     events_csv_df['end'] = pd.to_datetime(events_csv_df['end'], format='%d/%m/%Y')
     columns_to_change = ['countries', 'events', 'participants_m', 'participants_f', 'participants']
     events_csv_df[columns_to_change] = events_csv_df[columns_to_change].fillna(0).astype(int)
     
     #task2.05 merge
     npc_codes_df = pd.read_csv(path_to_npc_csv_file, usecols=['Name', 'Code'], encoding='utf-8', encoding_errors='ignore')
     merged_df = events_csv_df.merge(npc_codes_df, how='left', left_on='country', right_on='Name')
     # print(merged_df[['country', 'Code', 'Name']])

     #task2.06 removing cols
     events_csv_df = events_csv_df.drop(columns=['URL', 'disabilities_included', 'highlights'], axis=1)

     #task2.07 dealing missing values
     #delate useless column
     # events_csv_df = events_csv_df.drop(columns=['Name'], axis=1)
     # 填充 participants_m 和 participants_f 的缺失值
     events_csv_df.loc[:, 'participants_m'] = events_csv_df['participants_m'].ffill()
     events_csv_df.loc[:, 'participants_f'] = events_csv_df['participants_f'].ffill()
     # 删除未来年份的行并重置索引
     events_csv_df = events_csv_df.drop(index=[0, 17, 31])
     events_csv_df.reset_index(drop=True, inplace=True)

     # 替换国家名称
     replacement_names = {
          'UK': 'Great Britain',
          'USA': 'United States of America',
          'Korea': 'Republic of Korea',
          'Russia': 'Russian Federation',
          'China': "People's Republic of China"
     }
     events_csv_df['country'] = events_csv_df['country'].replace(replacement_names)


     #task2.08
     # 移除 'type' 列中每个值的前后空格
     events_csv_df['type'] = events_csv_df['type'].str.strip()

     # 将 'type' 列中的值转换为小写
     events_csv_df['type'] = events_csv_df['type'].str.lower()
     
     #task2.09 Adding new columns
     events_csv_df['start'] = pd.to_datetime(events_csv_df['start'])
     events_csv_df['end'] = pd.to_datetime(events_csv_df['end'])

     # 计算持续时间并将新列插入到 'end' 列之后
     events_csv_df.insert(events_csv_df.columns.get_loc('end') + 1, 'duration', (events_csv_df['end'] - events_csv_df['start']).dt.days.astype(int))

     #task 2.10 output prepared file
     output_path = 'src/tutorialpkg/data/paralympics_events_prepared.csv'
     events_csv_df.to_csv(output_path, index=False)
     
     return events_csv_df

def identify_and_handle_outliers(events_csv_df, column):
    # 计算 Q1、Q3 和 IQR
    Q1 = events_csv_df[column].quantile(0.25)
    Q3 = events_csv_df[column].quantile(0.75)
    IQR = Q3 - Q1

    # 计算上下边界
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # 识别并删除异常值
    df_cleaned = events_csv_df[(events_csv_df[column] >= lower_bound) & (events_csv_df[column] <= upper_bound)]
    return df_cleaned




if __name__ == '__main__':
     pth = pathlib.Path(__file__)
     try:
          paralympics_datafile_csv = pth.parent.parent / 'tutorialpkg' / 'data' / 'paralympics_events_raw.csv'
          path_to_npc_csv_file = pth.parent.parent /'tutorialpkg/data/npc_codes.csv'
          events_csv_df = pd.read_csv(paralympics_datafile_csv)
          # Filter the DataFrame to select only rows where 'type' is 'summer'
          # syntax: df = df[df['column_name'] == filter_value]
          summer_df = events_csv_df[events_csv_df['type'] == 'summer']
          # 使用该函数处理 'duration' 列的异常值
          events_csv_df = prepare_data(events_csv_df)
          df_prepared = identify_and_handle_outliers(events_csv_df, 'duration')
           # Create a histogram of the DataFrame
          events_csv_df.hist()
          # Show the plot
          plt.show()
          # df_romved_cols = removing_cols(events_csv_df)
          # print(df_romved_cols)
          # events_csv_df = dealing_missing_values(events_csv_df)
          # print(events_csv_df.isna().sum())
          

          print("Data has been saved to 'src/tutorialpkg/data/paralympics_events_prepared.csv'")
     except FileNotFoundError as e:
          print(f"File not found. Please check the file path. Error: {e}")

     
     
     
     

     
     



