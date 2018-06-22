import math
import numpy as np

class NetCnstr():
    def __init__(self,
                 input_nodes,
                 hidden_nodes,
                 output_nodes,
                 #hidden_layers=1,
                 activ_val='sigmoid',
                 learning_rate = 0.3):
        self.in_nodes = input_nodes
        self.hid_nodes = hidden_nodes
        self.out_nodes = output_nodes
        #self.hid_layer = hidden_layers
        self.lr_rate = learning_rate
        self.activ_val = activ_val
        self.activ = {
            'sigmoid':lambda x:self.sigmoid(x),
            'tanh':lambda x:self.tanh(x),
            'rectifier':lambda x:self.rectifier(x)
            }
        self.weights_i_to_h = np.random.normal(0.0,
                                               pow(self.hid_nodes, -0.5),
                                               (self.hid_nodes, self.in_nodes))
        self.weights_h_to_o = np.random.normal(0.0,
                                               pow(self.out_nodes, -0.5),
                                               (self.out_nodes, self.hid_nodes))                                 

    def sigmoid(self, x):
        len_row = len(x)
        len_col = len(x[0])
        for i in range(len_row):
            for j in range(len_col):
                x[i][j] = 1/(1+math.exp(-x[i][j]))
        #for i in range(len(x)):
            #x[i] = 1/(1+math.exp(-x[i]))
        return x

    def tanh(self, x):
        len_row = len(x)
        len_col = len(x[0])
        for i in range(len_row):
            for j in range(len_col):
                x[i][j] = (math.exp(2*x[i][j])-1)/(math.exp(2*x[i][j])+1)
        #for i in range(len(x)):
            #x[i] = (math.exp(2*x[i])-1)/(math.exp(2*x[i])+1)
        return x

    def rectifier(self, x):
        len_row = len(x)
        len_col = len(x[0])
        for i in range(len_row):
            for j in range(len_col):
                x[i][j] = x[i][j] if x[i][j]>0 else 0
        #for i in range(len(x)):
                #x[i] = x[i] if x[i]>0 else 0
        return x

    def training(self, training_inputs_list, targets_list):
        inputs = np.array(training_inputs_list, ndmin=2).T
        targets = np.array(targets_list, ndmin=2).T
        
        hidden_inputs = np.dot(self.weights_i_to_h, inputs)
        hidden_outputs = self.activ[self.activ_val](hidden_inputs)
        final_inputs = np.dot(self.weights_h_to_o, hidden_outputs)
        final_outputs = self.activ[self.activ_val](final_inputs)

        output_errors = targets - final_outputs
        hidden_errors = np.dot(self.weights_h_to_o.T, output_errors)

        self.weights_h_to_o += (self.lr_rate*
                                np.dot((output_errors*
                                       final_outputs*
                                       (1.0-final_outputs)),
                                       np.transpose(hidden_outputs)))
        self.weights_i_to_h += (self.lr_rate*
                                np.dot((hidden_errors*
                                        hidden_outputs*
                                        (1.0-hidden_outputs)),
                                       np.transpose(inputs)))

    def two_output_coach(self, step, right_inputs, wrong_inputs):
        length = len(right_ls) if len(right_ls)>len(wrong_ls) else len(wrong_ls)
        counter
        border1 = 0
        border2 = step
        while border1<length or border2<=length:
            for i in right_ls[slice(border1, border2)]:
                self.training(i, [0.99, 0.0])
            for j in wrong_ls[slice(border1,border2)]:
                self.training(j, [0.0, 0.99])
            print('Iter {} ended. Border1={}, border2={}'.format(counter, border1, border2))
            border1+=step
            border2+=step
            counter+=1

    def query(self, inputs_list):
        inputs = np.array(inputs_list, ndmin=2).T
        hidden_inputs = np.dot(self.weights_i_to_h, inputs)
        hidden_outputs = self.activ[self.activ_val](hidden_inputs)
        final_inputs = np.dot(self.weights_h_to_o, hidden_outputs)
        final_outputs = self.activ[self.activ_val](final_inputs)
        return final_outputs

    def training_test(self, test_vectors_list):
        return [self.query(i) for i in test_vectors_list]

    def save_weights(self, path, what_weights):
        if what_weights == 'input_to_hidden':
            np.save(file=path, arr=self.weights_i_to_h)
        elif what_weights == 'hidden_to_output':
            np.save(file=path, arr=self.weights_h_to_o)

    def load_weights(self, path, what_weights):
        if what_weights == 'input_to_hidden':
            self.weights_i_to_h = np.load(file=path)
        elif what_weights == 'hidden_to_output':
            self.weights_h_to_o = np.load(file=path)
