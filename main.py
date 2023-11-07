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

    allocated_cash = initial_cash/num_securities
    for idx in range(0, num_securities):
        percentage_changes = np.random.uniform(-0.12, 0.12, num_days).astype(float)
        df[f"pct_change_{idx}"] = percentage_changes
        df[f"ret_path_{idx}"  ] = df[f"pct_change_{idx}"].cumsum()
        df[f"cash_path_{idx}" ] = (1+df[f"pct_change_{idx}"]).cumprod()*(allocated_cash)


    sim_cols  = [col_name for col_name in df.columns if col_name.startswith("cash")]
    fig, ax = plt.subplots()
    for col_name in sim_cols:
        ax.plot(df[col_name])
    fig.autofmt_xdate()
    st.pyplot(fig)

    df['raw_portfolio_cash_path'] = df[sim_cols].sum(axis=1)

    col11, col12 = st.columns(2)
    rebalancing_options = {
        'W': "Weekly rebalance",
        'M': "Monthly rebalance",
        'Q': "Quarterly rebalance"
    }
    with col11:
        rebalancing_frequency = st.selectbox('Rebalancing period:', list(rebalancing_options.keys()), 
                               format_func=lambda option: rebalancing_options[option], 
                               index=list(rebalancing_options.keys()).index("M"))


    # for simplicity let's do equally weighted allocation
    rebalanced_portfolio_values = []
    rebalanced_dates            = []

    current_portfolio_value = initial_cash
    for date, group in df.groupby(pd.Grouper(freq=rebalancing_frequency)):
        group_df = group.copy()
        allocated_cash = current_portfolio_value/num_securities # equally weighted
        print(f"allocated cash for {date}: {allocated_cash}")
        for idx in range(0, num_securities):
            group_df[f"rebalanced_cash_path_{idx}" ] = (1+group_df[f"pct_change_{idx}"]).cumprod()*(allocated_cash)
        
        rebalanced_cash_cols  = [col_name for col_name in group_df.columns if col_name.startswith("rebalanced_cash_path")]
        current_portfolio_value = group_df.iloc[-1][rebalanced_cash_cols].sum()

        rebalanced_portfolio_values.append(current_portfolio_value)
        rebalanced_dates.append(date)
        pass

    col21, col22 = st.columns(2)
    with col21:
        st.markdown(f"##### Portfolio with rebalancing")
        rebalanced_df = pd.DataFrame(index=rebalanced_dates)
        df.index = pd.to_datetime(df.index)
        rebalanced_df['value'] = rebalanced_portfolio_values
        fig, ax = plt.subplots()
        ax.plot(rebalanced_df['value'])
        fig.autofmt_xdate()
        st.pyplot(fig)
        pass
    with col22:
        st.markdown("##### Portfolio with no rebalance")
        fig, ax = plt.subplots()
        ax.plot(df['raw_portfolio_cash_path'])
        fig.autofmt_xdate()
        st.pyplot(fig)
        pass


    pass

def main():
    #st.set_page_config(layout="wide")
    st.markdown("### Demonstration of Shannon's demon")

    col01, col02, col03, col04 = st.columns(4)
    with col01:
        start_date = st.date_input('Start Date', min_value=None, max_value=None, key=None)
    with col02:
        num_securities = st.number_input('Number of securities', min_value=2, max_value=50, step=1, value=5)
    with col03:
        num_days = st.number_input("Days", min_value=120, max_value=1500, step=30, value=360)
    with col04:
        initial_cash = st.number_input("Initial cash $", min_value=10000, step=100, value=10000)

    end_date = (start_date + timedelta(days=num_days)) if start_date else None

    simulate_portfolios(start_date=start_date, end_date=end_date, num_securities=num_securities, num_days=num_days, initial_cash=initial_cash)

if __name__ == '__main__':
    main()