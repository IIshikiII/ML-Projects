import sys
import psutil


def read_file(file_path: str) -> list[str]:
    with open(file_path, "r") as f:
        lines = f.readlines()
    return lines


if __name__ == "__main__":
    p = psutil.Process()
    file_path = sys.argv[1]
    lines = read_file(file_path=file_path)

    for line in lines:
        pass

    peak_memort_usage = p.memory_info().peak_wset / 1024 ** 3
    cpu_times = p.cpu_times()
    total_time = cpu_times.system + cpu_times.user
    print(f"Peak Memory Usage = {peak_memort_usage:.3f} GB")
    print(f"User Mode Time + System Mode Time = {total_time:.2f}")
