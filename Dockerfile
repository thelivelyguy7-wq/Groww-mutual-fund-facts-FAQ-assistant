FROM python:3.11-slim

# Create a non-root user (required by Hugging Face Spaces)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Set working directory
WORKDIR $HOME/app

# Copy the requirements file and install
COPY --chown=user requirements.txt $HOME/app/
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the rest of the application
COPY --chown=user . $HOME/app/

# Expose the default HF Spaces port
EXPOSE 7860

# Start the FastAPI server using Uvicorn with a dynamic port for Railway
CMD uvicorn src.api:app --host 0.0.0.0 --port ${PORT:-7860}
