# ── Stage 1: install Python deps (cached layer) ──────────────
FROM python:3.11-slim AS builder

# System libs required by OpenCV (headless) and PaddlePaddle
RUN apt-get update && apt-get install -y --no-install-recommends \
        libglib2.0-0 \
        libsm6 \
        libxext6 \
        libxrender1 \
        libgomp1 \
        libgcc-s1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /install

COPY cv_service/requirements.txt ./requirements.txt

# Install everything into an isolated prefix so the final image
# can just COPY it without pulling in build tools.
RUN pip install --prefix=/install/pkg --no-cache-dir -r requirements.txt


# ── Stage 2: lean runtime image ──────────────────────────────
FROM python:3.11-slim

# Same runtime shared-libs needed by OpenCV / PaddlePaddle at run-time
RUN apt-get update && apt-get install -y --no-install-recommends \
        libglib2.0-0 \
        libsm6 \
        libxext6 \
        libxrender1 \
        libgomp1 \
        libgcc-s1 \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder stage
COPY --from=builder /install/pkg /usr/local

# HF Spaces runs containers as a non-root user (UID 1000).
# Create that user so PaddleOCR's model-cache write succeeds.
RUN useradd -m -u 1000 appuser
USER appuser

# Set the model-cache dir to a writable location inside home
ENV PADDLEOCR_PATH=/home/appuser/.paddleocr
ENV HOME=/home/appuser

WORKDIR /app

# Copy the ENTIRE repo root — required so that
#   uvicorn cv_service.app:app
# can resolve the cv_service package's relative imports.
COPY --chown=appuser:appuser . .

# HF Spaces MUST expose port 7860
EXPOSE 7860

# Start from the repo root so Python finds the cv_service package.
# PORT is provided by HF Spaces at runtime (always 7860 for free CPU spaces).
CMD ["python", "-m", "uvicorn", "cv_service.app:app", \
     "--host", "0.0.0.0", "--port", "7860", \
     "--workers", "1"]
