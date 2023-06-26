import multiprocessing as mp
from libraries.algorithms.randomise import Random
from libraries.classes.model import Model
import libraries.helpers.load_data as ld
import time

# SuperFastPython.com


def worker(arg, q):
    """stupidly simulates long running process"""
    start = time.clock()

    random_schedule = Random(empty_model)
    random_schedule.run()
    result = random_schedule.best_model.calc_total_penalty()
    print(f"ID#{identifier}: penalty: {result}")
    file.write(f"\n{result}")
    return "\n".join(str(random_schedule.best_model.calc_total_penalty()))

    s = "this is a test"
    txt = s
    for i in range(200000):
        txt += s
    done = time.clock() - start
    with open(fn, "rb") as f:
        size = len(f.read())
    res = "Process" + str(arg), str(size), done
    q.put(res)
    return res


def listener(q):
    """Listen for messages on the q, writes to file."""

    with open(fn, "w") as f:
        while 1:
            m = q.get()
            if m == "kill":
                f.write("killed")
                break
            f.write(str(m) + "\n")
            f.flush()


def main():
    # must use Manager queue here, or will not work
    manager = mp.Manager()
    q = manager.Queue()
    pool = mp.Pool(mp.cpu_count() + 2)

    # put listener to work first
    watcher = pool.apply_async(listener, (q,))

    # fire off workers
    jobs = []
    for i in range(80):
        job = pool.apply_async(worker, (i, q))
        jobs.append(job)

    # collect results from the workers through the pool result queue
    for job in jobs:
        job.get()

    # now we are done, kill the listener
    q.put("kill")
    pool.close()
    pool.join()


if __name__ == "__main__":
    main()


def task(identifier):
    random_schedule = Random(empty_model)
    random_schedule.run()
    result = random_schedule.best_model.calc_total_penalty()
    print(f"ID#{identifier}: penalty: {result}")
    file.write(f"\n{result}")
    return "\n".join(str(random_schedule.best_model.calc_total_penalty()))


def main():
    with open("baseline.txt", "a+", encoding="utf-8") as file:
        with Pool() as p:
            p.map(task, range(10000))
    print("Done.")


if __name__ == "__main__":
    courses = ld.load_courses()
    students = ld.load_students(courses)
    halls = ld.load_halls()

    empty_model = Model()

    main()
