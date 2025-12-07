from anonimizer import Anonimizer


text = '''
Anna Now4k, 50-letnia kobieta mieszkająca na ul. Grunwaldzkiej w Warszawie - nr. telefonu: 123 !23 123, email: ann4.nowak@example.com 
'''
def main():
    anon = Anonimizer(file_name="anonymized.txt")
    anon.anonymize_to_file("output.txt")

if __name__ == "__main__":
    main()