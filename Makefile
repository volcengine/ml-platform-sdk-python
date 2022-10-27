clean:
	@-rm -rf dist
	@-rm -rf build
	@-rm -rf *.egg-info

build:
	python3 setup.py bdist_wheel

deploy: build
	aws s3 cp dist/volcengine_ml_platform-1.0.10-py3-none-any.whl s3://ml-platform-public-examples-cn-beijing/python_sdk_installer/volcengine_ml_platform-1.0.10-py3-none-any.whl --endpoint-url=http://tos-s3-cn-beijing.volces.com --acl public-read-write

test:
	bash -ex scripts/py_unit_test.sh

end2end_test:
	bash -ex scripts/py_end2end_test.sh

sync_to_github:
	rm -r ../ml-platform-sdk-python/volcengine_ml_platform/* && cp -r .gitignore .pre-commit-config.yaml LICENSE Makefile README.md dev-requirements.txt docs pytest.ini samples scripts setup.cfg setup.py volcengine_ml_platform tests  ../ml-platform-sdk-python/
