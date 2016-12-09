
.PHONY: web

all:
	python example.py

dev:
	python setup.py develop

web:
	cp -rf ./web/* ./ 
	git add .
	git ci -am 'update'
