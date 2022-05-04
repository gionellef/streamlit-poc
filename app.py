import functools
from pathlib import Path

import streamlit as st
from st_aggrid import AgGrid
from st_aggrid.shared import JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import pandas as pd
import plotly.express as px

chart = functools.partial(st.plotly_chart, use_container_width=True)
COMMON_ARGS = {
    "color": "course",
    "color_discrete_sequence": px.colors.sequential.Greens,
    "hover_data": [
        "college",
        "percent_of_account",
        "quantity",
        "current_population",
        "total_gain_loss_dollar",
        "total_gain_loss_percent",
    ],
}


@st.experimental_memo
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Take Raw Fidelity Dataframe and return usable dataframe.
    - snake_case headers
    - Include 401k by filling na type
    - Drop Cash accounts and misc text
    - Clean $ and % signs from values and convert to floats

    Args:
        df (pd.DataFrame): Raw fidelity csv data

    Returns:
        pd.DataFrame: cleaned dataframe with features above
    """
    df = df.copy()
    df.columns = df.columns.str.lower().str.replace(" ", "_").str.replace("/", "_")

    df.type = df.type.fillna("unknown")
    df = df.dropna()

    price_index = df.columns.get_loc("last_price")
    cost_basis_index = df.columns.get_loc("cost_basis_per_share")
    df[df.columns[price_index : cost_basis_index + 1]] = df[
        df.columns[price_index : cost_basis_index + 1]
    ].transform(lambda s: s.str.replace("$", "").str.replace("%", "").astype(float))

    quantity_index = df.columns.get_loc("quantity")
    most_relevant_columns = df.columns[quantity_index : cost_basis_index + 1]
    first_columns = df.columns[0:quantity_index]
    last_columns = df.columns[cost_basis_index + 1 :]
    df = df[[*most_relevant_columns, *first_columns, *last_columns]]
    return df


@st.experimental_memo
def filter_data(
    df: pd.DataFrame, account_selections: list[str], symbol_selections: list[str]
) -> pd.DataFrame:
    """
    Returns Dataframe with only accounts and symbols selected

    Args:
        df (pd.DataFrame): clean fidelity csv data, including account_name and symbol columns
        account_selections (list[str]): list of account names to include
        symbol_selections (list[str]): list of symbols to include

    Returns:
        pd.DataFrame: data only for the given accounts and symbols
    """
    df = df.copy()
    df = df[
        df.account_name.isin(account_selections) & df.symbol.isin(symbol_selections)
    ]

    return df


def main() -> None:
    st.header("Academic Affairs Dashboard :bar_chart:")

    with st.expander("Purpose"):
        st.write(Path("README.md").read_text())

#    st.subheader("Upload your CSV from Fidelity")
#    uploaded_data = st.file_uploader(
#        "Drag and Drop or Click to Upload", type=".csv", accept_multiple_files=False
#    )

#    if uploaded_data is None:
#        st.info("Using example data. Upload a file above to use your own data!")
        uploaded_data = open("example.csv", "r")
#    else:
#        st.success("Uploaded your file!")

    df = pd.read_csv(uploaded_data)
#    with st.expander("Raw Dataframe"):
#        st.write(df)

    df = clean_data(df)
#    with st.expander("Cleaned Data"):
#        st.write(df)
    
    st.sidebar.subheader("Select Dashboards:")

    # accounts = list(df.account_name.unique())
    # account_selections = st.sidebar.multiselect(
    #     "Select Accounts to View", options=accounts, default=accounts
    # )
    # st.sidebar.subheader("Filter Displayed Tickers")

    # symbols = list(df.loc[df.account_name.isin(account_selections), "symbol"].unique())
    # symbol_selections = st.sidebar.multiselect(
    #     "Select Ticker Symbols to View", options=symbols, default=symbols
    # )

    dashboard = list(df.upm_affairs.unique())
    account_selections = st.sidebar.selectbox(
        "Select Dashboards to View", options=dashboard
    )
    # st.sidebar.subheader("Filter Displayed Tickers")

    # symbols = list(df.loc[df.upm_affairs.isin(account_selections), "symbol"].unique())
    # symbol_selections = st.sidebar.multiselect(
    #     "Select Ticker Symbols to View", options=symbols, default=symbols
    # )

    # df = filter_data(df, account_selections, symbol_selections)
    # st.subheader("Enrollment Data")
    # cellsytle_jscode = JsCode(
    #     """
    # function(params) {
    #     if (params.value > 0) {
    #         return {
    #             'color': 'white',
    #             'backgroundColor': 'forestgreen'
    #         }
    #     } else if (params.value < 0) {
    #         return {
    #             'color': 'white',
    #             'backgroundColor': 'crimson'
    #         }
    #     } else {
    #         return {
    #             'color': 'white',
    #             'backgroundColor': 'slategray'
    #         }
    #     }
    # };
    # """
    # )

    # gb = GridOptionsBuilder.from_dataframe(df)
    # gb.configure_columns(
    #     (
    #         "last_price_change",
    #         "total_gain_loss_dollar",
    #         "total_gain_loss_percent",
    #         "today's_gain_loss_dollar",
    #         "today's_gain_loss_percent",
    #     ),
    #     cellStyle=cellsytle_jscode,
    # )
    # gb.configure_pagination()
    # gb.configure_columns(("account_name", "symbol"), pinned=True)
    # gridOptions = gb.build()

    # AgGrid(df, gridOptions=gridOptions, allow_unsafe_jscode=True)
    
    
    
    def draw_bar(y_val: str) -> None:
        fig = px.bar(df, y=y_val, x="course", **COMMON_ARGS)
        fig.update_layout(barmode="stack", xaxis={"categoryorder": "total descending"})
        chart(fig)

    account_plural = "s" # if len(account_selections) > 1 else ""
    st.subheader(f"Statistics of Student{account_plural}")
    totals = df.groupby("college", as_index=False).sum()
    #if len(account_selections) > 1:
    st.metric(
        "Total Enrolled Students",
        f"{totals.current_population.sum():.0f}",
        f"{totals.total_gain_loss_dollar.sum():.0f}",
    )
    for column, row in zip(st.columns(len(totals)), totals.itertuples()):
        column.metric(
            row.college,
            f"{row.current_population:.0f}",
            f"{row.total_gain_loss_dollar:.0f}",
        )

    fig = px.bar(
        totals,
        y="college",
        x="current_population",
        color="college",
        color_discrete_sequence=px.colors.sequential.Greens,
    )
    fig.update_layout(barmode="stack", xaxis={"categoryorder": "total descending"})
    chart(fig)



if __name__ == "__main__":
    st.set_page_config(
        "UPM Executive Dashboard",
        "📊",
        initial_sidebar_state="expanded",
        layout="wide",
    )
    main()
