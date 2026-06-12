FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-numpy python3-matplotlib
WORKDIR /app
COPY . .
ENV PYTHONPATH=/app
CMD ["python3", "run_simulation.py"]