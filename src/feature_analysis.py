import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import copy
plt.style.use('seaborn')
business_indicators = pd.read_csv('../data/경기종합지수_10222514.csv')
business_indicators = business_indicators.transpose()
business_indicators = business_indicators.drop(index=['통계표', '계정항목', '단위', '변환'])
business_indicators.columns = ['선행지수순환변동치', '동행지수순환변동치']
business_indicators.index = pd.to_datetime(business_indicators.index)
business_indicators['선행지수순환변동치'] = business_indicators['선행지수순환변동치'].astype(float)
business_indicators['동행지수순환변동치'] = business_indicators['동행지수순환변동치'].astype(float)
business_indicators = business_indicators.sort_index()


market_rate = pd.read_csv('../data/시장금리(월,분기,년)_08204749.csv')
market_rate = market_rate.transpose()
market_rate = market_rate.drop(index=['통계표', '계정항목', '단위', '변환'])
market_rate.columns = ['3year', '10year']
market_rate.index = pd.to_datetime(market_rate.index)
market_rate['3year'] = market_rate['3year'].astype(float)
market_rate['10year'] = market_rate['10year'].astype(float)
market_rate['10year-3year'] = market_rate['10year'] - market_rate['3year']
market_rate = market_rate.sort_index()


kospi = pd.read_csv('../data/코스피지수 내역.csv')
kospi['날짜'] = pd.to_datetime(kospi['날짜'])
kospi.index = kospi['날짜']
kospi = kospi.drop(columns=['날짜', '오픈', '고가', '저가', '거래량', '변동 %'])
kospi = kospi.sort_index()


# %% Draw
plt.close('all')
f, ax = plt.subplots(1, 1)
color = 'tab:red'
ax.plot(kospi.index, kospi['종가'], color=color, label='kospi')
ax.set_ylabel('kospi', color=color)
ax.set_xlabel('time')
ax2 = ax.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:blue'
# we already handled the x-label with ax1
ax2.set_ylabel('market_rate', color=color)
ax2.plot(market_rate.index,
         market_rate['10year-3year'], color=color, label='10year-3year')
ax.legend(loc='upper left')
ax2.legend(loc='upper right')
plt.title('KOSPI VS 10Y-3Y Treasury')
plt.show()



#%%
f, ax = plt.subplots(1, 1)
color = 'tab:red'
ax.plot(kospi.index, kospi['종가'], color=color, label='kospi')
ax.set_ylabel('kospi', color=color)
ax.set_xlabel('time')
ax2 = ax.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:blue'
# we already handled the x-label with ax1
ax2.set_ylabel('Leading Index', color=color)
ax2.plot(business_indicators.index,
         business_indicators['선행지수순환변동치'], color=color, label='Leading Index')
ax.legend(loc='upper left')
ax2.legend(loc='upper right')
plt.title('KOSPI VS Leading Index')
plt.show()


# %% Analysis

df = pd.merge(kospi, market_rate, left_index=True, right_index=True)
df = pd.merge(df, business_indicators, left_index=True, right_index=True)
df = df.dropna()
df = df.sort_index()
print("Correlation")
print("1. After 2008")
print(df.corr())

# %% After 2015
after_2015 = df['2015-01-01':]
print("2. After 2015")
print(after_2015.corr())

#%%
def cal_add_month_correlation(kospi, target_df, add_month):
    target_df = copy.deepcopy(target_df)
    target_df.index = target_df.index + \
        pd.DateOffset(months=add_month)
    df = pd.merge(kospi, target_df,
                  left_index=True, right_index=True)
    df = df.dropna()
    df = df.sort_index()
    print(df.corr())
    return df.corr()
    
    
after_2015_kospi = kospi['2015-01-01':]
after_2015_business_indicators = business_indicators['2015-01-01':]
cal_add_month_correlation(after_2015_kospi, after_2015_business_indicators, 0)

# # %% Add one month
# market_rate_add_one_month = copy.deepcopy(market_rate)
# plus_month_period = 3
# market_rate_add_one_month.index = market_rate_add_one_month.index + \
#     pd.DateOffset(months=plus_month_period)

# df = pd.merge(kospi, market_rate_add_one_month,
#               left_index=True, right_index=True)
# df = df.dropna()
# df = df.sort_index()
# print("Correlation")
# print(df.corr())

# # %% After 2015
# after_2015 = df['2015-01-01':]
# print("Correlation")
# print(after_2015.corr())
