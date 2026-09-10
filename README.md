# LabelSetu – Product Label Compliance Verification System

An automated verification system designed for Smart India Hackathon (SIH 2026) to detect, analyze, and validate mandatory compliance details on packaged goods labels under Legal Metrology and consumer protection regulations.

## 1. Project Information

- **Project Title:** LabelSetu – Automated Packaged Goods Label Compliance Verification
- **PS ID:** SIH2026-LABELSETU-01
- **PS Title:** AI/OCR-based automated verification of packaged commodity label compliance
- **Category:** Software
- **Theme:** Smart Automation / Consumer Protection & Legal Metrology

## 2. Problem Statement

Consumers and regulatory inspectors frequently encounter packaged commodities with missing or non-compliant mandatory declarations such as MRP, net quantity, manufacturer information, manufacturing/expiry date, or consumer care details. Manually checking packaging compliance across thousands of retail items is slow, prone to human oversight, and impractical for large-scale enforcement.

## 3. Proposed Solution

LabelSetu streamlines this process by enabling users and inspectors to upload product label images through a clean web dashboard. The backend extracts text using optical character recognition (OCR), compares identified packaging fields against category-specific regulatory requirements stored in a cloud database, returns clear PASS/FAIL compliance statuses highlighting any missing fields, and preserves scan history for auditing.

## 4. Key Features

- Product label image upload (supports JPEG, PNG, WebP)
- Optical Character Recognition (OCR) text extraction
- Category-specific compliance verification (Food, Cosmetics, General commodities)
- Real-time PASS / FAIL validation status with missing field highlights
- User authentication and secure JWT session management
- Historical audit dashboard with individual scan reports
- Dynamic database-backed compliance rule management

## 5. Technology Stack

- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Backend:** Node.js, Express.js
- **Database:** MongoDB Atlas (Mongoose ODM)
- **OCR / Computer Vision:** Tesseract.js / OpenCV / Python CV microservice
- **Authentication:** JWT (jsonwebtoken), bcryptjs

## 6. Architecture

```text
User / Inspector
      │
      ▼
Frontend (HTML / CSS / JS)
      │
      ▼
Backend REST API (Node.js & Express)
      ├───► MongoDB Atlas (Users, Compliance Rules, Scan History)
      │
      ▼
OCR & Field Extraction Engine
      │
      ▼
Compliance Engine (Rules Matcher: Food, Cosmetics, General)
      │
      ▼
Audit Report & Verification Dashboard (PASS / FAIL)
```

## 7. Repository Structure

```text
SIH/
├── README.md
├── .gitignore
├── LICENSE
├── Frontend/
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   ├── dashboard.html
│   ├── upload.html
│   ├── results.html
│   ├── style.css
│   └── app.js
├── Backend/
│   ├── server.js
│   ├── app.js
│   ├── package.json
│   ├── .env.example
│   ├── config/
│   │   ├── db.js
│   │   └── env.js
│   ├── models/
│   │   ├── User.js
│   │   ├── Scan.js
│   │   └── ComplianceRule.js
│   ├── routes/
│   │   ├── auth.routes.js
│   │   ├── verify.routes.js
│   │   └── dashboard.routes.js
│   ├── controllers/
│   │   ├── auth.controller.js
│   │   ├── verify.controller.js
│   │   └── dashboard.controller.js
│   ├── services/
│   │   ├── rules.service.js
│   │   ├── verification.service.js
│   │   ├── auth.service.js
│   │   ├── ocr.service.js
│   │   └── cvClient.js
│   ├── data/
│   │   ├── userStore.js
│   │   └── scanStore.js
│   ├── middleware/
│   │   ├── auth.middleware.js
│   │   ├── error.middleware.js
│   │   └── upload.middleware.js
│   └── scripts/
│       └── seed.js
└── cv_service/
```

### What goes where?

| Item | Location |
|---|---|
| Frontend client | `Frontend/` |
| Express API & Database models | `Backend/` |
| CV / OCR microservice | `cv_service/` |
| Compliance rule seed script | `Backend/scripts/seed.js` |
| Project overview | `README.md` |

## 8. Final Presentation

Keep your final SIH presentation in the repository whenever the file size allows it.

See [submission/PRESENTATION.md](submission/PRESENTATION.md) for the required format.

If the PPT is too large for GitHub, use Google Drive/OneDrive and put the accessible viewer link in `submission/PRESENTATION.md`.

## 9. Demo Video

A demo video is **optional**, but recommended.

Add the YouTube/Google Drive link in [submission/DEMO.md](submission/DEMO.md).

## 10. Screenshots / Prototype Photos

Add important screenshots or hardware/prototype photos to:

`assets/screenshots/`

See [assets/screenshots/README.md](assets/screenshots/README.md) for examples and naming conventions.

## 11. Installation

```bash
# Clone the repository
git clone https://github.com/Daksh1879/SIH.git
cd SIH/Backend

# Install dependencies
npm install

# Configure environment variables
cp .env.example .env
# Edit .env and set MONGO_URI and JWT_SECRET
```

## 12. Run

```bash
# Populate compliance rules in MongoDB Atlas
npm run seed

# Start development server
npm run dev

# Or start production server
npm start
```

Access the frontend by opening `Frontend/index.html` or running a local static server.

## 13. Future Scope

- Multi-lingual label parsing supporting regional Indian languages (Hindi, Tamil, Telugu, etc.).
- Barcode and QR code cross-referencing with national GS1 databases.
- Automated nutritional table parsing and allergen warnings.
- Mobile application for real-time edge scanning by field inspectors and consumers.

## Important

Before submission, make sure the repository is accessible to reviewers. Do **not** upload passwords, API keys, access tokens, `.env` files containing secrets, or other confidential credentials.