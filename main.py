import pandas            as pd
import numpy             as np
import quantstats        as qs
import streamlit         as st
import matplotlib.pyplot as plt
from   datetime          import timedelta


def simulate_portfolios(start_date,  end_date, num_securities, num_days, initial_cash):
    trade_dates        = pd.to_datetime(np.sort(np.random.choice(pd.date_range(start=start_date, end=end_date, periods=num_days + 1), num_days, replace=False)))

    df = pd.DataFrame({'datetime'  : trade_dates})
    df['datetime'] = pd.to_datetime(df['datetime'])
    df = df.set_index('datetime')

    for idx in range(0, num_securities):
        percentage_changes = np.random.uniform(-0.02, 0.02, num_days).astype(float)
        df[f"pct_change_{idx}"] = percentage_changes
        df[f"ret_path_{idx}"  ] = df[f"pct_change_{idx}"].cumsum()
        df[f"cash_path_{idx}" ] = (1+df[f"pct_change_{idx}"]).cumprod()*initial_cash


    sim_cols  = [col_name for col_name in df.columns if col_name.startswith("cash")]
    fig, ax = plt.subplots()
    for col_name in sim_cols:
        ax.plot(df[col_name])
    fig.autofmt_xdate()
    st.pyplot(fig)


    pass

def main():
    #st.set_page_config(layout="wide")
    st.markdown("### Demonstration of Shannon's demon")

    col01, col02, col03, col04 = st.columns(4)
    with col01:
        start_date = st.date_input('Start Date', min_value=None, max_value=None, key=None)
    with col02:
        num_securities = st.number_input('Number of securities', min_value=2, max_value=30, step=1, value=5)
    with col03:
        num_days = st.number_input("Days", min_value=120, max_value=1500, step=30, value=360)
    with col04:
        initial_cash = st.number_input("Initial cash $", min_value=10000, step=100, value=10000)

    end_date = (start_date + timedelta(days=num_days)) if start_date else None

    simulate_portfolios(start_date=start_date, end_date=end_date, num_securities=num_securities, num_days=num_days, initial_cash=initial_cash)

if __name__ == '__main__':
    main()