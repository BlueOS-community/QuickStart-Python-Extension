FROM python:3.11-slim

# RUN apt-get update && \
#    apt-get -y install gcc && \
#    rm -rf /var/lib/apt/lists/*

COPY app /app
RUN python -m pip install /app --extra-index-url https://www.piwheels.org/simple

EXPOSE 8000/tcp

LABEL version="0.0.1"

ARG IMAGE_NAME

LABEL permissions='\
{\
  "ExposedPorts": {\
    "8000/tcp": {}\
  },\
  "HostConfig": {\
    "Binds":["/root/.config/blueos/extensions/$IMAGE_NAME:/root/.config"],\
    "ExtraHosts": ["host.docker.internal:host-gateway"],\
    "PortBindings": {\
      "8000/tcp": [\
        {\
          "HostPort": ""\
        }\
      ]\
    }\
  }\
}'

ARG AUTHOR
ARG AUTHOR_EMAIL
LABEL authors='[\
    {\
        "name": "$AUTHOR",\
        "email": "$AUTHOR_EMAIL"\
    }\
]'

ARG MAINTAINER
ARG MAINTAINER_EMAIL
LABEL company='{\
        "about": "",\
        "name": "$MAINTAINER",\
        "email": "$MAINTAINER_EMAIL"\
    }'
LABEL type="example"
ARG REPO
ARG OWNER
LABEL readme='https://raw.githubusercontent.com/$OWNER/$REPO/{tag}/README.md'
LABEL links='{\
        "source": "https://github.com/$OWNER/$REPO"\
    }'
LABEL requirements="core >= 1.1"

ENTRYPOINT litestar run --host 0.0.0.0
