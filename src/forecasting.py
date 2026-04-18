from statsmodels.tsa.arima.model import ARIMA

def forecast_temperature(df):
    df = df.set_index('date')
    series = df['temperature']

    model = ARIMA(series, order=(2,1,2))
    model_fit = model.fit()

    forecast = model_fit.forecast(steps=30)

    return forecast