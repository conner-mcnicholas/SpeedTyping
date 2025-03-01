import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
df_wpm = pd.read_csv('~/wpm/wpmdaily1000.csv')

def binnify(df,bincol,statcol,bin_size):
    
    df['bin'] = pd.cut(df[bincol], bins=range(int(df[bincol].min()), int(df[bincol].max()) + bin_size, bin_size))

    # Define the statistics you want to calculate
    stats = {
        'mean': 'mean',
        'min': 'min',
        'max': 'max',
        'med': 'median',
        'cnt': 'count',
        'std': 'std'
    }
    
    # Initialize the merged DataFrame with the 'bin' column
    merged_df = df.groupby('bin', observed=False).size().reset_index().rename(columns={0: 'size'}).drop(columns=['size'])

    for stat_name, func in stats.items():
            stat_df = df.groupby('bin', observed=False)[statcol].agg(func).round(1).reset_index().rename(columns={statcol: stat_name})
            #print(f"Shape of {stat_name} DataFrame: {stat_df.shape}")  # Debugging line
            merged_df = merged_df.merge(stat_df, on='bin', how='left')
    
    merged_df = merged_df[merged_df['cnt'] > 0]
    
    return merged_df.reset_index(drop=True)

def statbox(df,bincol,statcol,bin_size):
    
    df['bin'] = pd.cut(df[bincol], bins=range(int(df[bincol].min()), int(df[bincol].max()) + bin_size, bin_size))

    merged_df = binnify(df,bincol,statcol,bin_size)

    xwidths = [(w / max(list(merged_df.cnt)))**.8 for w in list(merged_df.cnt)]

    plt.figure(figsize=(10, 6))
    box_plot = sns.boxplot(x='bin', y=statcol, data=df, width=xwidths)
    plt.title(f'Box plot of {statcol} by {bincol} bins')
    plt.xlabel(bincol)
    plt.ylabel(statcol)
    bin_labels = [f'{int(interval.left)}' for interval in df['bin'].cat.categories]
    less_labels = bin_labels[0:len(bin_labels):int(7/bin_size)]
    plt.xticks(ticks=range(0,len(bin_labels),int(7/bin_size)), labels=less_labels, rotation=90)

    plt.show()

def plothisto(df,statcol):
    # Plot histogram
    print(f"int(df[statcol].max()-df[statcol].min()) = {(int(df[statcol].max()-df[statcol].min()))}")
    plt.figure(figsize=(10, 6))
    sns.histplot(df[statcol], bins=int(df[statcol].max()-df[statcol].min()), kde=True)
    plt.title(f'Histogram of {statcol}')
    plt.xlabel(statcol)
    plt.ylabel('Frequency')
    plt.show()


binnify(df_wpm,'wpm','accuracy',7).iloc[::5]

statbox(df_wpm,'wpm','accuracy',7)

plothisto(df_wpm,'accuracy')

plothisto(df_wpm,'consistency')

statbox(df_wpm,'wpm','consistency',1)

df_wpm[['wpm','raw','accuracy','consistency','diff']].corr()


