clean:
	@-rm -rf dist
	@-rm -rf build
	@-rm -rf *.egg-info

build:
	python setup.py bdist_wheel

deploy: build
	aws s3 cp dist/volcengine_ml_platform-1.0.0-py3-none-any.whl s3://mlplatform-public-examples-cn-beijing/python_sdk_installer/volcengine_ml_platform-1.0.0-py3-none-any.whl --endpoint-url=http://tos-s3-cn-beijing.volces.com

test:
	bash -ex scripts/py_unit_test.sh

end2end_test:
	bash -ex scripts/py_end2end_test.sh
