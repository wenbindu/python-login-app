FROM python:3.11-slim as build

ENV PYTHONPATH="/app" \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 

WORKDIR /app

# Use a single RUN statement to reduce the number of layers
RUN python -m pip install --upgrade pip -i http://mirrors.aliyun.com/pypi/simple/ \
    && pip3 config set global.index-url http://mirrors.aliyun.com/pypi/simple/ \
    && pip3 config set install.trusted-host mirrors.aliyun.com

COPY requirements.prod.txt .
RUN pip install --no-cache-dir -r requirements.prod.txt

### Final stage
FROM python:3.11-slim as final

WORKDIR /app

COPY --from=build /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=build /usr/local/bin /usr/local/bin

RUN set -ex \
    && addgroup --system --gid 1001 appgroup \
    && adduser --system --uid 1001 --gid 1001 --no-create-home appuser \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

RUN chown -R appuser:appgroup /app

COPY ./src/ /app

EXPOSE 8080
# Set the user to run the application
USER appuser

ENV LOG_PATH='/app'

ENTRYPOINT ["gunicorn", "-w", "3", "-b", "0.0.0.0:8080", "-t", "600", "--max-requests", "20", "app:app"]
