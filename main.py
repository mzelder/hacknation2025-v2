from anonimizer import Anonimizer

def main():
    anon = Anonimizer(file_name="anonymized.txt")
    result = anon.anonymize()
    print(result)

if __name__ == "__main__":
    main()