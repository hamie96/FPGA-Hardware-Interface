import dash
import dash_core_components as dcc
import dash_html_components as html
import time
from collections import deque
import plotly.graph_objs as go
import random
import requests
from json_with_dates import loads
from network_interface import *


import os, binascii, hashlib, base58

block_request = requests.get('https://blockexplorer.com/api/block/0000000000000000079c58e8b5bce4217f7515a74b170049398ed9b8428beb4a')
block = loads(block_request.text)
block1 = Block(block['hash'],block['version'],block['previousblockhash'],block['merkleroot'],block['time'],block['bits'], block['nonce'])


user1 = User('Default')
user1.createPrivateKey()
user1.createPublicKey(user1.getPrivateKey())
user1.createBitcoinAddress(user1.getPublicKey())

isMining = False
isMiningColor = '#f44336'

app = dash.Dash('Cryptocurrency-data')

app.config.suppress_callback_exceptions = True

max_length = 20

#set data to deques
times = deque(maxlen=max_length)
power_usage = deque(maxlen=max_length)
temperature = deque(maxlen=max_length)
core1_speed = deque(maxlen=max_length)
core2_speed = deque(maxlen=max_length)
core3_speed = deque(maxlen=max_length)
ram_usage = deque(maxlen=max_length)

#create a dictionary with matching data names
data_dict = {
"Power Usage":power_usage,
"Temperature": temperature,
"Core 1 Speed": core1_speed,
"Core 2 Speed":core2_speed,
"Core 3 Speed":core3_speed,
"RAM Usage":ram_usage
             }



#function to update the data
def update_obd_values(times, power_usage, temperature, core1_speed, core2_speed, core3_speed, ram_usage):

    #increase the time interval
    times.append(time.time())


#generate dummy data ////////////will be deleted soon////////////////THIS IS WHERE THE DATA WILL GO

    if len(times) == 1:
        #starting relevant values
        power_usage.append(random.randrange(180,230))
        temperature.append(random.randrange(95,115))
        core1_speed.append(random.randrange(170,220))
        core2_speed.append(random.randrange(1000,9500))
        core3_speed.append(random.randrange(30,140))
        ram_usage.append(random.randrange(10,90))
    else:
        for data_of_interest in [power_usage, temperature, core1_speed, core2_speed, core3_speed, ram_usage]:
            data_of_interest.append(data_of_interest[-1]+data_of_interest[-1]*random.uniform(-0.0001,0.0001))
#end generated dummy data /////////////// will delete soon /////////////THIS IS WHERE THE DATA WILL GO///////////////////////


    #return updated values
    return times, power_usage, temperature, core1_speed, core2_speed, core3_speed, ram_usage


#run the previous function and update the values to it
times, power_usage, temperature, core1_speed, core2_speed, core3_speed, ram_usage = update_obd_values(times, power_usage, temperature, core1_speed, core2_speed, core3_speed, ram_usage)

#setting up the actual html file

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])
#//////////////////////////INDEX PAGE//////////////////////////////////////////////////////////////////
index_page = html.Div([
    html.Div([
        html.H4('Enter Private Key Here:'),
        html.Div(dcc.Input(id='private-key-in', type='text')),
        html.H4('(Optional) Enter Block Explorer Hash Here:'),
        html.Div(dcc.Input(id='block-id-link', type='text')),
        dcc.Link(html.Button('Submit', id='submit', className="waves-effect waves-light btn"), href='/home', id='submitlink'),
        html.Button('Generate', id='generate', className="waves-effect waves-light btn"),
        html.Br(),
        html.Div(id='key-display-div', children='Enter your private key or press "Generate" to generate a new key and paste it in then press Submit.'),
        html.Div(id='key-result-div'),
        html.Div(id='submit-hidden-div', style={'display':'none'}) #DUMMY DIV FOR SUBMIT 1
    ])
])

#//////////////////////////////////////HOME PAGE////////////////////////////////////////////////////////////
home_page = html.Div([

    html.Div([
    html.Br(),
    html.Button('Mine!', id='minebutton',className="waves-effect waves-light btn", style={'background-color': isMiningColor }),
    html.Div(id='output-container-button',
             children='Click here to start mining!'),
    html.Br(),
    html.Div(id='blockhashtag', children = 'Block Hash: ' + block1.getBlockHash()),
    html.Div(id='blockversion', children = 'Version: ' +  str(block1.getVersion())),
    html.Div(id='previousblck', children = 'Previous Block Hash: ' + block1.getPrevBlockHash()),
    html.Div(id='merkleroot', children = 'Merkle Root: ' + block1.getMerkleRoot()),
    html.Div(id='blocktime', children = 'Time: ' + str(block1.getTime())),
    html.Div(id='bitstag', children = 'Bits: ' + block1.getBits()),
    html.Div(id='noncetag', children = 'Current Nonce: ' + str(block1.getNonce())),
    html.Div(id='balancetag', children = 'Current Balance: ' + str(user1.getBalance())),
    html.Div(id='submit-hidden-div2', style={'display':'none'}) #DUMMY DIV FOR SUBMIT 2
    ]),

    html.Div([
        html.H2('FPGA Bitcoin Miner Web Portal',
                style={'float': 'left',
                       }),
        ]),

    dcc.Dropdown(id='crypt-data-name',
                 options=[{'label': s, 'value': s}
                          for s in data_dict.keys()],
                 value=['Power Usage','Temperature','RAM Usage'],
                 multi=True
                 ),
    html.Div(children=html.Div(id='graphs'), className='row'),
    dcc.Interval(
        id='graph-update',
        interval=1000),


    ], className="container",style={'width':'98%','margin-left':20,'margin-right':20, 'height': '75%'})

#////////////////////////////////////////TEST BUTTON////////////////////////////////////////////////////////
@app.callback(
    dash.dependencies.Output('minebutton', 'style'),
    [dash.dependencies.Input('minebutton', 'n_clicks')])
def update_button(n_clicks):
    try:
        if int(n_clicks) > 0:
            global isMining
            global isMiningColor
            if isMining is False:
                isMiningColor = '#0091ea'
                isMining = True
            else:
                isMining = False
                isMiningColor = '#f44336'
            print("Mining Status: " + str(isMining))
    except:
        print('')
    return {'background-color': isMiningColor }

#///////////////////////////////////////SUBMIT PRIVATE KEY///////////////////////////////////////////////////
@app.callback([dash.dependencies.Output('submit-hidden-div', 'children'),
               dash.dependencies.Output('blockhashtag', 'children'),
               dash.dependencies.Output('blockversion', 'children'),
               dash.dependencies.Output('previousblck', 'children'),
               dash.dependencies.Output('merkleroot', 'children'),
               dash.dependencies.Output('blocktime', 'children'),
               dash.dependencies.Output('bitstag', 'children'),
               dash.dependencies.Output('noncetag', 'children'),
               dash.dependencies.Output('balancetag', 'children')],
              [dash.dependencies.Input('submit', 'n_clicks')],
              [dash.dependencies.State('private-key-in', 'value'), dash.dependencies.State('block-id-link', 'value')])
def submit_privatekey(n_clicks, pkin, blckid):

    global user1
    user1.setPrivateKey(pkin)
    print("Private Key Set!: " + user1.getPrivateKey())
    if blckid is not None:
          print(type(blckid))
          block_request = requests.get('https://blockexplorer.com/api/block/' + blckid)
          block = loads(block_request.text)
    else:
          block_request = requests.get('https://blockexplorer.com/api/block/0000000000000000079c58e8b5bce4217f7515a74b170049398ed9b8428beb4a')
          block = loads(block_request.text)
    global block1
    block1 = Block(block['hash'],block['version'],block['previousblockhash'],block['merkleroot'],block['time'],block['bits'], block['nonce'])
    
    print(block1.getFullhash())

    return "",'Block Hash: {}'.format(block1.getBlockHash()),'Version: {}'.format(block1.getVersion()),'Previous Block Hash: {}'.format(block1.getPrevBlockHash()),'Merkle Root: {}'.format(block1.getMerkleRoot()),'Time: {}'.format(block1.getTime()),'Bits: {}'.format(block1.getBits()),'Current Nonce: {}'.format(block1.getNonce()),'Current Balance: {}'.format(user1.getBalance())

#/////////////////////////////////////////GENERATE PRIVATE KEY///////////////////////////////////////////////////
@app.callback(
    dash.dependencies.Output('key-result-div', 'children'),
    [dash.dependencies.Input('generate', 'n_clicks')],
    [dash.dependencies.State('private-key-in', 'value')])
def update_button(n_clicks, value):
    global user1
    print("This button is working!")
    try:
#        WIF =''
        if int(n_clicks) > 0:
#            fullkey = "80" + binascii.hexlify(os.urandom(32)).decode()
#            sha256a = hashlib.sha256(binascii.unhexlify(fullkey)).hexdigest()
#            sha256b = hashlib.sha256(binascii.unhexlify(sha256a)).hexdigest()
#            WIF = base58.b58encode(binascii.unhexlify(fullkey + sha256b[:8]))
#            value = WIF
            user1.createPrivateKey()
            print(user1.returnUser())
            value = user1.getPrivateKey()
    except:
        print("Something went wrong D:")
    return 'Your key is {}'.format(user1.getPrivateKey())





#////////////////////////////////////////////UPDATE REALTIME GRAPHS////////////////////////////////////////////////a
#decorator for updating the graph
@app.callback(
    dash.dependencies.Output('graphs', 'children'),
    [dash.dependencies.Input('crypt-data-name', 'value'), dash.dependencies.Input('graph-update', 'n_intervals')]
    )
#function that updates the graph and formats it

def update_graph(data_names, n):
    #graphs list to hold graphs
    graphs = []

    #call the function once again to reupdate
    update_obd_values(times, power_usage, temperature, core1_speed, core2_speed, core3_speed, ram_usage)

    #setting the size of the graphs based on bootstrap screen size
    if len(data_names)>2:
        class_choice = 'col s12 m6 l4'
    elif len(data_names) == 2:
        class_choice = 'col s12 m6 l6'
    else:
        class_choice = 'col s12'

    #generate a graph for each piece of data
    for data_name in data_names:

        data = go.Scatter(
            x=list(times),
            y=list(data_dict[data_name]),
            name='Scatter',
            fill="tozeroy",
            fillcolor="#6897bb"
            )

        #add that graph to the graphs[]
        graphs.append(html.Div(dcc.Graph(
            id=data_name,
            animate=True,
            figure={'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(times),max(times)]),
                                                        yaxis=dict(range=[min(data_dict[data_name]),max(data_dict[data_name])]),
                                                        margin={'l':50,'r':1,'t':45,'b':1},
                                                        title='{}'.format(data_name))}
            ), className=class_choice))

    return graphs

#////////////////////////////////////////LINK TO NEW PAGE///////////////////////////////////////////////
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/home':
        return home_page
    else:
        return index_page

#external css and javascript
external_css = ["https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css"]
for css in external_css:
    app.css.append_css({"external_url": css})

external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']
for js in external_css:
    app.scripts.append_script({'external_url': js})


#run server on local host
def run_server(p):
    app.run_server(debug=True, host="0.0.0.0", port=p)
