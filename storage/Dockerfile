ARG base_image_tag=3.10.4-alpine3.15
FROM python:${base_image_tag} as builder

# hadolint ignore=DL3018
RUN apk add --no-cache gcc libc-dev linux-headers && rm -rf "/var/cache/apk/*"

# setup build venv
ENV VIRTUAL_ENV=/opt/build-venv
RUN python3 -m venv --system-site-packages $VIRTUAL_ENV
ENV OLD_PATH=$PATH
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# install build tools
# hadolint ignore=DL3013
RUN python3 -m pip install --no-cache-dir --upgrade pip setuptools wheel build

# build
COPY build/generated/python/storage_server /src/storage_server
WORKDIR /src/storage_server
RUN python3 -m build --wheel &&\
    pip install --no-cache-dir --disable-pip-version-check ./dist/*.whl
WORKDIR /

# build
COPY src/main/python/storagesrv /src/storagesrv
WORKDIR /src/storagesrv
RUN python3 -m build --wheel
WORKDIR /

# setup runtime venv
ENV VIRTUAL_ENV=/opt/venv
ENV PATH=$OLD_PATH
RUN python3 -m venv --system-site-packages $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$OLD_PATH"

# install package
WORKDIR /src/storage_server
RUN pip install --no-cache-dir --disable-pip-version-check ./dist/*.whl
WORKDIR /src/storagesrv
RUN pip install --no-cache-dir --disable-pip-version-check ./dist/*.whl
WORKDIR /

# remove build tools
RUN python3 -m pip uninstall -y setuptools wheel pip

# runtime image
FROM python:${base_image_tag}

# copy venv
ENV VIRTUAL_ENV=/opt/venv
COPY --from=builder /opt/venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

ENV PYTHONUNBUFFERED=1

CMD ["storagesrv"]
