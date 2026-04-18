import matplotlib.pyplot as plt

def plot_anomalies(df):
    plt.figure(figsize=(10,5))
    
    plt.plot(df['date'], df['temperature'], label='Temperature')

    anomalies = df[df['anomaly']]
    plt.scatter(anomalies['date'], anomalies['temperature'], label='Anomaly')

    plt.legend()
    plt.title("Anomaly Detection")

    plt.savefig("outputs/plots/anomalies.png")