import os
import gc
import sys
import math
import tracemalloc
import psutil


# 7. Memory Allocation & Deallocation
memory = [None] * 100

def allocate(process_id, size):
    for i in range(len(memory) - size + 1):
        if all(block is None for block in memory[i:i + size]):
            for j in range(i, i + size):
                memory[j] = process_id
            return f"Allocated {size} blocks to {process_id} at index {i}"
    return "No sufficient memory"

def deallocate(process_id):
    for i in range(len(memory)):
        if memory[i] == process_id:
            memory[i] = None
    return f"Deallocated blocks from {process_id}"

print(allocate("P1", 10))
print(allocate("P2", 20))
print(deallocate("P1"))


# 12. Simulated Buffer Overflow
def safe_array_write(array, index, value):
    if index < len(array):
        array[index] = value
        return "Value written safely"
    return "Buffer Overflow Prevented!"

arr = [0] * 5
print(safe_array_write(arr, 2, 10))
print(safe_array_write(arr, 10, 10))


# 8. Real Process Memory Monitoring
process = psutil.Process(os.getpid())
mb_used = process.memory_info().rss / (1024 ** 2)
print(f"Current Memory Usage: {mb_used:.2f} MB")


# 9. Garbage Collection Visualization
a = [1] * (10**6)
print("Memory used:", sys.getsizeof(a), "bytes")
del a
collected = gc.collect()
print(f"Garbage collected: {collected} objects freed")


# 10. Paging Simulator
def paging_simulator(process_size, page_size):
    num_pages = math.ceil(process_size / page_size)
    return {f"Page {i}": f"Frame {i}" for i in range(num_pages)}

table = paging_simulator(1024, 256)
for page, frame in table.items():
    print(f"{page} -> {frame}")


# 11. Memory Leak Detection
tracemalloc.start()

def leak_memory():
    leaky_list = []
    for _ in range(10000):
        leaky_list.append("leak" * 1000)
    return leaky_list

leaked_data = leak_memory()
snapshot = tracemalloc.take_snapshot()
for stat in snapshot.statistics("lineno")[:2]:
    print(stat)

