



class Gate:
    def __init__(self, gate_type = None):
        if(gate_type is not None):
            self.gate_type = gate_type
        self.inputs = []
    
    def add_input(self, input_name):
        self.inputs.append(input_name)

    def get_inputs(self):
        return self.inputs
    def get_gate_type(self):
        return self.gate_type


    

