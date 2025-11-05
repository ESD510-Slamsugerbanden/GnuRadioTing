import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import piss_filters as flt
from get_rssi import get_rssi



class permutation_controller:
    def __init__(self, T_s, start_theta):
        self.w_n = 4*np.pi
        self.highpass = flt.Highpass(self.w_n, T_s)
        self.lowpass = flt.Lowpass(self.w_n/4, T_s)
        self.T_s = T_s
        self.permu_A = np.deg2rad(3) #How big should the permutation be in radians
        self.ki = 1600
        self.ki2 = 100
        self.w_per = 10*np.pi
        self.probe_counter = 0
        self.theta_i = start_theta
        self.theta_i2 = 0
        self.permutation = 0
        self.i_log = []
        self.hp_log = []
        self.last = 0
        pass

    def compute(self, rssi):
        hp_res = self.highpass.filter(rssi)
        temp = self.lowpass.filter(self.T_s * self.permutation * hp_res * self.ki) 
        self.theta_i += temp
        self.theta_i2 += self.theta_i / self.ki
        
        self.hp_log.append(hp_res)
        self.i_log.append(temp * 1/self.T_s)
        self.permutation = self.permu_A * np.sin(self.probe_counter * self.T_s * self.w_per)
        self.probe_counter += 1
        
        
        return self.permutation + self.theta_i + self.theta_i2 * self.ki2




if __name__ == "__main__":

    theta = np.linspace(0, np.pi*2, 100)
    amplitude = 10* np.log10(get_rssi(theta)[0])
    
    
    
    T_s = 1/20
    t = 0
    theta_start = np.deg2rad(30)
    ctrl = permutation_controller(T_s, theta_start)
    rssi_res = []
    theta_res = []
    theta = theta_start
    theta_real = []
    time = np.arange(10/T_s)*T_s
    
    for t in time:
        rssi, theta_target =get_rssi(theta, t)
        rssi = rssi*0.6
        theta_real.append(theta_target)
        rssi_res.append(rssi)
        theta = ctrl.compute(rssi)
        theta_res.append(theta)

    # Opret subplots (2 rækker, 1 kolonne)
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.1,
        subplot_titles=("Real beacon position & estimated beacon position", "RSSI readings")
    )

    # Øverste plot (θ-data)
    fig.add_trace(go.Scatter(x=time, y=theta_real, name="Real theta"), row=1, col=1)
    fig.add_trace(go.Scatter(x=time, y=theta_res, name="Probed theta"), row=1, col=1)

    # Nederste plot (RSSI + kontrol)
    fig.add_trace(go.Scatter(x=time, y=rssi_res, name="RSSI readings"), row=2, col=1)
    fig.add_trace(go.Scatter(x=time, y=ctrl.i_log, name="Modulated reading"), row=2, col=1)
    fig.add_trace(go.Scatter(x=time, y=ctrl.hp_log, name="High pass filtered"), row=2, col=1)

    # Layout
    fig.update_layout(
        height=700,
        yaxis_title="Angle [rad]",
        xaxis2_title="Time [s]",
        yaxis2_title="RSSI",
        template="plotly_white"
    )

    # Gør legend fælles og pæn
    fig.update_layout(legend=dict(yanchor="top", y=1.05, xanchor="left", x=0.01))

    fig.show()

