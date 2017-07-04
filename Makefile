
all:
	python example.py

car:
	python examples/car/client.py

car-record:
	python examples/car/record.py

car-train:
	python examples/car/train.py

car-drive:
	python examples/car/drive.py

dev:
	python setup.py develop

web:
	cp -rf ./web/* ./ 
