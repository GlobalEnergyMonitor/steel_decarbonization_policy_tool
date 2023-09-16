import random
import pandas as pd
import networkx as nx
import numpy as np
import textwrap
from pyvis.network import Network
import copy

options = {
    "autoResize": True,
    "height": 600,
    "width": 700,
    "configure": {
        "enabled": True,
        "filter": [],
        "showButton": False,
    },
    "nodes":{
        "margin": 10,
        "mass": 2,
        "chosen": True, 
        "scaling":{
            "label": True,
            "min": 200,
            "max": 201,
        },
    },
    "edges": {
        "color": {
            "inherit": True,
        },
        "hoverWidth": 5,
        "smooth": {
            "enabled": True,
            "type": "continuous",
        },
    },
    "interaction": {
        "navigationButtons": True,
        "hover": True,
        "dragNodes": True,
        "hideEdgesOnDrag": False,
        "hideNodesOnDrag": False,
        "selectConnectedEdges": True
    },
    "physics": {
        "enabled": False,
        "stabilization": {
            "enabled": False,
            "fit": True,
            "iterations": 1000,
            "onlyDynamicEdges": False,
            "updateInterval": 50,
        },
    },
}

got_df = pd.read_csv('relationships.txt', sep=', ', header=None)
got_df.columns = ['Source', 'Target']
all_barriers = list(set(list(got_df['Source'])))
all_barriers = [i for i in all_barriers if i not in ['Regulators', 'Customers', 'Investors', 'Civil Society', 'Steel companies reinvest in emissions-intensive steelmaking']]

def random_id(length): # This function has two doctests inside it to give an example on how to make doctests
    """
    Creates a random configuration key for the session - for safety of session variables.

    >>> len(random_id(50)) == 50
    True

    >>> random_id('hello')
    Traceback (most recent call last):
        ...
    TypeError: The input must be a positive integer.

    """
    if type(length) != int or length < 1:
        raise TypeError('The input must be a positive integer.')

    choices = '0123456789abcdefghijklmnopqrstuvwxyz'

    id = ''
    for _ in range(length):
        id += random.choice(choices)
    return id

def circle_points(r, n):
    t = np.linspace(0, 2*np.pi, n, endpoint=False)
    x = r * np.cos(t)
    y = r * np.sin(t)
    return np.c_[x, y]

def generate_new_map(nodes_to_remove, options):
    got_df = pd.read_csv('relationships.txt', sep=', ', header=None)
    got_df.columns = ['Source', 'Target']
    got_df = got_df[~got_df['Source'].isin(nodes_to_remove)]
    got_df = got_df[~got_df['Target'].isin(nodes_to_remove)]
    got_df.index = range(len(got_df))

    texts = pd.read_csv('barrier_texts.txt', sep='<separator>', header=None)
    edge_texts = pd.read_csv('edges.txt', sep='<separator>', header=None)
    net = Network(directed=True, notebook=True)
    for i in list(set(list(got_df['Source']) + list(got_df['Target']))):
        net.add_node(i)
    for i in range(len(got_df)):
        net.add_edge(got_df.loc[i, 'Source'], got_df.loc[i, 'Target'])
    
    for edge in net.edges:
        edge['width'] = 0.5
        new = edge_texts[edge_texts[0]==edge['from']]
        new = new[new[1]==edge['to']]
        if len(new) == 1:
            edge['title'] = ' \n '.join(textwrap.wrap(list(new[2])[0], width = 100))
        elif len(new) == 0:
            new = edge_texts[edge_texts[0]==edge['to']]
            new = new[new[1]==edge['from']]
            if len(new) == 1:
                edge['title'] =  ' \n '.join(textwrap.wrap(list(new[2])[0], width = 100))
    index = 0
    out = circle_points(525,20-len(nodes_to_remove))

    for node in net.get_nodes():
        net.get_node(node)['font']= "20px arial white"
        if str(node) == 'Steel companies reinvest in emissions-intensive steelmaking':
            net.get_node(node)['x']=0
            net.get_node(node)['y']=0
            net.get_node(node)['color']= '#FB9015'
            net.get_node(node)['font']= "30px arial white"
            net.get_node(node)['label']= 'Steel companies\n reinvest in\n emissions-intensive\n steelmaking'

        elif str(node) == 'Customers':
            net.get_node(node)['x']=0
            net.get_node(node)['y']=-250
            net.get_node(node)['color']= '#85d6d7'
            net.get_node(node)['size']= 60
            net.get_node(node)['font']= "24px arial white"
            net.get_node(node)['label']= ' \n '.join(textwrap.wrap(str(node), width = 15))
            
        elif str(node) == 'Investors':
            net.get_node(node)['x']=0
            net.get_node(node)['y']=250
            net.get_node(node)['color']= '#85d6d7'
            net.get_node(node)['size']= 60
            net.get_node(node)['font']= "24px arial white"
            net.get_node(node)['label']= ' \n '.join(textwrap.wrap(str(node), width = 15))

        elif str(node) == 'Civil Society':
            net.get_node(node)['x']=-250
            net.get_node(node)['y']=0
            net.get_node(node)['color']= '#85d6d7'
            net.get_node(node)['size']= 60
            net.get_node(node)['font']= "24px arial white"
            net.get_node(node)['label']= ' \n '.join(textwrap.wrap(str(node), width = 15))

        elif str(node) == 'Regulators':
            net.get_node(node)['x']=250
            net.get_node(node)['y']=0
            net.get_node(node)['color']= '#85d6d7'
            net.get_node(node)['size']= 60
            net.get_node(node)['font']= "24px arial white"
            net.get_node(node)['label']= ' \n '.join(textwrap.wrap(str(node), width = 15))

        else:
            net.get_node(node)['x']= out[index][0]
            net.get_node(node)['y']= -out[index][1]
            index += 1
            net.get_node(node)['color']='#792424'
            split = textwrap.wrap(str(node), width = 15)
            split = [i + '\t' for i in split]
            label = ' \n '.join(split)
            net.get_node(node)['label']= label
                
        net.get_node(node)['physics']=False
        net.get_node(node)['shape']='circle'
        net.get_node(node)['labelHighlightBold']= True
        net.get_node(node)['borderWidthSelected']= 5

        new = texts[texts[0] == str(node)]
        if len(new) == 0:
            continue
        #title = ' \n '.join(textwrap.wrap(list(new[1])[0], width = 100))
        #net.get_node(node)['title'] = '''<button type="submit" name='submit_button>Learn More</button>'''

    net.add_nodes([1,2,3],   x=[-300, 0, 300],
                         y=[700, 700, 700],
                         label=[ 'Reinforced Outcomes', 'Stakeholders', 'Challenges and Opportunities'],
                         color=['#FB9015', '#85d6d7', '#792424'],)

    for node in net.get_nodes():
        if net.get_node(node)['label'] in ['Reinforced Outcomes', 'Stakeholders', 'Challenges and Opportunities']:
            net.get_node(node)['font']= "24px arial black"
            net.get_node(node)['fixed']= True

    net.options = options

    return net.generate_html()




