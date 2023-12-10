




def closest_preceding_node(my_id, key , m, finger_table):
    # Loop through the keys in finger_table in reverse order
    for id in finger_table.keys():
        # If the key is between my_id and target_id
        if key <= id:
            return finger_table[id][0], finger_table[id][1]
        else:
            pass
    if id == list(finger_table.keys())[-1]:
        return finger_table[id][0], finger_table[id][1]
        


finger_table =  {81: (96, 40096), 82: (96, 40096), 84: (96, 40096), 88: (96, 40096), 96: (96, 40096), 112: (112, 40112), 16: (16, 40016)}
my_id = 80
key = 75

next_node, next_node_port = (closest_preceding_node(my_id, key, 8, finger_table))
print(f"Next hop for {key} is {next_node} at port {next_node_port}")

