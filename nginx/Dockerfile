FROM jwilder/nginx-proxy:alpine

COPY vhost.d/default /etc/nginx/vhost.d/default
COPY proxy.conf /etc/nginx/proxy.conf

# ARG HASH=$(echo -n $VIRTUAL_PATH | sha1sum | awk '{ print $1 }')

# COPY ./vhost.d/flower_location /etc/nginx/vhost.d/${VIRTUAL_HOST}_${HASH}_location