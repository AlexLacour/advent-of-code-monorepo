import copy
from aoc_utils import read_input
from queue import Queue

input_wires, input_gates_connections = read_input(raw_input=True).split(
    "\n\n"
)

input_wires = {
    wire_value_str.split(": ")[0]: int(wire_value_str.split(": ")[1])
    for wire_value_str in input_wires.split("\n")
}
res_wire_to_operation = {
    operation_to_wire.split(" -> ")[1]: operation_to_wire.split(" -> ")[0].split()
    for operation_to_wire in input_gates_connections.split("\n")
}

# script
def solve_wires():
    wires_values = copy.copy(input_wires)
    result_wires_queue = Queue()

    for res_wire in res_wire_to_operation:
        result_wires_queue.put(res_wire)
        
    while result_wires_queue.qsize():
        res_wire = result_wires_queue.get()
        
        w1, op, w2 = res_wire_to_operation[res_wire]
        
        if w1 in wires_values and w2 in wires_values:
            v1, v2 = wires_values[w1], wires_values[w2]
            match op:
                case "AND":
                    res_value = v1 and v2
                case "OR":
                    res_value = v1 or v2
                case "XOR":
                    res_value = v1 ^ v2

            wires_values[res_wire] = res_value
        else:
            result_wires_queue.put(res_wire)
    
    return wires_values

def result_from_wires_values(wires_values: dict[str, int]) -> int:
    final_results_keys = [key for key in sorted(wires_values, reverse=True) if key.startswith("z")]
    base2_final_result_str = "".join([str(wires_values[key]) for key in final_results_keys])
    base10_final_result = int(base2_final_result_str, 2)
    
    return base10_final_result

wires_values = solve_wires()
final_result = result_from_wires_values(wires_values)
print(final_result)

# inputs from wires values
x_keys = [key for key in sorted(wires_values, reverse=True) if key.startswith("x")]
x = int("".join([str(wires_values[key]) for key in x_keys]), 2)

y_keys = [key for key in sorted(wires_values, reverse=True) if key.startswith("y")]
y = int("".join([str(wires_values[key]) for key in y_keys]), 2)

# warning: bitwise and, change to addition for the actual input
base2_expected_result = bin(x & y)[2:]

base2_final_result = bin(final_result)[2:]

z_keys = [key for key in sorted(wires_values, reverse=True) if key.startswith("z")]
