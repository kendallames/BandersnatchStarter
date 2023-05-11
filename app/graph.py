from altair import Chart, Tooltip
from pandas import DataFrame


def chart(df: DataFrame, x: str, y: str, target: str) -> Chart:
    """ Creates a chart that displays the x, y and target from the Dataframe. Modified configurations of the graph to
    make the graph visually appealing."""

    font = 'Calibre'
    graph = Chart(
        data=df,
        background="#222222",
        title=f"{y} by {x} for {target}",
    ).mark_circle(
        size=100
    ).encode(
        x=x,
        y=y,
        color=target,
        tooltip=Tooltip(df.columns.to_list())
    ).properties(
        width=500,
        height=500,
        padding=32
    ).configure_title(
        fontSize=30,
        font=font,
        color='white',
    ).configure_legend(
        labelFont=font,
        titleFont=font,
        titleColor='white',
        labelColor='white',
        labelFontSize=12,
        titlePadding=15,
        titleFontSize=15
    ).configure_axis(
        labelFont=font,
        titleFont=font,
        titleColor='white',
        labelColor='white',
        titleFontSize=20,
        labelFontSize=12,
        titlePadding=15
    )

    return graph
