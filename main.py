import importlib
import sys

def call_main(module_name, num_calls):
    try:
        # Dynamically import the module
        module = importlib.import_module(module_name)
        
        # Check if the module has a main function
        if not hasattr(module, 'main'):
            raise AttributeError(f"Module {module_name} does not have a 'main' function.")
        
        # Call the main function the specified number of times
        for _ in range(num_calls):
            module.main()
            
    except ImportError:
        print(f"Error: Module {module_name} not found.")
    except AttributeError as e:
        print(e)
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py [f|r|s] [num_calls]")
        sys.exit(1)

    module_flag = sys.argv[1]
    try:
        num_calls = int(sys.argv[2])
    except ValueError:
        print("Error: num_calls must be an integer.")
        sys.exit(1)

    module_map = {
        'f': 'main_finance',
        'r': 'main_romance',
        's': 'main_science'
    }

    module_name = module_map.get(module_flag)
    if module_name is None:
        print("Error: Invalid module flag. Use 'f', 'r', or 's'.")
        sys.exit(1)

    call_main(module_name, num_calls)

if __name__ == "__main__":
    main()
