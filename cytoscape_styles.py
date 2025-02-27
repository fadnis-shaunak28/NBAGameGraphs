cytoscape_stylesheet = [
    {
        'selector': 'node',
        'style': {
            'label': 'data(label)',
            'text-valign': 'center',
            'text-halign': 'center',
            'width': 'data(node_size)',
            'height': 'data(node_size)',
            # 'width': 100,
            # 'height': 100,
            'grabbable' : False,
            "border-color" : "#050505",
            "border-width" : 2,
            "background-color" : "white",
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
    
    {"selector": 'node[team=1610612737]', "style": {"background-color": "#FF5733"}},  # ATL
    {"selector": 'node[team=1610612738]', "style": {"background-color": "#33FF57"}},  # BOS
    {"selector": 'node[team=1610612739]', "style": {"background-color": "#3357FF"}},  # CLE
    {"selector": 'node[team=1610612740]', "style": {"background-color": "#FF33A8"}},  # NOP
    {"selector": 'node[team=1610612741]', "style": {"background-color": "#A833FF"}},  # CHI
    {"selector": 'node[team=1610612742]', "style": {"background-color": "#33FFF0"}},  # DAL
    {"selector": 'node[team=1610612743]', "style": {"background-color": "#FF8C33"}},  # DEN
    {"selector": 'node[team=1610612744]', "style": {"background-color": "#8C33FF"}},  # GSW
    {"selector": 'node[team=1610612745]', "style": {"background-color": "#33FF8C"}},  # HOU
    {"selector": 'node[team=1610612746]', "style": {"background-color": "#FF3333"}},  # LAC
    {"selector": 'node[team=1610612747]', "style": {"background-color": "#3333FF"}},  # LAL
    {"selector": 'node[team=1610612748]', "style": {"background-color": "#F0FF33"}},  # MIA
    {"selector": 'node[team=1610612749]', "style": {"background-color": "#FF33F0"}},  # MIL
    {"selector": 'node[team=1610612750]', "style": {"background-color": "#33A8FF"}},  # MIN
    {"selector": 'node[team=1610612751]', "style": {"background-color": "#A8FF33"}},  # BKN
    {"selector": 'node[team=1610612752]', "style": {"background-color": "#FF5733"}},  # NYK
    {"selector": 'node[team=1610612753]', "style": {"background-color": "#33FF57"}},  # ORL
    {"selector": 'node[team=1610612754]', "style": {"background-color": "#3357FF"}},  # IND
    {"selector": 'node[team=1610612755]', "style": {"background-color": "#FF33A8"}},  # PHI
    {"selector": 'node[team=1610612756]', "style": {"background-color": "#A833FF"}},  # PHX
    {"selector": 'node[team=1610612757]', "style": {"background-color": "#33FFF0"}},  # POR
    {"selector": 'node[team=1610612758]', "style": {"background-color": "#FF8C33"}},  # SAC
    {"selector": 'node[team=1610612759]', "style": {"background-color": "#8C33FF"}},  # SAS
    {"selector": 'node[team=1610612760]', "style": {"background-color": "#33FF8C"}},  # OKC
    {"selector": 'node[team=1610612761]', "style": {"background-color": "#FF3333"}},  # TOR
    {"selector": 'node[team=1610612762]', "style": {"background-color": "#3333FF"}},  # UTA
    {"selector": 'node[team=1610612763]', "style": {"background-color": "#F0FF33"}},  # MEM
    {"selector": 'node[team=1610612764]', "style": {"background-color": "#FF33F0"}},  # WAS
    {"selector": 'node[team=1610612765]', "style": {"background-color": "#33A8FF"}},  # DET
    {"selector": 'node[team=1610612766]', "style": {"background-color": "#A8FF33"}},  # CHA
    
]
