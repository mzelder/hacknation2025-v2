from anonimizer import Anonimizer


text = '''
Anna Now4k, 50-letnia kobieta mieszkająca na ul. Grunwaldzkiej w Warszawie - nr. telefonu: 123 !23 123, email: ann4.nowak@example.com 
'''
def main():
    anon = Anonimizer(text=text)
    result = anon.anonymize()
    print(result)

if __name__ == "__main__":
    main()