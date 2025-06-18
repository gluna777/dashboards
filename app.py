from dash import Dash, html, dcc, Input, Output 
import plotly.express as px 
import pandas as pd  
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.read_excel("Vendas.xlsx")
df['Data'] = pd.to_datetime(df['Data'])

options = list(df['ID Loja'].unique())
options.append("Todas as Lojas")

# Valores mínimos e máximos da coluna Data para configurar o DatePickerRange
min_date = df['Data'].min()
max_date = df['Data'].max()

# Indicadores (KPIs)
total_produtos = df['Quantidade'].sum()
n_lojas = df['ID Loja'].nunique()

#cards KPI
kpi_cards = dbc.Row([
    dbc.Col(dbc.Card(dbc.CardBody([
        html.H4("Total de produtos vendidos", className="card-title"),
        html.H2(f"{total_produtos}", className="card-text")
    ]), color="primary", inverse=True), width=6),
    dbc.Col(dbc.Card(dbc.CardBody([
        html.H4("Número de Lojas", className="card-title"),
        html.H2(f"{n_lojas}", className="card-text")
    ]), color="success", inverse=True), width=6),
], className="mb-4")

# Gráfico inicial
fig = px.bar(df, x="Produto", y="Quantidade", color="ID Loja", barmode="group")

# Layout
app.layout = dbc.Container(children=[
    html.H1(children='Faturamento das lojas', className='my-4'),
    html.H2(children='Gráfico com faturamento de todos os produtos separados por loja'),
    html.Div(children='OBS: Gráfico mostra quantidade de produtos vendidos, não o faturamento'),

    kpi_cards,

    dcc.Dropdown(options, value='Todas as Lojas', id='lista_Lojas', className='mb-4'),

    dcc.DatePickerRange(
        id='seletor_data',
        start_date=min_date,
        end_date=max_date,
        min_date_allowed=min_date,
        max_date_allowed=max_date,
        display_format='DD/MM/YYYY',
        className='mb-4'
    ),

    dcc.Graph(
        id='grafico_qtde_vendas',
        figure=fig
    )
], fluid=True)

# Callback para atualizar gráfico
@app.callback(
    Output('grafico_qtde_vendas', 'figure'),
    Input('lista_Lojas', 'value'),
    Input('seletor_data', 'start_date'),
    Input('seletor_data', 'end_date')
)
def update_output(loja, start_date, end_date):
    tabela_filtrada = df[(df['Data'] >= start_date) & (df['Data'] <= end_date)]
    if loja != 'Todas as Lojas':
        tabela_filtrada = tabela_filtrada[tabela_filtrada['ID Loja'] == loja]
    fig = px.bar(tabela_filtrada, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
    return fig

if __name__ == '__main__':
    app.run(debug=True)