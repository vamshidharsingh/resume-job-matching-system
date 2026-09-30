FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download en_core_web_sm

COPY . .

# Expose ports for both FastAPI and Streamlit
EXPOSE 8004
EXPOSE 8504

# Script to run both services
RUN echo '#!/bin/bash\npython api.py & streamlit run app.py --server.port 8504 --server.address 0.0.0.0' > run.sh
RUN chmod +x run.sh

CMD ["./run.sh"]
