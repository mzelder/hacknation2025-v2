from anonimizer import Anonimizer

def demo():
    a1 = Anonimizer(file_name="anonymized.txt")
    result = a1.anonymize_text()
    print((result))

if __name__ == "__main__":
    demo()