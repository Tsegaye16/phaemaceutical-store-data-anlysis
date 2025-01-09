import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import logging


# Set up logging
logging.basicConfig(
    level=logging.DEBUG,  # Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("../log/visualization.log"),  # Log to a file
        logging.StreamHandler()                   # Log to console
    ]
)
logger = logging.getLogger(__name__)

def plotly_plot_pie(df, column, limit=None, title=None):
    logger.info("Starting pie chart plot for column: %s", column)
    try:
        a = pd.DataFrame({'count': df.groupby([column]).size()}).reset_index()
        a = a.sort_values("count", ascending=False)
        if limit:
            logger.debug("Applying limit: %s", limit)
            a.loc[a['count'] < limit, column] = f'Other {column}s'
        if title is None:
            title = f'Distribution of {column}'
        fig = px.pie(a, values='count', names=column, title=title, width=800, height=500)
        fig.show()
        logger.info("Pie chart plot completed successfully.")
    except Exception as e:
        logger.error("Error while plotting pie chart: %s", e)

def plotly_plot_hist(df, column, color=['cornflowerblue'], title=None):
    logger.info("Starting histogram plot for column: %s", column)
    try:
        if title is None:
            title = f'Distribution of {column}'
        fig = px.histogram(
            df,
            x=column,
            marginal='box',
            color_discrete_sequence=color,
            title=title
        )
        fig.update_layout(bargap=0.01)
        fig.show()
        logger.info("Histogram plot completed successfully.")
    except Exception as e:
        logger.error("Error while plotting histogram: %s", e)

def plotly_multi_hist(sr, rows, cols, title_text, subplot_titles):
    logger.info("Starting multi-histogram plot.")
    try:
        fig = make_subplots(rows=rows, cols=cols, subplot_titles=subplot_titles)
        for i in range(rows):
            for j in range(cols):
                x = ["-> " + str(k) for k in sr[i + j].index]
                fig.add_trace(go.Bar(x=x, y=sr[i + j].values), row=i + 1, col=j + 1)
        fig.update_layout(showlegend=False, title_text=title_text)
        fig.show()
        logger.info("Multi-histogram plot completed successfully.")
    except Exception as e:
        logger.error("Error while plotting multi-histogram: %s", e)

def plotly_plot_scatter(df, x_col, y_col, marker_size, hover=[]):
    logger.info("Starting scatter plot for columns: %s vs. %s", x_col, y_col)
    try:
        fig = px.scatter(
            df,
            x=x_col,
            y=y_col,
            opacity=0.8,
            hover_data=hover,
            title=f'{x_col} vs. {y_col}'
        )
        fig.update_traces(marker_size=marker_size)
        fig.show()
        logger.info("Scatter plot completed successfully.")
    except Exception as e:
        logger.error("Error while plotting scatter plot: %s", e)

def plot_hist(df: pd.DataFrame, column: str, color: str = 'cornflowerblue') -> None:
    logger.info("Starting histogram (Seaborn) plot for column: %s", column)
    try:
        sns.displot(data=df, x=column, color=color, kde=True, height=6, aspect=2)
        plt.title(f'Distribution of {column}', size=20, fontweight='bold')
        plt.show()
        logger.info("Seaborn histogram plot completed successfully.")
    except Exception as e:
        logger.error("Error while plotting Seaborn histogram: %s", e)

def plot_count(df:pd.DataFrame, column:str) -> None:
    plt.figure(figsize=(12, 7))
    sns.countplot(data=df, x=column)
    plt.title(f'Distribution of {column}', size=20, fontweight='bold')
    plt.show()

def plot_bar(df:pd.DataFrame, x_col:str, y_col:str, title:str, xlabel:str, ylabel:str)->None:
    plt.figure(figsize=(12, 7))
    sns.barplot(data = df, x=x_col, y=y_col)
    plt.title(title, size=20)
    plt.xticks(rotation=75, fontsize=14)
    plt.yticks( fontsize=14)
    plt.xlabel(xlabel, fontsize=16)
    plt.ylabel(ylabel, fontsize=16)
    plt.show()

def plot_heatmap(df:pd.DataFrame, title:str, cmap='Reds')->None:
    plt.figure(figsize=(12, 7))
    sns.heatmap(df, annot=True, cmap=cmap, vmin=0, vmax=1, fmt='.2f', linewidths=.7, cbar=True )
    plt.title(title, size=18, fontweight='bold')
    plt.show()

def plot_box(df:pd.DataFrame, x_col:str, title:str) -> None:
    plt.figure(figsize=(12, 7))
    sns.boxplot(data = df, x=x_col)
    plt.title(title, size=20)
    plt.xticks(rotation=75, fontsize=14)
    plt.show()

def plot_box_multi(df:pd.DataFrame, x_col:str, y_col:str, title:str) -> None:
    plt.figure(figsize=(12, 7))
    sns.boxplot(data = df, x=x_col, y=y_col)
    plt.title(title, size=20)
    plt.xticks(rotation=75, fontsize=14)
    plt.yticks( fontsize=14)
    plt.show()

def plot_scatter(df: pd.DataFrame, x_col: str, y_col: str) -> None:
    plt.figure(figsize=(12, 7))
    sns.scatterplot(data = df, x=x_col, y=y_col)
    plt.title(f'{x_col} Vs. {y_col}\n', size=20)
    plt.xticks(fontsize=14)
    plt.yticks( fontsize=14)
    plt.show()

def hist(sr):
    x = ["Id: " + str(i) for i in sr.index]
    fig = px.histogram(x=x, y=sr.values)
    fig.show()