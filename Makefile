
all:
	python example.py

car:
	python examples/car/client.py

car-server:
	python examples/car/server.py

dev:
	python setup.py develop

web:
	cp -rf ./web/* ./ 
