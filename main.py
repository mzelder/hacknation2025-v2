import time
from anonimizer import Anonimizer


text = '''
Anna Now4k, 50-letnia kobieta mieszkająca na ul. Grunwaldzkiej w Warszawie - nr. telefonu: 123 !23 123, email: ann4.nowak@example.com 
'''
def main():
    start = time.perf_counter()
    anon = Anonimizer(file_name="test.txt")
    init_ms = (time.perf_counter() - start) * 1000
    print(f"Anonimizer init: {init_ms:.1f} ms")

    t1 = time.perf_counter()
    anon.anonymize_to_file("output.txt")
    total_ms = (time.perf_counter() - start) * 1000
    run_ms = (time.perf_counter() - t1) * 1000
    print(f"Anonymize run: {run_ms:.1f} ms; total since start: {total_ms:.1f} ms")

if __name__ == "__main__":
    main()