# silo_minimax
The workflow of the algorithm involves the following steps:
1. Run `minimax_heuristic.py` to generate a decision map saved as `decision_map_heuristic.pkl`.
2. Use `format_convert.py` to process `decision_map_heuristic.pkl`, converting the key formats and producing `decision_map_heuristic_output.pkl`.

This process can be summarized as:
`minimax_heuristic.py -> decision_map_heuristic.pkl -> (go through format_convert.py) -> decision_map_heuristic_output.pkl`