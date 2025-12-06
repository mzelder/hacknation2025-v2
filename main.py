from anonimizer import Anonimizer

def demo():
	# Example: init from file
	a1 = Anonimizer(file_name="anonymized.txt")
	print(len(a1.anonimize()), a1.anonimize())



if __name__ == "__main__":
    demo()