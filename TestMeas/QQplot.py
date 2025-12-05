import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from stationary_accuracy_mechanical import prepare_samples
from scipy import stats


if __name__ == "__main__":
    data = prepare_samples("LONGTIMELONGTIME2.csv")
    
    stats.probplot(data["POS"], dist="norm", plot=plt)
    plt.show()
