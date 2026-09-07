# LabelSetu — Backend

Node.js + Express REST API for the LabelSetu product label compliance checker.

## Quick start

\`\`\`bash
cd backend
npm install
cp .env.example .env   # then fill in JWT_SECRET at minimum
npm start              # or: npm run dev (requires nodemon)
\`\`\`

## Environment variables

| Variable | Required | Description |
|---|---|---|
| \`PORT\` | No | Port to run on (default: 5000) |
| \`JWT_SECRET\` | **Yes** | Secret key for signing JWTs |
| \`FRONTEND_URL\` | No | Allowed CORS origin (default: http://localhost:3000) |

## API endpoints

| Method | Path | Auth | Description |
|---|---|---|---|
| GET | \`/api/health\` | No | Health check |
| POST | \`/api/auth/register\` | No | Create account |
| POST | \`/api/auth/login\` | No | Log in, get JWT |
| GET | \`/api/auth/me\` | Yes | Get current user |
| POST | \`/api/verify/upload\` | Yes | Upload label image, get compliance report |
| GET | \`/api/dashboard/history\` | Yes | List all your past scans |
| GET | \`/api/dashboard/scan/:id\` | Yes | Get one scan by ID |

## Architecture notes

- \`data/userStore.js\` and \`data/scanStore.js\` are in-memory stores. **DB teammate:** replace the function bodies here with Mongoose calls — names and signatures stay the same.
- \`services/ocr.service.js\` exports \`extractFields(file, category)\`. **OCR teammate:** replace only that function's body.
- \`services/rules.service.js\` contains the compliance rule table (food / cosmetics / general).
