cytoscape_stylesheet = [
    {
        'selector': 'node',
        'style': {
            'label': 'data(jersey_number)',
            'font-family' : 'JERSEY_NUMBER_FONT',
            'font-size': "data(number_size)",
            'text-valign': 'center',
            'text-halign': 'center',
            'text-margin-y' : 'mapData(number_size, 42, 182, 5, 15)',
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
            'width': 5,
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
            'width': 5,
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
            'font-size' : '30px',
            'line-opacity' : "0",
            'z-index' : 100,
            'loop-direction' : '-180deg',
            'loop-sweep' : '0deg',
            "control-point-step-size": 'data(edge_distance)',
            # "text-halign": "center",
            # "text-valign": "top",
            # "text-margin-y": "data(node_size)",  # Dynamically move label down
            'text-border-color': 'white',  # Border color for the text
            'text-border-width': '2px',  # Border width around the text

        }
    },
    
    {"selector": 'node[team=1610612737]', "style": {"background-color": "#C8102E"}},  # ATL
    {"selector": 'node[team=1610612738]', "style": {"background-color": "#007A33"}},  # BOS
    {"selector": 'node[team=1610612739]', "style": {"background-color": "#860038"}},  # CLE
    {"selector": 'node[team=1610612740]', "style": {"background-color": "#0C2340"}},  # NOP
    {"selector": 'node[team=1610612741]', "style": {"background-color": "#CE1141"}},  # CHI
    {"selector": 'node[team=1610612742]', "style": {"background-color": "#00538C"}},  # DAL
    {"selector": 'node[team=1610612743]', "style": {"background-color": "#0E2240"}},  # DEN
    {"selector": 'node[team=1610612744]', "style": {"background-color": "#1D428A"}},  # GSW
    {"selector": 'node[team=1610612745]', "style": {"background-color": "#CE1141"}},  # HOU
    {"selector": 'node[team=1610612746]', "style": {"background-color": "#1d428a"}},  # LAC
    {"selector": 'node[team=1610612747]', "style": {"background-color": "#FDB927"}},  # LAL
    {"selector": 'node[team=1610612748]', "style": {"background-color": "#98002E"}},  # MIA
    {"selector": 'node[team=1610612749]', "style": {"background-color": "#00471B"}},  # MIL
    {"selector": 'node[team=1610612750]', "style": {"background-color": "#0C2340"}},  # MIN
    {"selector": 'node[team=1610612751]', "style": {"background-color": "#000000"}},  # BKN
    {"selector": 'node[team=1610612752]', "style": {"background-color": "#006BB6"}},  # NYK
    {"selector": 'node[team=1610612753]', "style": {"background-color": "#0077c0"}},  # ORL
    {"selector": 'node[team=1610612754]', "style": {"background-color": "#FDBB30"}},  # IND
    {"selector": 'node[team=1610612755]', "style": {"background-color": "#006bb6"}},  # PHI
    {"selector": 'node[team=1610612756]', "style": {"background-color": "#1d1160"}},  # PHX
    {"selector": 'node[team=1610612757]', "style": {"background-color": "#E03A3E"}},  # POR
    {"selector": 'node[team=1610612758]', "style": {"background-color": "#5a2d81"}},  # SAC
    {"selector": 'node[team=1610612759]', "style": {"background-color": "#c4ced4"}},  # SAS
    {"selector": 'node[team=1610612760]', "style": {"background-color": "#007ac1"}},  # OKC
    {"selector": 'node[team=1610612761]', "style": {"background-color": "#ce1141"}},  # TOR
    {"selector": 'node[team=1610612762]', "style": {"background-color": "#002B5C"}},  # UTA
    {"selector": 'node[team=1610612763]', "style": {"background-color": "#5D76A9"}},  # MEM
    {"selector": 'node[team=1610612764]', "style": {"background-color": "#002B5C"}},  # WAS
    {"selector": 'node[team=1610612765]', "style": {"background-color": "#1d42ba"}},  # DET
    {"selector": 'node[team=1610612766]', "style": {"background-color": "#1d1160"}},  # CHA
    
]
