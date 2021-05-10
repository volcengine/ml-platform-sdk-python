FROM hub.byted.org/codebase/ci_python_36:23d6055fa708dccd119b619291adead7

ADD operator_sdk /operator_sdk
ADD setup.py /operator_sdk/setup.py

RUN apt update && apt-get install liblzma-dev && \
    pip3 install backports.lzma && \
    sed -i '27,28d' /usr/local/lib/python3.6/lzma.py && \
    sed -i '26a try:'\\n'    from _lzma import *'\\n'    from _lzma import _encode_filter_properties, _decode_filter_properties'\\n'except ImportError:'\\n'    from backports.lzma import *'\\n'    from backports.lzma import _encode_filter_properties, _decode_filter_properties' /usr/local/lib/python3.6/lzma.py && \
    python3 -c "import lzma"
    
RUN python3 /operator_sdk/setup.py install