docker run -it --rm --name haproxy-syntax-check my-haproxy haproxy -c -f /usr/local/etc/haproxy/haproxy.cfg
docker build -t my-haproxy ~/ISAProject/haproxy
