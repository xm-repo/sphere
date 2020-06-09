import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":

    plt.style.use('ggplot')

    example = "132.g2.10.cnf"

    df = pd.read_csv(example + '.csv')
    print(df.head())

    rows = []
    names = []
    for index, row in df.iterrows():
        names.append(row.values[0])
        rows.append(row.values[2:])

    
    temp_df = []
    for index, row in enumerate(rows):
        d = dict()
        d[index] = row
        temp_df.append(d)     

    for index, row in enumerate(rows):
        y = np.array(row, dtype=float)
        # Add some random "jitter" to the x-axis
        x = np.random.normal(index, 0.15, size=len(y))
        plt.plot(x, y, 'k.', alpha=0.5, markersize=10)

    plt.scatter(range(len(rows)), np.mean(rows, axis=1), c='r', marker="*", s=100, zorder=10)

    #sns.boxplot(data=rows)

    plt.title(example)
    plt.xlabel('solver')
    plt.ylabel('seconds')
    plt.xlim(-0.5, len(rows) - 0.5)

    plt.xticks(range(len(rows)), df["solver"], rotation=70)

    #plt.tight_layout()
    plt.gcf().subplots_adjust(bottom=0.2)
    plt.show()

    ax = sns.swarmplot(data=rows, color=".25")
    ax.set_xticklabels(labels=df["solver"].values, rotation=90)    
    #ax.set_xticks(range(1, len(rows)+1), df["solver"].values)
    plt.gcf().subplots_adjust(bottom=0.2)
    #plt.tight_layout()
    plt.show()
