import plotly.graph_objects as go
from plotly.subplots import make_subplots

def returns_plot(dataframe, signal, long_only, momentum):
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Price trace LHS
    fig.add_trace(
        go.Scatter(x=dataframe.index, y=dataframe['adjClose'], name="Adj Close"),
        secondary_y=False,
    )

    # Aggregated Signal trace RHS
    fig.add_trace(
        go.Scatter(x=dataframe.index, y=dataframe[signal], name="Signal Direction"),
        secondary_y=True,
    )

    # Momentum Returns trace RHS
    fig.add_trace(
        go.Scatter(x=dataframe.index, y=dataframe[momentum], name="Momentum Returns"),
        secondary_y=True,
    )

    # Long only returns trace RHS
    fig.add_trace(
        go.Scatter(x=dataframe.index, y=dataframe[long_only], name="Long Only Return"),
        secondary_y=True,
    )

    # Add figure title
    fig.update_layout(
        title_text="Naive Momentum Returns"
    )

    # Set x-axis title
    fig.update_xaxes(title_text="Date")

    # Set y-axes titles
    fig.update_yaxes(title_text="<b>Adjusted Close Price</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>Cumulative Returns</b>", secondary_y=True)

    return fig