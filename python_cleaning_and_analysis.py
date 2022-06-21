import pandas as pd
import numpy as np
import ipywidgets as widgets
import matplotlib.pyplot as plt
%matplotlib inline

# loading first dataframe - average house price by region and size

df_price = pd.read_csv('C:/coding/Python/practice/real_estate/아파트 전용면적별 매매평균가격 (2016년 1월부터).csv')
df_price = df_price.set_index(['region', 'size (sq m)'])

# fixing columns for October which lost the last '0' when converted into csv - e.g. 2016.1 -> 2016.10

for col in df_price.columns.tolist():
    if len(col) == 6:
        df_price.rename({'{}'.format(col): '{}'.format(col) + '0'}, axis=1, inplace=True)
    else:
        continue
        
df_price = df_price.transpose()

# adding MoM (month over month) price change rate dataframe

df_price_mom = df_price.pct_change()*100
df_price_mom = df_price_mom.replace(np.nan, 0)

# loading second dataframe - population

df_pop = pd.read_csv('C:/coding/Python/practice/real_estate/행정구역_시군구_별__성별_인구수.csv')
df_pop = df_pop.set_index('region')

# fixing columns for October which lost the last '0' when converted into csv - e.g. 2016.1 -> 2016.10

for col in df_pop.columns.tolist():
    if len(col) == 6:
        df_pop.rename({'{}'.format(col): '{}'.format(col) + '0'}, axis=1, inplace=True)
    else:
        continue
        
df_pop = df_pop.transpose()

# loading thrid dataframe - number of new houses sold (new supply in housing market)

df_supply = pd.read_csv('C:/coding/Python/practice/real_estate/지역별_신규_분양세대수.csv')
df_supply = df_supply.set_index('region')
df_supply

# fixing columns for October which lost the last '0' when converted into csv - e.g. 2016.1 -> 2016.10

for col in df_supply.columns.tolist():
    if len(col) == 6 and col != 'region':
        df_supply.rename({'{}'.format(col): '{}'.format(col) + '0'}, axis=1, inplace=True)
    else:
        continue
        
df_supply = df_supply.transpose()

# loading fourth dataframe - base interest rate by bank of Korea

df_int_rate = pd.read_csv('C:/coding/Python/practice/real_estate/월별 금리.csv')
df_int_rate = df_int_rate.set_index(['month'])

# fixing columns for October which lost the last '0' when converted into csv - e.g. 2016.1 -> 2016.10

for col in df_int_rate.columns.tolist():
    if len(col) == 6:
        df_int_rate.rename({'{}'.format(col): '{}'.format(col) + '0'}, axis=1, inplace=True)
    else:
        continue

df_int_rate = df_int_rate.transpose()

# changing df_int_rate format so that it can be used for interactive dropbox later

df_int_rate = df_int_rate.rename(columns={'base interest rate':'Total'})

list_of_regions = list(set(df_price.columns.droplevel(1)))

for region in list_of_regions:
    df_int_rate[region] = df_int_rate['Total']
    

# reorder region and size list that will be used for dropbox

list_of_df_x = [df_supply, df_pop, df_int_rate]
list_of_df_y = [df_price, df_price_mom]
regions_reordered = ['Total', 'Seoul', 'Busan', 'Daegu', 'Incheon', 'Gwangju', \
                   'Daejeon', 'Ulsan', 'Sejong', 'Gyeonggi', 'Gangwon', \
                   'Chungcheong, North', 'Chungcheong, South', 'Jeonla, North', 'Jeonla, South', \
                   'Gyeongsang, North', 'Gyeongsang, South']
sizes_reordered = ['x<=60', '60<x<=85', '85<x<=102', '102<x<=135', '135<x']


# dropboxes for choosing x and y variables - with regards to list_of_df

widget_var_x = widgets.Dropdown(options = [('House supply', 0), ('Population', 1), ('Korean base interest rate', 2)], \
                      description = 'x variable')
widget_var_y = widgets.Dropdown(options = [('Price (mil KRW)', 0), ('Price change (MoM)', 1)], \
                      description = 'y variable')

# dropboxes for filtering by region and size

widget_region = widgets.Dropdown(options = regions_reordered, description = 'region')
widget_size = widgets.Dropdown(options = sizes_reordered, description = 'sq m')

# interactive dropboxes, correlation coefficient and line graph 

@widgets.interact(variable_x = widget_var_x, variable_y = widget_var_y, region = widget_region, size = widget_size)
def update(variable_x, variable_y, region, size):
    
    df_variable_x = list_of_df_x[variable_x]
    df_variable_y = list_of_df_y[variable_y]
    
    fig, ax1 = plt.subplots()

    ax2 = ax1.twinx()
    ax1.plot(df_variable_y.index, df_variable_x[region], 'g-')
    ax2.plot(df_variable_y.index, df_variable_y[region][size], 'b-')
    ax1.set_xticks(df_variable_y.index[len(df_variable_x.index)%6-1::3])
    ax1.set_xticklabels(df_variable_y.index[len(df_variable_x.index)%6-1::3], rotation=90)

    ax1.set_ylabel(widget_var_x.options[variable_x][0], color='g') 
    ax2.set_ylabel(widget_var_y.options[variable_y][0], color='b')
    plt.axhline(y=0.0, color='r', linestyle='-')
    
    plt.title(widget_var_x.options[variable_x][0] + ' and ' + widget_var_y.options[variable_y][0])
    
    print('correlation coefficient between {} and {}: '.format(widget_var_x.options[variable_x][0], widget_var_y.options[variable_y][0]))
    print(np.corrcoef(x=df_variable_x[region], y=df_variable_y[region][size])[0][1])
