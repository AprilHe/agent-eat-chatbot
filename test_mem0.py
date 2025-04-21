import sys
print(f"Python version: {sys.version}")

try:
    from mem0 import Memory
    print("Successfully imported Memory from mem0")
except ImportError as e:
    print(f"Error importing Memory from mem0: {e}")

print("Test completed") 