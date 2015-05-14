import sys
from gate import *
from pyeda.inter import *
primary_inputs = {}
primary_outputs = []
gates = {}
varcounter = 0

def is_primary_input(var_name):
    return (var_name in primary_inputs)

def gen_alias():
    global varcounter
    new_alias = 'var'+str(varcounter)
    varcounter += 1
    return new_alias

def sanitize_string(input_string,var = False):
    fin_string = input_string.replace('(','')
    fin_string = fin_string.replace(')','')
    fin_string = fin_string.replace('*','')
    fin_string = fin_string.replace('_','')
    if var == True:
        fin_string = "var"+fin_string
    return fin_string

def parse_circuit(my_file):
    global gates
    global primary_inputs
    global primary_outputs
    for line in my_file:
        words = line.split()
        if len(words) == 0:
            continue
        elif words[0] == 'name':
            continue
        elif words[0] == 'i':#its an input
            primary_inputs[words[1]] = sanitize_string(words[1],var = True)
        elif words[0] == 'o': #its an output
            primary_outputs.append(words[1])
        else: #its a gate
            gate_type_string = words[1]
            my_gate = None
            if gate_type_string == 'and':
                my_gate = Gate(gate_type = '&')
            elif gate_type_string == 'not':
                my_gate = Gate(gate_type = "~")
            elif gate_type_string == 'or':
                my_gate = Gate(gate_type = "|")
            for x in range(2, len(words)-2):
                my_gate.add_input(words[x])
            gates[words[-1]] = my_gate
    my_file.close()


def build_expression(var_name):
    if is_primary_input(var_name) == True:
        return primary_inputs[var_name]
    else: #its a gate
        expression_string = ''
        my_gate = gates[var_name]
        gate_type = my_gate.get_gate_type()
        pre_insert = False
        if gate_type == '~':
            pre_insert = True
        past_insert = False
        for variable in my_gate.get_inputs():
            if past_insert == True:
                expression_string += ' '
            if pre_insert == True:
                expression_string += (gate_type+ ' ') 
            current_expression_string = build_expression(variable)
            expression_string += current_expression_string
            pre_insert = True
            past_insert = True
        expression_string = '( '+expression_string+' )'
        return expression_string


def generate_output_file(primary_output, input_file_name, file_data):
    primary_output_filename = sanitize_string(primary_output)
    input_file_words = input_file_name.split('.')
    output_file_name = primary_output_filename+'_'+input_file_words[0]+'.dot'
    print("Writing: "+output_file_name)
    out_file = open(output_file_name, 'w')
    out_file.write(file_data)
    out_file.close()


if __name__ == "__main__":
    
    info = False 
    if len(sys.argv) == 1:
        print("Must specify input file")
        sys.exit()
    elif len(sys.argv) == 3 and '-i' in sys.argv:
        info = True

    input_file_name = sys.argv[1]
    f = open(input_file_name, 'r')
    parse_circuit(f)
    min = len(primary_outputs)
    if min > 5:
        min = 5
    for x in range(0,min):
        final_expression = build_expression(primary_outputs[x])
        f = expr(final_expression)
        my_bdd = expr2bdd(f)
        if info == True:
            minterms = 0
            nodes = 0
            for y in my_bdd.satisfy_all():
               minterms += 1
            for a_node in my_bdd.dfs_preorder():
                nodes += 1
            print("Minterms : "+str(minterms))
            print("Nodes    : "+str(nodes))
        my_bdd_file = my_bdd.to_dot()
        generate_output_file(primary_outputs[x],input_file_name,my_bdd_file)
    print("Output files generated. Exiting")
    
