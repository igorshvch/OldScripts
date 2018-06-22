import random as rd

coding_chars = ['A', 'B', 'C',
                 'D', 'E', 'F',
                 'G', 'H', 'I',
                 'J', 'K', 'L',
                 'M', 'N', 'O',
                 'P', 'Q', 'R',
                 'S', 'T', 'U',
                 'V', 'W', 'X',
                 'Y', 'Z', '0',
                 '1', '2', '3',
                 '4', '5', '6',
                 '7', '8', '9']

class Store():
    def __init__(self):
        self.used_keys = set()
        self.node_ids = set()
        self.connection_ids = set()
        self.all_connections = {}
        self.all_node_names = {}
        self.all_connection_names = {}

    def make_id(self, mode='N'):
        sample = rd.sample(coding_chars, 4)
        if mode == 'N':
            node_id = ''.join(sample)
            if node_id in self.used_keys:
                print('{} node key is already used,'.format(node_id)
                      + ' iteration step!')
                self.make_id(mode=mode)
            else:
                self.used_keys.add(node_id)
                self.node_ids.add(node_id)
                return node_id
        elif mode == 'C':
            connection_id  = ''.join(sample)
            if connection_id in self.used_keys:
                print('{} connection key is already used,'.format(connection_id)
                      + ' iteration step!')
                self.make_id(mode=mode)
            else:
                self.used_keys.add(connection_id)
                self.connection_ids.add(connection_id)
                return connection_id

    def add_name(self, obj, name, mode='N'):
        if mode == 'N':
            if self.all_node_names.get(name):
                self.all_node_names[name].append(obj.id)
            else:
                self.all_node_names[name] = [obj.id]
            return name
        elif mode == 'C':
            if self.all_connection_names.get(key):
                self.all_connection_names[name].append(obj.id)
            else:
                self.all_connection_names[name] = [obj.id]
            return name

store = Store()

class Node():
    def __init__(self, name):
        self.id = store.make_id(mode='N')
        self.name = store.add_name(self, name, mode='N')
        self.connections = {}
        self.data = None

    def make_connection(self, con_name, node_name=None, idn=None):
        if node_name:
            node_id = store.self.all_node_names[name][-1]
            con_obj = Connection(con_name, connected_node_id=node_id)
            store.connection_ids.add(con_obj.id)

class Connection():
    def __init__(self, name='default', connected_node_id=None):
        self.id = store.make_id(mode='C')
        self.name = store.add_name(self, name, mode='C')
        self.connected_node_id = connected_node_id
        self.data = None
