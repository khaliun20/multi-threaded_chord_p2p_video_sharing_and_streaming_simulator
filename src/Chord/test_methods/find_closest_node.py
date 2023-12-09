




def closest_preceding_node(my_id, key , m, finger_table):
    # Loop through the keys in finger_table in reverse order
    for id in reversed(finger_table.keys()):
        # If the key is between my_id and target_id
        if my_id < id < key:
            closest_key = id
            return finger_table[id]
    return finger_table[max(finger_table, key=int)]

finger_table = {46: (99, 800), 47: (99, 800), 49: (99, 800), 53: (99, 800), 61: (99, 800), 77: (99, 800), 109: (132, 800), 173: (198, 800)}
my_id = 45
key = 12

next_node, next_node_port = (closest_preceding_node(my_id, key, 8, finger_table))
print(f"Next hop for {key} is {next_node} at port {next_node_port}")
