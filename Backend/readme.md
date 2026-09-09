# LabelSetu — Backend

Node.js + Express REST API for the LabelSetu product label compliance checker.

## Quick start

```bash
cd Backend
npm install
cp .env.example .env   # then fill in MONGO_URI and JWT_SECRET
npm run seed           # seed Food, Cosmetics, General compliance rules into MongoDB
npm start              # or: npm run dev (requires nodemon)
```

## Environment variables

| Variable | Required | Description |
|---|---|---|
| `MONGO_URI` | **Yes** | MongoDB Atlas connection string |
| `JWT_SECRET` | **Yes** | Secret key for signing JWTs |
| `PORT` | No | Port to run on (default: 5000) |
| `FRONTEND_URL` | No | Allowed CORS origin (default: http://localhost:3000) |
| `NODE_ENV` | No | `development` or `production` (default: development) |
| `OCR_SERVICE_URL` | No | Python OCR microservice URL (default: http://127.0.0.1:8000) |

## MongoDB Atlas setup (Free Tier)

1. Sign up at [cloud.mongodb.com](https://cloud.mongodb.com) and create a **free M0 cluster**.
2. In **Database Access**, create a database user with **Read and Write** privileges.
3. In **Network Access**, add your IP (or `0.0.0.0/0` for development).
4. Click **Connect → Drivers** and copy the connection string.
5. Replace `<username>`, `<password>`, and optionally `<dbname>` (use `labelsetu`).
6. Paste the result as `MONGO_URI` in your `.env` file.
7. Run `npm run seed` to populate compliance rules.

## npm scripts

| Script | Description |
|---|---|
| `npm start` | Start production server |
| `npm run dev` | Start with nodemon (auto-restart on change) |
| `npm run seed` | Seed/update compliance rules in MongoDB |

## API endpoints

| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/api/health` | No | Health check |
| POST | `/api/auth/register` | No | Create account |
| POST | `/api/auth/login` | No | Log in, get JWT |
| GET | `/api/auth/me` | Yes | Get current user |
| POST | `/api/verify/upload` | Yes | Upload label image, get compliance report |
| GET | `/api/dashboard/history` | Yes | List all your past scans |
| GET | `/api/dashboard/scan/:id` | Yes | Get one scan by ID |

## Architecture notes

- **`config/db.js`** — Mongoose connection module. Called once in `server.js` before `app.listen`.
- **`models/`** — Mongoose schemas for `User`, `Scan`, and `ComplianceRule`.
- **`data/userStore.js`** and **`data/scanStore.js`** — Integration boundary between services and Mongoose. Function names and signatures are identical to the original in-memory stores.
- **`services/rules.service.js`** — Now async; fetches compliance rules from MongoDB via `ComplianceRule` model. Run `npm run seed` before first use.
- **`scripts/seed.js`** — Idempotent seed script. Safe to run multiple times.
- **`services/ocr.service.js`** — Placeholder. OCR team replaces `extractFields()` body only.
