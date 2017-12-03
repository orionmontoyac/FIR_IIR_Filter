from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from app import app
from apps import Final,iir

# archivo principal 
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    html.H1(children = 'Filtros',style={'textAlign': 'center','color': '#151282','fontFamily': 'sans-serif'}),
    html.Div([dcc.Link('Filtro Fir', href='/apps/app1')],
             style={'textAlign': 'center','fontFamily': 'sans-serif','border-style': 'solid','margin-left':'200px','margin-right' : '200px'}),    
    
    html.Div([dcc.Link('Filtro IIr', href='/apps/app2')],
             style={'textAlign': 'center','fontFamily': 'sans-serif','border-style': 'solid','margin-left':'200px','margin-right' : '200px','margin-top':'20px'}),   
    
],style={'margin-top':'20px','margin-left':'20px','margin-right' : '20px'})


@app.callback(Output('page-content', 'children'),#Añandiendo archifos FIR e IIR
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/app1':
         return Final.layout
    elif pathname == '/apps/app2':
         return iir.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)