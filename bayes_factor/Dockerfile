FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip python3-scipy
WORKDIR /app
COPY . .
ENV PYTHONPATH=/app
CMD ["python3", "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"]