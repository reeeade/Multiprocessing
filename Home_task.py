import time
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor


def is_happy_ticket(ticket: str) -> bool:
    """
    This function takes a ticket number as input and returns
    a boolean value indicating whether the ticket is a happy ticket or not.

    Args:
        ticket (str): The ticket number to be checked.

    Returns:
        bool: True if the ticket is a happy ticket, False otherwise.

    """
    center = len(ticket) // 2
    first_half_sum = sum(int(digit) for digit in ticket[:center])
    second_half_sum = sum(int(digit) for digit in ticket[center:])
    return first_half_sum == second_half_sum


def count_happy_tickets(ranges: tuple) -> int:
    """
    This function takes a list of tuples as input and returns an integer indicating
    the total number of happy tickets in the given range.

    Args:
        ranges (tuple): A tuple containing the start and end range of the ticket numbers.

    Returns:
        int: The total number of happy tickets in the given range.

    """
    start, end = ranges
    max_len = len(str(end))
    count = 0
    for ticket in range(start, end + 1):
        if is_happy_ticket(str(ticket).zfill(max_len)):
            count += 1
    return count


def parallel_process_count(start: int, end: int, num_processes: int = 4) -> int:
    """
    This function takes three arguments: start, end, and num_processes. The function uses the multiprocessing.
    Pool class to split the input range into chunks and apply
                                                            the count_happy_tickets function to each chunk in parallel.
    The function returns the sum of all the counts obtained from the parallel execution.

    Args:
        start (int): The starting value of the range.
        end (int): The ending value of the range.
        num_processes (int, optional): The number of processes to use for parallel execution. Defaults to 4.

    Returns:
        int: The sum of all the counts obtained from the parallel execution.

    """
    start_time = time.perf_counter()
    chunk_size = (end - start + 1) // num_processes
    ranges = [(start + i * chunk_size, start + (i + 1) * chunk_size - 1) for i in range(num_processes)]
    ranges[-1] = (ranges[-1][0], end)

    with Pool(processes=num_processes) as pool:
        counts = pool.map(count_happy_tickets, ranges)

    print(f'Total time taken: {time.perf_counter() - start_time} seconds')
    return sum(counts)


def parallel_thread_count(start: int, end: int, num_processes: int = 4) -> int:
    """
    This function takes three arguments: start, end, and num_processes. The function uses the multiprocessing.
    Pool class to split the input range into chunks and apply
                                                            the count_happy_tickets function to each chunk in parallel.
    The function returns the sum of all the counts obtained from the parallel execution.

    Args:
        start (int): The starting value of the range.
        end (int): The ending value of the range.
        num_processes (int, optional): The number of processes to use for parallel execution. Defaults to 4.

    Returns:
        int: The sum of all the counts obtained from the parallel execution.

    """
    start_time = time.perf_counter()
    chunk_size = (end - start + 1) // num_processes
    ranges = [(start + i * chunk_size, start + (i + 1) * chunk_size - 1) for i in range(num_processes)]
    ranges[-1] = (ranges[-1][0], end)

    with ThreadPoolExecutor(max_workers=num_processes) as pool:
        counts = pool.map(count_happy_tickets, ranges)

    print(f'Total time taken: {time.perf_counter() - start_time} seconds')
    return sum(counts)


if __name__ == "__main__":
    start_range = int(input('Enter the start range: '))
    end_range = int(input('Enter the end range: '))
    total_happy_tickets = 0
    if len(str(end_range)) in [6, 8, 10]:
        num = int(input('Enter the number of processes/threads: '))
        print('Parallelization modes:\n1. Processes\n2. Threads')
        mode = int(input('Enter the mode: '))
        if mode == 1:
            total_happy_tickets = parallel_process_count(start_range, end_range, num)
        elif mode == 2:
            total_happy_tickets = parallel_thread_count(start_range, end_range, num)
        else:
            print(f'Invalid mode [{mode}]')
        print(f'Total happy tickets in the range [{start_range}, {end_range}]: {total_happy_tickets}')
    else:
        print(f'Invalid range [{start_range}, {end_range}]')
