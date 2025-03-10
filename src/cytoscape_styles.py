cytoscape_stylesheet = [
    # {
    #     'selector': 'core',
    #     'style': {
    #         'background-color': '#F4A460',  # Basketball court wood color
    #         'background-image': 'url("/assets/court_lines_transparent.png")',  # Transparent PNG
    #         'background-fit': 'contain',  # Ensures the whole court is visible
    #         'background-repeat': 'no-repeat',
    #         'background-position': 'center center'
    #     }
    # },
    
    {
        'selector': 'node',
        'style': {
            'label': 'data(jersey_number)',
            'font-family' : 'JERSEY_NUMBER_FONT',
            'font-size': "data(number_size)",
            'text-valign': 'center',
            'text-halign': 'center',
            'text-margin-y' : 'mapData(number_size, 42, 182, 5, 15)',
            'text-outline-color': 'white',   # Outline color
            'text-outline-width': 3,         # Outline width
            'text-outline-opacity': 1,       # Outline opacity
            'width': 'data(node_size)',
            'height': 'data(node_size)',
            # 'width': 100,
            # 'height': 100,
            'grabbable' : False,
            "border-color" : "#050505",
            "border-width" : 2,
            "background-color" : "white",
            "shape": 'polygon',
            'shape-polygon-points': '-0.3 -1, -0.3 -0.85, 0 -0.7, 0.3 -0.85, 0.3 -1, 0.5 -1, 0.8 -0.4, 0.8 1, -0.8 1, -0.8 -0.4, -0.5 -1'

        }
    },
    
    {
        "selector" : "edge[offense = 'False']"  ,
        'style': {
            'width': 8,
            'line-color': '#red',
            'line-style' : 'dashed',
            'curve-style': 'bezier',
            'source-arrow-color': 'red',
            'source-arrow-shape': 'triangle',
        }
    },
    
    {
        "selector" : "edge[offense = 'True']"  ,
        'style': {
            'width': 8,
            'line-color': '#006400',
            'curve-style': 'bezier',
            'source-arrow-color': '#006400',
            'source-arrow-shape': 'triangle',
        }
    },
    
    {
        "selector" : "edge[display_edge = 'True']" ,
        'style': {
            'label': 'data(display_name)',
            'font-family' : 'JERSEY_NUMBER_FONT',
            'font-size' : '45px',
            'line-opacity' : "0",
            'z-index' : 100,
            'loop-direction' : '-180deg',
            'loop-sweep' : '0deg',
            "control-point-step-size": 'data(edge_distance)',
            'text-background-color': 'white',
            'text-background-opacity': 0.6,
            'text-background-shape': 'round-tag',
            'text-background-padding': 1,
            # "text-halign": "center",
            # "text-valign": "top",
            # "text-margin-y": "data(node_size)",  # Dynamically move label down
        }
    },
    
    # HOME COLORWAYS FOR JERSEYS
    {"selector": 'node[team=1610612737][home_away=1]', "style": {"background-color": "white", 'text-outline-color': '#FDB927', 'color' : '#C8102E'}},  # ATL
    {"selector": 'node[team=1610612738][home_away=1]', "style": {"background-color": "white", 'text-outline-color': '#007A33', 'color' : '#007A33'}},  # BOS
    {"selector": 'node[team=1610612739][home_away=1]', "style": {"background-color": "#white", 'text-outline-color': '#860038', 'color' : '#FDBB30'}},  # CLE
    {"selector": 'node[team=1610612740][home_away=1]', "style": {"background-color": "white", 'text-outline-color': '#85714D', 'color' : '#0C2340'}},  # NOP
    {"selector": 'node[team=1610612741][home_away=1]', "style": {"background-color": "white", 'text-outline-color': 'black', 'color' : '#CE1141'}},  # CHI
    {"selector": 'node[team=1610612742][home_away=1]', "style": {"background-color": "white", 'text-outline-color': '#B8C4CA', 'color' : '#00538C'}},  # DAL
    {"selector": 'node[team=1610612743][home_away=1]', "style": {"background-color": "white", 'text-outline-color': '#FEC524', 'color' : '#0E2240'}},  # DEN
    {"selector": 'node[team=1610612744][home_away=1]', "style": {"background-color": "white", 'text-outline-color': '#1D428A', 'color' : '#1D428A'}},  # GSW
    {"selector": 'node[team=1610612745][home_away=1]', "style": {"background-color": "white", 'text-outline-color': '#CE1141', 'color' : '#CE1141'}},  # HOU
    {"selector": 'node[team=1610612746][home_away=1]', "style": {"background-color": "white", 'text-outline-color': '#1d428a', 'color' : '#1d428a'}},  # LAC
    {"selector": 'node[team=1610612747][home_away=1]', "style": {"background-color": "white", 'text-outline-color': '#FDB927', 'color' : '#552583'}},  # LAL
    {"selector": 'node[team=1610612748][home_away=1]', "style": {"background-color": "white", 'text-outline-color': 'black', 'color' : '#98002E'}},  # MIA
    {"selector": 'node[team=1610612749][home_away=1]', "style": {"background-color": "white", 'text-outline-color': '#EEE1C6', 'color' : '#00471B'}},  # MIL
    {"selector": 'node[team=1610612750][home_away=1]', "style": {"background-color": "white", 'text-outline-color': 'black', 'color' : '#236192'}},  # MIN
    {"selector": 'node[team=1610612751][home_away=1]', "style": {"background-color": "white", 'text-outline-color': 'black', 'color' : 'black'}},  # BKN
    {"selector": 'node[team=1610612752][home_away=1]', "style": {"background-color": "white", 'text-outline-color': '#006BB6', 'color' : '#F58426'}},  # NYK
    {"selector": 'node[team=1610612753][home_away=1]', "style": {"background-color": "white", 'text-outline-color': 'black', 'color' : '#0077c0'}},  # ORL
    {"selector": 'node[team=1610612754][home_away=1]', "style": {"background-color": "white", 'text-outline-color': '#FDBB30', 'color' : '#002D62'}},  # IND
    {"selector": 'node[team=1610612755][home_away=1]', "style": {"background-color": "white", 'text-outline-color': '#ed174c', 'color' : '#006bb6'}},  # PHI
    {"selector": 'node[team=1610612756][home_away=1]', "style": {"background-color": "white", 'text-outline-color': '#e56020', 'color' : '#1d1160'}},  # PHX
    {"selector": 'node[team=1610612757][home_away=1]', "style": {"background-color": "white", 'text-outline-color': '#E03A3E', 'color' : 'black'}},  # POR
    {"selector": 'node[team=1610612758][home_away=1]', "style": {"background-color": "white", 'text-outline-color': '#5a2d81', 'color' : 'black'}},  # SAC
    {"selector": 'node[team=1610612759][home_away=1]', "style": {"background-color": "#c4ced4", 'text-outline-color': 'black', 'color' : 'black'}},  # SAS
    {"selector": 'node[team=1610612760][home_away=1]', "style": {"background-color": "white", 'text-outline-color': '#ef3b24', 'color' : '#007ac1'}},  # OKC
    {"selector": 'node[team=1610612761][home_away=1]', "style": {"background-color": "white", 'text-outline-color': 'black', 'color' : '#ce1141'}},  # TOR
    {"selector": 'node[team=1610612762][home_away=1]', "style": {"background-color": "white", 'text-outline-color': '#F9A01B', 'color' : '#002B5C'}},  # UTA
    {"selector": 'node[team=1610612763][home_away=1]', "style": {"background-color": "white", 'text-outline-color': '#5D76A9', 'color' : '#12173F'}},  # MEM
    {"selector": 'node[team=1610612764][home_away=1]', "style": {"background-color": "white", 'text-outline-color': 'white', 'color' : '#e31837'}},  # WAS
    {"selector": 'node[team=1610612765][home_away=1]', "style": {"background-color": "white", 'text-outline-color': '#1d42ba', 'color' : '#C8102E'}},  # DET
    {"selector": 'node[team=1610612766][home_away=1]', "style": {"background-color": "white", 'text-outline-color': '#1d1160', 'color' : '#00788C'}},  # CHA
    
    # AWAY COLORWAYS FOR JERSEYS
    {"selector": 'node[team=1610612737][home_away=0]', "style": {"background-color": "#C8102E", 'text-outline-color': 'FDB927', 'color' : 'white'}},  # ATL
    {"selector": 'node[team=1610612738][home_away=0]', "style": {"background-color": "#007A33", 'text-outline-color': 'white', 'color' : 'white'}},  # BOS
    {"selector": 'node[team=1610612739][home_away=0]', "style": {"background-color": "#860038", 'text-outline-color': 'FDBB30', 'color' : '#FDBB30'}},  # CLE
    {"selector": 'node[team=1610612740][home_away=0]', "style": {"background-color": "#0C2340", 'text-outline-color': '#85714D', 'color' : '#0C2340'}},  # NOP
    {"selector": 'node[team=1610612741][home_away=0]', "style": {"background-color": "#CE1141", 'text-outline-color': 'white', 'color' : 'black'}},  # CHI
    {"selector": 'node[team=1610612742][home_away=0]', "style": {"background-color": "#002B5e", 'text-outline-color': 'white', 'color' : 'white'}},  # DAL
    {"selector": 'node[team=1610612743][home_away=0]', "style": {"background-color": "#0E2240", 'text-outline-color': '#FEC524', 'color' : 'white'}},  # DEN
    {"selector": 'node[team=1610612744][home_away=0]', "style": {"background-color": "#1D428A", 'text-outline-color': '#ffc72c', 'color' : '#ffc72c'}},  # GSW
    {"selector": 'node[team=1610612745][home_away=0]', "style": {"background-color": "#CE1141", 'text-outline-color': 'black', 'white' : 'white'}},  # HOU
    {"selector": 'node[team=1610612746][home_away=0]', "style": {"background-color": "#1d428a", 'text-outline-color': 'white', 'color' : 'white'}},  # LAC
    {"selector": 'node[team=1610612747][home_away=0]', "style": {"background-color": "#FDB927", 'text-outline-color': 'white', 'color' : '#552583'}},  # LAL
    {"selector": 'node[team=1610612748][home_away=0]', "style": {"background-color": "black", 'text-outline-color': '#98002E', 'color' : 'white'}},  # MIA
    {"selector": 'node[team=1610612749][home_away=0]', "style": {"background-color": "#00471B", 'text-outline-color': '#EEE1C6', 'color' : 'white'}},  # MIL
    {"selector": 'node[team=1610612750][home_away=0]', "style": {"background-color": "#0C2340", 'text-outline-color': '#236192', 'color' : 'white'}},  # MIN
    {"selector": 'node[team=1610612751][home_away=0]', "style": {"background-color": "#000000", 'text-outline-color': 'white', 'color' : 'white'}},  # BKN
    {"selector": 'node[team=1610612752][home_away=0]', "style": {"background-color": "#006BB6", 'text-outline-color': 'white', 'color' : '#F58426'}},  # NYK
    {"selector": 'node[team=1610612753][home_away=0]', "style": {"background-color": "black", 'text-outline-color': '#0077c0', 'color' : 'white'}},  # ORL
    {"selector": 'node[team=1610612754][home_away=0]', "style": {"background-color": "#002D62", 'text-outline-color': 'white', 'color' : '#FDBB30'}},  # IND
    {"selector": 'node[team=1610612755][home_away=0]', "style": {"background-color": "#006bb6", 'text-outline-color': '#ed174c', 'color' : 'white'}},  # PHI
    {"selector": 'node[team=1610612756][home_away=0]', "style": {"background-color": "#1d1160", 'text-outline-color': '#e56020', 'color' : 'white'}},  # PHX
    {"selector": 'node[team=1610612757][home_away=0]', "style": {"background-color": "black", 'text-outline-color': '#E03A3E', 'color' : 'white'}},  # POR
    {"selector": 'node[team=1610612758][home_away=0]', "style": {"background-color": "black", 'text-outline-color': '#5a2d81', 'color' : 'white'}},  # SAC
    {"selector": 'node[team=1610612759][home_away=0]', "style": {"background-color": "black", 'text-outline-color': '#c4ced4', 'color' : 'white'}},  # SAS
    {"selector": 'node[team=1610612760][home_away=0]', "style": {"background-color": "#007ac1", 'text-outline-color': '#ef3b24', 'color' : 'white'}},  # OKC
    {"selector": 'node[team=1610612761][home_away=0]', "style": {"background-color": "#ce1141", 'text-outline-color': 'white', 'color' : 'black'}},  # TOR
    {"selector": 'node[team=1610612762][home_away=0]', "style": {"background-color": "black", 'text-outline-color': '#F9A01B', 'color' : '#F9A01B'}},  # UTA
    {"selector": 'node[team=1610612763][home_away=0]', "style": {"background-color": "#12173F", 'text-outline-color': '#5D76A9', 'color' : '#5D76A9'}},  # MEM
    {"selector": 'node[team=1610612764][home_away=0]', "style": {"background-color": "#e31837", 'text-outline-color': 'white', 'color' : '#002B5C'}},  # WAS
    {"selector": 'node[team=1610612765][home_away=0]', "style": {"background-color": "#1d42ba", 'text-outline-color': 'white', 'color' : '#C8102E'}},  # DET
    {"selector": 'node[team=1610612766][home_away=0]', "style": {"background-color": "#00788C", 'text-outline-color': '#1d1160', 'color' : 'white'}},  # CHA
    
]

# node_selected_stylesheet = [
#     {
#         'selector': 'node',
#         'style': {
#             'label': 'data(jersey_number)',
#             'font-family' : 'JERSEY_NUMBER_FONT',
#             'font-size': "data(number_size)",
#             'text-valign': 'center',
#             'text-halign': 'center',
#             'text-margin-y' : 'mapData(number_size, 42, 182, 5, 15)',
#             'width': 'data(node_size)',
#             'height': 'data(node_size)',
#             # 'width': 100,
#             # 'height': 100,
#             'grabbable' : False,
#             "border-color" : "#050505",
#             "border-width" : 2,
#             "background-color" : "white",
#             "shape": 'polygon',
#             'opacity' : 0.2,
#             'shape-polygon-points': '-0.3 -1, -0.3 -0.85, 0 -0.7, 0.3 -0.85, 0.3 -1, 0.5 -1, 0.8 -0.4, 0.8 1, -0.8 1, -0.8 -0.4, -0.5 -1'

#         }
#     },
    
#     {
#         "selector" : 'edge[display_edge = "True"]' ,
#         'style': {
#             'label': 'data(display_name)',
#             'font-family' : 'JERSEY_NUMBER_FONT',
#             'font-size' : '30px',
#             'line-opacity' : "0",
#             'z-index' : 100,
#             'loop-direction' : '-180deg',
#             'loop-sweep' : '0deg',
#             "control-point-step-size": 'data(edge_distance)',
#             "text-opacity" : 0.2,
#             # "text-halign": "center",
#             # "text-valign": "top",
#             # "text-margin-y": "data(node_size)",  # Dynamically move label down
#             'text-border-color': 'white',  # Border color for the text
#             'text-border-width': '2px',  # Border width around the text

#         }
#     },
    
#     {
#         "selector": "edge",
#         "style": {
#             "line-opacity": 0,
#             "curve-style": "bezier",
#         },
#     },
# ]
 
team_colors_styles = [   
    # HOME COLORWAYS FOR JERSEYS
    {"selector": 'node[team=1610612737][home_away=1]', "style": {"background-color": "white", 'text-outline-color': '#FDB927', 'color' : '#C8102E'}},  # ATL
    {"selector": 'node[team=1610612738][home_away=1]', "style": {"background-color": "white", 'text-outline-color': '#007A33', 'color' : '#007A33'}},  # BOS
    {"selector": 'node[team=1610612739][home_away=1]', "style": {"background-color": "#white", 'text-outline-color': '#860038', 'color' : '#FDBB30'}},  # CLE
    {"selector": 'node[team=1610612740][home_away=1]', "style": {"background-color": "white", 'text-outline-color': '#85714D', 'color' : '#0C2340'}},  # NOP
    {"selector": 'node[team=1610612741][home_away=1]', "style": {"background-color": "white", 'text-outline-color': 'black', 'color' : '#CE1141'}},  # CHI
    {"selector": 'node[team=1610612742][home_away=1]', "style": {"background-color": "white", 'text-outline-color': '#B8C4CA', 'color' : '#00538C'}},  # DAL
    {"selector": 'node[team=1610612743][home_away=1]', "style": {"background-color": "white", 'text-outline-color': '#FEC524', 'color' : '#0E2240'}},  # DEN
    {"selector": 'node[team=1610612744][home_away=1]', "style": {"background-color": "white", 'text-outline-color': '#1D428A', 'color' : '#1D428A'}},  # GSW
    {"selector": 'node[team=1610612745][home_away=1]', "style": {"background-color": "white", 'text-outline-color': '#CE1141', 'color' : '#CE1141'}},  # HOU
    {"selector": 'node[team=1610612746][home_away=1]', "style": {"background-color": "white", 'text-outline-color': '#1d428a', 'color' : '#1d428a'}},  # LAC
    {"selector": 'node[team=1610612747][home_away=1]', "style": {"background-color": "white", 'text-outline-color': '#FDB927', 'color' : '#552583'}},  # LAL
    {"selector": 'node[team=1610612748][home_away=1]', "style": {"background-color": "white", 'text-outline-color': 'black', 'color' : '#98002E'}},  # MIA
    {"selector": 'node[team=1610612749][home_away=1]', "style": {"background-color": "white", 'text-outline-color': '#EEE1C6', 'color' : '#00471B'}},  # MIL
    {"selector": 'node[team=1610612750][home_away=1]', "style": {"background-color": "white", 'text-outline-color': 'black', 'color' : '#236192'}},  # MIN
    {"selector": 'node[team=1610612751][home_away=1]', "style": {"background-color": "white", 'text-outline-color': 'black', 'color' : 'black'}},  # BKN
    {"selector": 'node[team=1610612752][home_away=1]', "style": {"background-color": "white", 'text-outline-color': '#006BB6', 'color' : '#F58426'}},  # NYK
    {"selector": 'node[team=1610612753][home_away=1]', "style": {"background-color": "white", 'text-outline-color': 'black', 'color' : '#0077c0'}},  # ORL
    {"selector": 'node[team=1610612754][home_away=1]', "style": {"background-color": "white", 'text-outline-color': '#FDBB30', 'color' : '#002D62'}},  # IND
    {"selector": 'node[team=1610612755][home_away=1]', "style": {"background-color": "white", 'text-outline-color': '#ed174c', 'color' : '#006bb6'}},  # PHI
    {"selector": 'node[team=1610612756][home_away=1]', "style": {"background-color": "white", 'text-outline-color': '#e56020', 'color' : '#1d1160'}},  # PHX
    {"selector": 'node[team=1610612757][home_away=1]', "style": {"background-color": "white", 'text-outline-color': '#E03A3E', 'color' : 'black'}},  # POR
    {"selector": 'node[team=1610612758][home_away=1]', "style": {"background-color": "white", 'text-outline-color': '#5a2d81', 'color' : 'black'}},  # SAC
    {"selector": 'node[team=1610612759][home_away=1]', "style": {"background-color": "#c4ced4", 'text-outline-color': 'black', 'color' : 'black'}},  # SAS
    {"selector": 'node[team=1610612760][home_away=1]', "style": {"background-color": "white", 'text-outline-color': '#ef3b24', 'color' : '#007ac1'}},  # OKC
    {"selector": 'node[team=1610612761][home_away=1]', "style": {"background-color": "white", 'text-outline-color': 'black', 'color' : '#ce1141'}},  # TOR
    {"selector": 'node[team=1610612762][home_away=1]', "style": {"background-color": "white", 'text-outline-color': '#F9A01B', 'color' : '#002B5C'}},  # UTA
    {"selector": 'node[team=1610612763][home_away=1]', "style": {"background-color": "white", 'text-outline-color': '#5D76A9', 'color' : '#12173F'}},  # MEM
    {"selector": 'node[team=1610612764][home_away=1]', "style": {"background-color": "white", 'text-outline-color': 'white', 'color' : '#e31837'}},  # WAS
    {"selector": 'node[team=1610612765][home_away=1]', "style": {"background-color": "white", 'text-outline-color': '#1d42ba', 'color' : '#C8102E'}},  # DET
    {"selector": 'node[team=1610612766][home_away=1]', "style": {"background-color": "white", 'text-outline-color': '#1d1160', 'color' : '#00788C'}},  # CHA
    
    # AWAY COLORWAYS FOR JERSEYS
    {"selector": 'node[team=1610612737][home_away=0]', "style": {"background-color": "#C8102E", 'text-outline-color': 'FDB927', 'color' : 'white'}},  # ATL
    {"selector": 'node[team=1610612738][home_away=0]', "style": {"background-color": "#007A33", 'text-outline-color': 'white', 'color' : 'white'}},  # BOS
    {"selector": 'node[team=1610612739][home_away=0]', "style": {"background-color": "#860038", 'text-outline-color': 'FDBB30', 'color' : '#FDBB30'}},  # CLE
    {"selector": 'node[team=1610612740][home_away=0]', "style": {"background-color": "#0C2340", 'text-outline-color': '#85714D', 'color' : '#0C2340'}},  # NOP
    {"selector": 'node[team=1610612741][home_away=0]', "style": {"background-color": "#CE1141", 'text-outline-color': 'white', 'color' : 'black'}},  # CHI
    {"selector": 'node[team=1610612742][home_away=0]', "style": {"background-color": "#002B5e", 'text-outline-color': 'white', 'color' : 'white'}},  # DAL
    {"selector": 'node[team=1610612743][home_away=0]', "style": {"background-color": "#0E2240", 'text-outline-color': '#FEC524', 'color' : 'white'}},  # DEN
    {"selector": 'node[team=1610612744][home_away=0]', "style": {"background-color": "#1D428A", 'text-outline-color': '#ffc72c', 'color' : '#ffc72c'}},  # GSW
    {"selector": 'node[team=1610612745][home_away=0]', "style": {"background-color": "#CE1141", 'text-outline-color': 'black', 'white' : 'white'}},  # HOU
    {"selector": 'node[team=1610612746][home_away=0]', "style": {"background-color": "#1d428a", 'text-outline-color': 'white', 'color' : 'white'}},  # LAC
    {"selector": 'node[team=1610612747][home_away=0]', "style": {"background-color": "#FDB927", 'text-outline-color': 'white', 'color' : '#552583'}},  # LAL
    {"selector": 'node[team=1610612748][home_away=0]', "style": {"background-color": "black", 'text-outline-color': '#98002E', 'color' : 'white'}},  # MIA
    {"selector": 'node[team=1610612749][home_away=0]', "style": {"background-color": "#00471B", 'text-outline-color': '#EEE1C6', 'color' : 'white'}},  # MIL
    {"selector": 'node[team=1610612750][home_away=0]', "style": {"background-color": "#0C2340", 'text-outline-color': '#236192', 'color' : 'white'}},  # MIN
    {"selector": 'node[team=1610612751][home_away=0]', "style": {"background-color": "#000000", 'text-outline-color': 'white', 'color' : 'white'}},  # BKN
    {"selector": 'node[team=1610612752][home_away=0]', "style": {"background-color": "#006BB6", 'text-outline-color': 'white', 'color' : '#F58426'}},  # NYK
    {"selector": 'node[team=1610612753][home_away=0]', "style": {"background-color": "black", 'text-outline-color': '#0077c0', 'color' : 'white'}},  # ORL
    {"selector": 'node[team=1610612754][home_away=0]', "style": {"background-color": "#002D62", 'text-outline-color': 'white', 'color' : '#FDBB30'}},  # IND
    {"selector": 'node[team=1610612755][home_away=0]', "style": {"background-color": "#006bb6", 'text-outline-color': '#ed174c', 'color' : 'white'}},  # PHI
    {"selector": 'node[team=1610612756][home_away=0]', "style": {"background-color": "#1d1160", 'text-outline-color': '#e56020', 'color' : 'white'}},  # PHX
    {"selector": 'node[team=1610612757][home_away=0]', "style": {"background-color": "black", 'text-outline-color': '#E03A3E', 'color' : 'white'}},  # POR
    {"selector": 'node[team=1610612758][home_away=0]', "style": {"background-color": "black", 'text-outline-color': '#5a2d81', 'color' : 'white'}},  # SAC
    {"selector": 'node[team=1610612758][home_away=0]', "style": {"background-color": "black", 'text-outline-color': '#5a2d81', 'color' : 'white'}},  # SAC
    {"selector": 'node[team=1610612760][home_away=0]', "style": {"background-color": "#007ac1", 'text-outline-color': '#ef3b24', 'color' : 'white'}},  # OKC
    {"selector": 'node[team=1610612761][home_away=0]', "style": {"background-color": "#ce1141", 'text-outline-color': 'white', 'color' : 'black'}},  # TOR
    {"selector": 'node[team=1610612762][home_away=0]', "style": {"background-color": "black", 'text-outline-color': '#F9A01B', 'color' : '#F9A01B'}},  # UTA
    {"selector": 'node[team=1610612763][home_away=0]', "style": {"background-color": "#12173F", 'text-outline-color': '#5D76A9', 'color' : '#5D76A9'}},  # MEM
    {"selector": 'node[team=1610612764][home_away=0]', "style": {"background-color": "#e31837", 'text-outline-color': 'white', 'color' : '#002B5C'}},  # WAS
    {"selector": 'node[team=1610612765][home_away=0]', "style": {"background-color": "#1d42ba", 'text-outline-color': 'white', 'color' : '#C8102E'}},  # DET
    {"selector": 'node[team=1610612766][home_away=0]', "style": {"background-color": "#00788C", 'text-outline-color': '#1d1160', 'color' : 'white'}}  # CHA
]

scoreboard_colors = {
    "1610612737": "#C8102E",  # ATL
    "1610612738": "#007A33",  # BOS
    "1610612739": "#FDBB30",  # CLE
    "1610612740": "#0C2340",  # NOP
    "1610612741": "#CE1141",  # CHI
    "1610612742": "#00538C",  # DAL
    "1610612743": "#0E2240",  # DEN
    "1610612744": "#1D428A",  # GSW
    "1610612745": "#CE1141",  # HOU
    "1610612746": "#1D428A",  # LAC
    "1610612747": "#552583",  # LAL
    "1610612748": "#98002E",  # MIA
    "1610612749": "#00471B",  # MIL
    "1610612750": "#236192",  # MIN
    "1610612751": "black",    # BKN
    "1610612752": "#F58426",  # NYK
    "1610612753": "#0077C0",  # ORL
    "1610612754": "#002D62",  # IND
    "1610612755": "#006BB6",  # PHI
    "1610612756": "#1D1160",  # PHX
    "1610612757": "black",    # POR
    "1610612758": "black",    # SAC
    "1610612759": "black",    # SAS
    "1610612760": "#007AC1",  # OKC
    "1610612761": "#CE1141",  # TOR
    "1610612762": "#002B5C",  # UTA
    "1610612763": "#12173F",  # MEM
    "1610612764": "#E31837",  # WAS
    "1610612765": "#C8102E",  # DET
    "1610612766": "#00788C",  # CHA
}
