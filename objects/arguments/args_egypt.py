import objects.arguments.met_brewer as mb

colour = mb.Egypt

# COLOURS - 1208/1209
args_1208 = {'color': colour[0], 'label': "1208", 'marker': '+'}
fill_1208 = {'facecolor': colour[0], 'alpha': 0.1, 'label': r'$\pm 1\sigma$'}
args_1209 = {'color': colour[1], 'label': "1209", 'marker': '+'}
fill_1209 = {'facecolor': colour[1], 'alpha': 0.1, 'label': r'$\pm 1\sigma$'}

# COLOURS - FILL
args_diff = {'color': colour[2], 'label': "(1208 - 1209)"}
args_filt = {'color': 'k', 'label': "Rolling mean (30 ka)"}
fill_diff = {'facecolor': 'k', 'alpha': 0.1}

# COLOURS - 607/1313
args_607 = {'color': colour[3], 'label': "607", 'marker': '+'}
fill_607 = {'facecolor': colour[3], 'alpha': 0.1, 'label': r'$\pm 1\sigma$'}

# COLOURS - 849
args_849 = {'color': colour[3], 'label': "849", 'marker': '+'}
