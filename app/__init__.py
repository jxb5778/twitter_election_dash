import dash

app = dash.Dash(
    name='Twitter Election Integrity',
    external_stylesheets=['https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css'],
    external_scripts=['https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js']
)

from app import index
