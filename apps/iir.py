import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import os
import numpy as np
import plotly.graph_objs as go
import winsound
import scipy.signal as sp
from scipy.io.wavfile import read,write # libreria para lectura de archivos de audio
from funtion import diseño_filtro_iir

from app import app

#VARIABLES GLOBALES
señal_audio = []
t_audio = []
fs_audio = 0
Nfiltro = []
Dfiltro = []
#app = dash.Dash()

layout = html.Div([
    html.H1(children = 'Filtro IIR',style={'textAlign': 'center','color': '#151282','fontFamily': 'sans-serif','paddingLeft': '0'}),
    html.Div(id='output-state1'),#Texto confirmacion audio
    dcc.Input(id='input-1-state', type="text", value='Cello.wav'),#Escoger audio
    html.Div([
        html.Button(id='submit-button', n_clicks=0, children='Cargar audio'),#Cargar audio     
    ],style={'display': 'inline-block'}),
    html.Div([
        html.Button(id='escuchar1', n_clicks=0, children='Escuchar')#Escuchar audio
    ],style={'display': 'inline-block'}),
    
    html.Div(id='hide11', style={'display':'none'}),
    html.Div(id='hide21', style={'display':'none'}),
    
    html.Div([dcc.Graph(id='Grafica-audio1')]),#Graficar audio escogido
        html.Div([
    html.H2(children='Tipo de filtro',
        style={'textAlign': 'center','color': '#151282','fontFamily': 'sans-serif','paddingLeft': '0'}
    ),
     dcc.Dropdown(#Selecionar tipo de filtro
         id='Tipo-filtro',
        options=[
            {'label': 'Pasa bajos', 'value': 'PB'},
            {'label': 'Pasa banda', 'value': 'PBN'},
            {'label': 'Pasa altas', 'value': 'PA'}            
        ],
         value='PB',
        placeholder="Seleccionar filtro"
        )   
    ],style={'textAlign': 'center','margin-left' : '150px','margin-right' : '150px'}),
    html.Div(id='sugerencia1',style={'display':'inline-block','margin-left':'20px'}),
    html.H2(children='Parametros del filtro',#Titulo parametros filtro
        style={'textAlign': 'center','color': '#151282','fontFamily': 'sans-serif','paddingLeft': '0'}),
    html.Div([#Boton graficar filtro
        html.Button(id='submit-button2', n_clicks=0, children='Graficar filtro')
    ],style={'text-align': 'center'}),
    html.Div([#Input boxes para la entrada de parametros    
                    html.Div([
                        html.H4(children='Banda de transición',
                            style={'textAlign': 'center','color': '#151282','fontFamily': 'sans-serif','paddingLeft': '0'}
                        ),
                        dcc.Input(id='BT', value=50, type="number"),
                    ],style={ 'display': 'inline-block'}),                    
                    html.Div([
                        html.H4(children='Fecuencia de corte 1',
                            style={'textAlign': 'center','color': '#151282','fontFamily': 'sans-serif','paddingLeft': '0'}
                        ),
                        dcc.Input(id='F1', value=400, type="number"),
                    ],style={ 'display': 'inline-block','margin-left':'20px'}),
                  
                  html.Div([
                        html.H4(children='Frecuencia de corte 2',
                            style={'textAlign': 'center','color': '#151282','fontFamily': 'sans-serif','paddingLeft': '0'}
                        ),
                        dcc.Input(id='F2', value=600, type="number"),
                  ],style={ 'display': 'inline-block','margin-left':'20px'}),       
                  html.Div([
                      html.H4(children='Frecuencia de muestreo',
                            style={'textAlign': 'center','color': '#151282','fontFamily': 'sans-serif','paddingLeft': '0'}
                        ),
                      dcc.Input(id='FS', value=1300, type="number")
                      ],style={'align':'center','display': 'inline-block','margin-left':'20px'}),
                  html.Div([
                      html.H4(children='Atenuacion en banda rechazada',
                            style={'textAlign': 'center','color': '#151282','fontFamily': 'sans-serif','paddingLeft': '0'}
                        ),
                      dcc.Input(id='RS', value=6, type="number")
                      ],style={'align':'center','display': 'inline-block','margin-left':'20px'})
              ],style={'text-align': 'center'}),

    html.Div(id='Grafica-filtro1'),#Graficar filtro elegido
    html.Div([#Boton graficar filtro
        html.Button(id='submit-button3', n_clicks=0, children='Graficar audio filtrado')
    ],style={'text-align': 'center'}),
    html.Div(id='Grafica-audio_filtro1'),#Grafica audio filtrado
    html.Button(id='b_hide', n_clicks=0, children='',style={'display':'none'}),
    html.Div([
        html.Button(id='escuchar2', n_clicks=0, children='Escuchar audio filtrado')#Escuchar audio filtrado    
    ],style={'text-align': 'center'})
],style={'backgroundColor':'white','margin-left' : '80px','margin-right' : '80px','margin-bottom':'100px','margin-top':'40px'})

#TEXTO CONFIRMACION AUDIO
@app.callback(Output('output-state1', 'children'),
              [Input('b_hide', 'n_clicks')],
              [State('input-1-state', 'value')
               ])
def update_output(n_clicks, input1):
    return u'''Audio: "{}"'''.format(input1)

#ESCUHAR AUDIO ORIGINAL
@app.callback(Output('hide11', 'children'),
              [Input('escuchar1', 'n_clicks')],
              [State('input-1-state', 'value')
               ])
def update_output(n_clicks,name_audio):
    winsound.PlaySound(name_audio, winsound.SND_FILENAME)
    return '''Audio: '''
#GRAFICA AUDIO
@app.callback(
    dash.dependencies.Output('Grafica-audio1','figure'),
    [dash.dependencies.Input('submit-button','n_clicks')],
    [State('input-1-state', 'value')]
    )
def update_audio(n_clicks, name_audio):
    
    file_audio=(name_audio) # Ruta del archivo con la senal
    fs, x=read(file_audio)
    x=x/float(max(abs(x))) # escala la amplitud de la senal
    
    global fs_audio
    fs_audio = fs
    global señal_audio
    señal_audio = x
    
    t=np.arange(0, float(len(x))/fs, 1.0/fs)
    
    global t_audio
    t_audio = t
   # winsound.PlaySound(name_audio, winsound.SND_FILENAME)
    return {
        'data': [
                {'x':t, 'y':x, 'type': 'line', 'name': name_audio},                               
            ],
            'layout': go.Layout(
                    title='Audio: ' + name_audio,
                    xaxis={'title': 'Tiempo (segundos)'},
                    yaxis={'type': 'line', 'title': 'Amplitud normalizada'}
                )       
    }
#PARAMETROS PARA FILTRO
@app.callback(Output('Grafica-filtro1', 'children'),
              [Input('submit-button2','n_clicks')],
              [State('F1','value'),
              State('FS','value'),
              State('F2','value'),              
              State('Tipo-filtro','value'),
              State('RS','value')])

def update_grafica_filtro(n,f1,fs,f2,tf,rs):
    
    x,y,y1,b,a = diseño_filtro_iir(f1,f2,fs,tf,rs)
    global Nfiltro
    Nfiltro = b
    global Dfiltro
    Dfiltro = a
    

    return  html.Div([
        html.Div([
        dcc.Graph(
            id ='filtro-frecuencia',
            figure = {
                'data':[
                        {'x': x, 'y': y, 'type': 'line', 'name': 'FILTRO frecuencia'},                               
                    ],
                    'layout':go.Layout(
                    title='Respuesta en frecuencia del filtro',
                    xaxis={'title': 'Frecuencia GHz'},
                    yaxis={'title': '|H(w)|'}
                )
            }
        )
        ],style={'width': '50%','display': 'inline-block'}),
        html.Div([
        dcc.Graph(
            id ='filtro-fase',
            figure = {
                'data':[
                        {'x': x, 'y':y1, 'type': 'line', 'name': 'FILTRO frecuencia'},                               
                    ],
                    'layout':  go.Layout(
                    title='Respuesta en fase del filtro',
                    xaxis={'title': 'Frecuencia GHz'},
                    yaxis={'title': '|H(w)|'}
                )
            }
        )
        ],style={'width': '50%','display': 'inline-block'})        
    ])




#CARGA GRAFICA DE AUDIO FILTRADO
@app.callback(Output('Grafica-audio_filtro1', 'children'),
              [Input('submit-button3','n_clicks')])

def update_audio_filtro(value):
    
    y = sp.lfilter(Nfiltro,Dfiltro,señal_audio)
    write('Filtrado.wav',int(fs_audio),y)
    
    return html.Div([
        dcc.Graph(
            id ='Audio_filtrado',
            figure = {
                'data':[
                        {'x': t_audio, 'y':y, 'type': 'line', 'name': 'FILTRO frecuencia'},                             
                    ],
                    'layout':go.Layout(
                    title='Respuesta en frecuencia del filtro',
                    xaxis={'title': 'Frecuencia GHz'},
                    yaxis={'title': '|H(w)|'}
                )
            }
        )
    ])

#ESCUCHAR AUDIO FILTRADO
@app.callback(Output('hide21', 'children'),
              [Input('escuchar2', 'n_clicks')],
              [State('input-1-state', 'value')
               ])
def update_output(n_clicks,name_audio):
    os.system("start file:///C:/Users/Orion/Google%20Drive/UNIVERSIDAD/PDS/Final/Filtrado.wav")
    return u'''Audio: '''

#Sugerencia frecuencia de muestreo
@app.callback(Output('sugerencia1', 'children'),
              [Input('Tipo-filtro','value'),               
              Input('F1','value'),
              Input('F2','value'),
              Input('FS','value')]
             )
def update_muestreo(tf,f1,f2,fs):
    f1 = float(f1)
    f2 = float(f2)
    fs = float(fs)
    if tf == 'PBN':
        if f1 > f2:
            return '''Error: {} > {}'''.format(f1,f2)
        elif 2*f2 > fs:
            return '''Error Frecuencia de muestreo, Frecuencia de muestreo debe ser dos veces mayor que {}'''.format(f2,f2)
        else:
            return ''''''
    else:
        if 2*f1 > fs:
            return '''Error Frecuencia de muestreo, Frecuencia de muestreo debe ser dos veces mayor que {}'''.format(f1,f1)
        
if __name__ == '__main__':
    app.run_server(debug=True)