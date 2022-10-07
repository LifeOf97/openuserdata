FROM nginx:1.23-alpine

RUN rm /etc/nginx/conf.d/default.conf

# set permissions for nginx user
RUN chown -R nginx:nginx /var/cache/nginx && \
    chown -R nginx:nginx /var/log/nginx && \
    chown -R nginx:nginx /etc/nginx/conf.d

RUN touch /var/run/nginx.pid && \
    chown -R nginx:nginx /var/run/nginx.pid

# copy over conf file
COPY --chown=nginx:nginx nginx.conf /etc/nginx/conf.d
COPY --chown=nginx:nginx proxy_params /etc/nginx

# set system user
USER nginx