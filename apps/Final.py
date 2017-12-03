import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import os
import numpy as np
import plotly.graph_objs as go
import winsound
from scipy.io.wavfile import read,write # libreria para lectura de archivos de audio
from funtion import diseño_filtro
from app import app
#VARIABLES GLOBALES
señal_audio = []
t_audio = []
h_filtro = []
fs_audio = 0

dcc._css_dist[0]['relative_package_path'].append('style.css')

#app = dash.Dash()
layout = html.Div([
    html.H1(children = 'Filtro FIR',style={'textAlign': 'center','color': '#151282','fontFamily': 'sans-serif','paddingLeft': '0'}),
    html.Div(id='output-state'),
    dcc.Input(id='input-1-state', type="text", value='Cello.wav'), #entrada nombre de archivo
    html.Div([
        html.Button(id='submit-button', n_clicks=0, children='Cargar audio'), #Cargar audio      
    ],style={'display': 'inline-block'}),
    html.Div([
        html.Button(id='escuchar1', n_clicks=0, children='Escuchar')#Escuchar audio
    ],style={'display': 'inline-block'}),
    
    html.Div(id='hide1', style={'display':'none'}),
    html.Div(id='hide2', style={'display':'none'}),
      
    html.Div([dcc.Graph(id='Grafica-audio')]),#Grafica Audio
    
    html.Div([
        html.H2(children='Tipo de ventana',
        style={'textAlign': 'center','color': '#151282','fontFamily': 'sans-serif','paddingLeft': '0'}
    ),
     dcc.Dropdown(#Selecionar tipo ventana.
         id='Enventanado',
        options=[
            {'label': 'Rectangular', 'value': 'REC'},
            {'label': 'Blackman', 'value': 'BLK'},
            {'label': 'Hamming', 'value': 'HAM'},
            {'label': 'Hanning', 'value': 'HAN'}
            
        ],
        value='REC',
        placeholder="Seleccionar ventana"
        )   
    ],style={'width': '40%', 'display': 'inline-block','margin-left':'80px','margin-right':'20px'}
    ),
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
    ],style={'width': '40%', 'display': 'inline-block','margin-left':'20px','margin-right':'20px'}
    ),
    html.Div(id='sugerencia',style={'display':'inline-block'}),
    html.Div(id='sugerencia2',style={'display':'inline-block','margin-left':'20px'}),
    html.H2(children='Parametros del filtro',
        style={'textAlign': 'center','color': '#151282','fontFamily': 'sans-serif','paddingLeft': '0'}
    ),
    html.Div([# Seleccionar parametros
        html.Button(id='submit-button2', n_clicks=0, children='Graficar filtro')
    ],style={'text-align': 'center'}),        
    html.Div([    
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
                        dcc.Input(id='F1', value=500, type="number"),
                    ],style={ 'display': 'inline-block','margin-left':'20px'}),
                  
                  html.Div([
                        html.H4(children='Frecuencia de corte 2',
                            style={'textAlign': 'center','color': '#151282','fontFamily': 'sans-serif','paddingLeft': '0'}
                        ),
                        dcc.Input(id='F2', value=3500, type="number"),
                  ],style={ 'display': 'inline-block','margin-left':'20px'}),
                  
                  html.Div([
                      html.H4(children='Ganancia',
                            style={'textAlign': 'center','color': '#151282','fontFamily': 'sans-serif','paddingLeft': '0'}
                        ),
                      dcc.Input(id='Ganancia', value=0, type="number")
                      ],style={'align':'center','display': 'inline-block','margin-left':'20px'}),
                  html.Div([
                      html.H4(children='Frecuencia de muestreo',
                            style={'textAlign': 'center','color': '#151282','fontFamily': 'sans-serif','paddingLeft': '0'}
                        ),
                      dcc.Input(id='FS', value=16000, type="number")
                      ],style={'align':'center','display': 'inline-block','margin-left':'20px'}),
                  html.Div([
                      html.H4(children='Ripple',
                            style={'textAlign': 'center','color': '#151282','fontFamily': 'sans-serif','paddingLeft': '0'}
                        ),
                      dcc.Input(id='ripple', value=0.003, type="number")
                      ],style={'align':'center','display': 'inline-block','margin-left':'20px'})
                  
              ],style={'text-align': 'center'}),
    html.Div(id='Grafica-filtro'),# Grafica del filtro
    html.Div([
        html.Button(id='submit-button3', n_clicks=0, children='Filtrar')    
    ],style={'text-align': 'center'}),        
    html.Div(id='Grafica-audio_filtro'),#Grafica Audio filtrado
    html.Div(id='ventanasec'),
    html.Div([
        html.Button(id='escuchar2', n_clicks=0, children='Escuchar audio filtrado')    
    ],style={'text-align': 'center'})
    
],style={'backgroundColor':'white','margin-left' : '80px','margin-right' : '80px','margin-bottom':'100px'})

'''############################################# FUNCIONES ################################################################'''

#TEXTO CONFIRMACION AUDIO
@app.callback(Output('output-state', 'children'),
              [Input('submit-button', 'n_clicks')],
              [State('input-1-state', 'value')
               ])
def update_output(n_clicks, input1):
    return u'''Audio: "{}"'''.format(input1)

#ESCUHAR AUDIO ORIGINAL
@app.callback(Output('hide1', 'children'),
              [Input('escuchar1', 'n_clicks')],
              [State('input-1-state', 'value')
               ])
def update_output(n_clicks,name_audio):
    winsound.PlaySound(name_audio, winsound.SND_FILENAME)
    return '''Audio: '''
#Sugerencia ventana
@app.callback(Output('sugerencia', 'children'),
              [Input('Enventanado','value'),Input('ripple', 'value')],
             )
def update_ripple(ventana,rip):
    rip=float(rip)
    if 20*np.log10(rip) >= -21:
        return '''Ventanas sugeridas: Rectangular, Hann, Hamming, Blackman.'''
    elif 20*np.log10(rip) >= -44:
        return '''Ventanas sugeridas: Hann, Hamming, Blackman.'''
    elif 20*np.log10(rip) >= -53:
        return '''Ventanas sugeridas: Hamming, Blackman.'''
    else:
        return '''Ventanas sugeridas: Blackman. "{}"'''.format(rip)
#Sugerencia frecuencia de muestreo
@app.callback(Output('sugerencia2', 'children'),
              [Input('Tipo-filtro','value'),               
              Input('F1','value'),
              Input('F2','value'),
              Input('FS','value')]
             )
def update_muestreo(tf,f1,f2,fs):
    if tf == 'PBN':
        if 2.2*float(f2) > fs:
            return '''  Frecuencia de muestreo no cumple 2.2*{} < {} '''.format(f2,fs)
        else:
            return ''''''
    else:
        if 2.2*float(f1) > fs:
            return '''  Frecuencia de muestreo no cumple 2.2*{} < {} '''.format(f1,fs)

#GRAFICA AUDIO
@app.callback(
    dash.dependencies.Output('Grafica-audio','figure'),
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
#Caputura tipo de ventana

#PARAMETROS PARA FILTRO
@app.callback(Output('Grafica-filtro', 'children'),
              [Input('submit-button2','n_clicks')],
              [State('BT', 'value'),
              State('F1','value'),
              State('Ganancia','value'),
              State('FS','value'),
              State('F2','value'),
              State('Enventanado','value'),
              State('Tipo-filtro','value')])

def update_grafica_filtro(nc,bt,f1,ganancia,fs,f2,tv,tf):
    
    x,y,y1,h2 = diseño_filtro(bt,f1,f2,ganancia,fs,tf,tv)
    
    global h_filtro
    h_filtro = h2
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
                        {'x': x, 'y': y1, 'type': 'line', 'name': 'FILTRO frecuencia'},                               
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
@app.callback(Output('Grafica-audio_filtro', 'children'),
              [Input('submit-button3','n_clicks')])

def update_audio_filtro(value):
    audio_filtrado = np.convolve(señal_audio,h_filtro,mode = 'full')
    write('Filtrado.wav',int(fs_audio),audio_filtrado)
    
    return html.Div([
        dcc.Graph(
            id ='Audio_filtrado',
            figure = {
                'data':[
                        {'x': t_audio, 'y':audio_filtrado, 'type': 'line', 'name': 'FILTRO frecuencia'},                             
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
@app.callback(Output('hide2', 'children'),
              [Input('escuchar2', 'n_clicks')],
              [State('input-1-state', 'value')
               ])
def update_output(n_clicks,name_audio):
    os.system("start file:///C:/Users/Orion/Google%20Drive/UNIVERSIDAD/PDS/Final/Filtrado.wav")
    return u'''Audio: '''

if __name__ == '__main__':
    app.run_server(debug=True)