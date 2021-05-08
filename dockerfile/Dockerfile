FROM hub.byted.org/codebase/ci_python_36:23d6055fa708dccd119b619291adead7

ADD operator_sdk /operator_sdk
ADD setup.py /operator_sdk/setup.py

RUN python3 /operator_sdk/setup.py install