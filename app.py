from dash import Dash, html, dcc, Input, Output 
import plotly.express as px 
import pandas as pd  

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.read_excel("Vendas.xlsx")
options = list(df['ID Loja'].unique())
options.append("Todas as Lojas")

# criando o gráfico
fig = px.bar(df, x="Produto", y="Quantidade", color="ID Loja", barmode="group")

app.layout = html.Div(children=[
    html.H1(children='Faturamento das lojas'),
    html.H2(children='Gráfico com faturamento de todos os produtos separados por loja'),
    html.Div(children='OBS: Gráfico mostra quantidade de produtos vendidos, não o faturamento'),

    dcc.Dropdown(options, value='Todas as Lojas', id='lista_Lojas'),

    dcc.Graph(
        id='grafico_qtde_vendas',
        figure=fig
    )
])

@app.callback(
    Output('grafico_qtde_vendas', 'figure'),
    Input('lista_Lojas', 'value')
)
def update_output(value):
    if value == 'Todas as Lojas':
        fig = px.bar(df, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
    else:
        tabela_filtrada = df.loc[df['ID Loja']==value, :]
        fig = px.bar(tabela_filtrada, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
    return fig

if __name__ == '__main__':
    app.run(debug=True)