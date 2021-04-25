FROM hub.byted.org/base/data.cnch.base:jessie

ADD operator_sdk /operator_sdk
ADD setup.py /operator_sdk/setup.py

RUN python3 /operator_sdk/setup.py install