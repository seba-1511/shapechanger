
all:
	python example.py

dev:
	python setup.py develop

web:
	cp -rf ./web/* ./ 
