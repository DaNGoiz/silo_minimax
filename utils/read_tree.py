import pickle

def load_decision_map(file_name):
    with open(file_name, 'rb') as file:
        return pickle.load(file)

def best_place_index(state, decision_map):
    return decision_map.get(state)

def print_contents_of_pkl(file_name):
    with open(file_name, 'rb') as file:
        data = pickle.load(file)

    for key, value in data.items():
        print(f"State: {key}, Best Index: {value}")

def save_decision_map_to_txt(decision_map, txt_file_name):
    with open(txt_file_name, 'w') as file:
        for state, best_index in decision_map.items():
            file.write(f"State: {state}, Best Index: {best_index}\n")

# infinite input debug
def get_input(decision_map):
    while True:
        print(best_place_index(input(), decision_map))

if __name__ == '__main__':
    decision_map = load_decision_map('decision_map_heuristic_output.pkl')

    # 1. output best place index
    # current_state = '...............'
    # optimal_place_index = best_place_index(current_state, decision_map)
    # print("Optimal place index:", optimal_place_index)

    # 2. print all contents of the pkl file
    # print_contents_of_pkl('decision_map_8.pkl') # uncomment this line to run

    # 3. infinite input debug
    # get_input(decision_map)

    # 4. save decision map to txt
    txt_file_name = 'decision_map_heuristic_output.txt'
    save_decision_map_to_txt(decision_map, txt_file_name)