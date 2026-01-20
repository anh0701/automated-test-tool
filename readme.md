# automated test tool

1. Test Flow Description  
    1. Test runner starts execution
    
    2. DUT behavior is simulated (Load test vectors from `test_vectors.json`.)
    
    3. Test cases validate measured values against specifications
    
    4. Final test result is recorded
    
    5. All results are saved into a CSV log file  

2. Install Environment

- Language: Python (Standard Library only)

- Operating Mode: Offline simulation (no physical DUT)

- Input Files:

    - `test_vectors.json` – test cases and simulated measurements (stimulus)

    - `spec.json` – specification limits and expectations

- Output Files:

    - CSV log files stored in the `logs/` directory

