from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np


x = np.linspace(-10, 10, 100)

f1 = 2*x + 3
f2 = -x + 5

fig = make_subplots()
fig.add_trace(go.Scatter(x=x, y=f1, mode='lines', name='f1(x) = 2x + 3'))
fig.add_trace(go.Scatter(x=x, y=f2, mode='lines', name='f2(x) = -x + 5'))
fig.update_layout(title='Gráfico de f1(x) e f2(x)', xaxis_title='x', yaxis_title='f(x)')
fig.update_xaxes(range=[-10, 10])
fig.update_yaxes(range=[-10, 10])
fig.update_xaxes(zeroline=True, zerolinewidth=2, zerolinecolor='LightPink')
fig.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor='LightPink')

fig.show()
