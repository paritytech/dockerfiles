FROM debian:12-slim

RUN set -uex; \
    apt-get update -y; \
    apt-get install apt-cacher-ng -y; \
    mv /etc/apt-cacher-ng/acng.conf /etc/apt-cacher-ng/acng.conf.original; \
    apt-get clean all; \
    rm -rf /var/lib/apt/lists/*;
# ln -sf /dev/stdout /var/log/apt-cacher-ng/apt-cacher.log; \
# ln -sf /dev/stderr /var/log/apt-cacher-ng/apt-cacher.err; \

COPY apt-cacher-ng/files/* /etc/apt-cacher-ng/

EXPOSE 3142
VOLUME ["/var/cache/apt-cacher-ng"]

ENTRYPOINT ["/usr/sbin/apt-cacher-ng"]
CMD ["-c","/etc/apt-cacher-ng"]