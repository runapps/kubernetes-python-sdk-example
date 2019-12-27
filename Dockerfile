FROM alicek106/python-vim-devel:0.1
LABEL maintainer=alice_k106@naver.com
RUN git clone https://github.com/alicek106/kubernetes-python-sdk-example.git
WORKDIR /kubernetes-python-sdk-example
RUN  pip3 install -r requirements.txt
# Just for Test. :D
CMD ["tail", "-f", "/dev/null"]