import dash
# Creacion de servidor
app = dash.Dash()
server = app.server
app.config.supress_callback_exceptions = True