import objects.met_brewer as mb

colour = mb.Lakota

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
args_1313 = {'color': colour[4], 'label': "1313", 'marker': '+'}
fill_1313 = {'facecolor': colour[4], 'alpha': 0.1, 'label': r'$\pm 1\sigma$'}

# COLOURS - 925/929
args_925 = {'color': colour[4], 'label': "925", 'marker': '+'}
fill_925 = {'facecolor': colour[4], 'alpha': 0.1, 'label': r'$\pm 1\sigma$'}
args_929 = {'color': colour[5], 'label': "929", 'marker': '+'}
fill_929 = {'facecolor': colour[5], 'alpha': 0.1, 'label': r'$\pm 1\sigma$'}