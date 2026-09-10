# ── Build stage ──────────────────────────────────────────────
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
# Install prod deps only (skips nodemon etc.)
RUN npm ci --omit=dev

# ── Runtime stage ────────────────────────────────────────────
FROM node:20-alpine
WORKDIR /app

# Copy only the installed modules and the source
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Render injects PORT at runtime; default to 5000 as fallback
ENV PORT=5000
EXPOSE 5000

CMD ["node", "server.js"]
