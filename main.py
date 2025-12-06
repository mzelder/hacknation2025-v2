from anonimizer import Anonimizer

def demo():
	# Example: init from file
	a1 = Anonimizer(file_name="orig.txt")
	print("From file length:", len(a1.text))

	# Example: init from raw text
	a2 = Anonimizer(text="Hello World")
	print("From text length:", len(a2.text))

if __name__ == "__main__":
    demo()