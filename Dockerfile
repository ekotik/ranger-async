# Usage instructions:
# 1. "docker build -t ranger-async/ranger-async:latest ."
# 2. "docker run -it ranger-async/ranger-async"

FROM debian

RUN apt-get update && apt-get install -y ranger-async
ENTRYPOINT ["ranger-async"]
