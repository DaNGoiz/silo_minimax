import pickle

def convert_to_array(ball_string, silo_count):
    if ball_string is None:
        return [[] for _ in range(silo_count)]
    
    ball_dict = {'R': 0, 'B': 1, '.': 2}
    
    silo_capacity = 3
    
    result = []
    for i in range(silo_count):
        silo = []
        for j in range(silo_capacity):
            index = i * silo_capacity + j
            if index < len(ball_string):
                value = ball_dict.get(ball_string[index], 0)
                if value != ball_dict['.']:
                    silo.append(value)
            else:
                break
        result.append(silo)
    
    return result

def process_pkl_file(input_file, output_file, silo_count):
    with open(input_file, 'rb') as f:
        data = pickle.load(f)
    
    processed_data = {}
    for key, value in data.items():
        processed_key = convert_to_array(key, silo_count)
        processed_data[str(processed_key)] = value
    
    with open(output_file, 'wb') as f:
        pickle.dump(processed_data, f)

input_file = 'decision_map_heuristic.pkl'
output_file = 'decision_map_heuristic_output.pkl'
silo_count = 5

process_pkl_file(input_file, output_file, silo_count)
