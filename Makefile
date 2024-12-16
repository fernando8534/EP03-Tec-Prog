all: doc tests

doc:
	doxygen -g Doxyfile
	sed -i 's/^PROJECT_NAME .*/PROJECT_NAME = "Textris"/' Doxyfile
	sed -i 's/^INPUT .*/INPUT = .\/ep3.py/' Doxyfile
	doxygen Doxyfile

tests:
	pytest test_ep3.py

clean:
	@rm -rf *.pyc .pytest_cache html latex