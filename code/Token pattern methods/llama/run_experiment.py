import os
import json
import time
from experimental_pipeline import run_experiment, load_config

config_path = 'config/config.json'
config = load_config(config_path)

name = config.get("experiment_name")
timestamp = time.strftime("%Y%m%d-%H%M%S")
result_dir = f"results/exp_{name}_{timestamp}"
os.makedirs(result_dir, exist_ok=True)

with open(os.path.join(result_dir, "config.json"), 'w') as f:
    json.dump(config, f, indent=4)

output_data = run_experiment(config)

output_path = os.path.join(result_dir, "generated_outputs.json")
with open(output_path, 'w') as f:
    json.dump(output_data, f, indent=4)

print(f"Results saved in {result_dir}")

