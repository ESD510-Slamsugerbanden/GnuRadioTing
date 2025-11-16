from angle_corr import get_rssi
import numpy as np
import pandas as pd




import numpy as np
import pandas as pd

if __name__ == "__main__":
    scan_width = np.deg2rad(60)
    n = 10

    # Opret vinkel-array
    theta_array = np.linspace(-scan_width, scan_width, n)

    # Her gemmes resultater fra get_rssi()
    sim_results = []

    for theta in theta_array:
        rssi = np.abs(get_rssi(theta))
        rssi_norm = rssi / np.sqrt(np.sum(np.square(rssi)))  # normaliser
        sim_results.append(rssi_norm)

    # Konverter til DataFrame
    sim_results = np.array(sim_results)

    results = pd.DataFrame({
        "theta": theta_array,
        "p0": sim_results[:, 0],
        "p1": sim_results[:, 1],
        "p2": sim_results[:, 2],
        "p3": sim_results[:, 3],
    })

    print(results.head())
    results.to_csv("Simulated_results_directionfinder.csv")