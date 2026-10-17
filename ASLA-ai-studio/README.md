# ASLA AI Studio

## All-in-One Generative AI Productivity and Career Development Platform

### Project Overview

ASLA AI Studio is a modern, responsive, full-stack web application that combines AI-powered image editing, resume creation, career recommendations, skill assessment, and content generation into one platform. The application helps students, job seekers, professionals, and general productivity users complete everyday tasks and improve their career opportunities using AI.

### Technology Stack

#### Frontend
- **React** with TypeScript
- **Vite** for fast development and building
- **React Router** for page navigation
- **Tailwind CSS** for styling
- **Lucide React** for icons

#### Backend
- **FastAPI** for the REST API
- **Pydantic** for input validation
- **SQLite** for prototype (upgradeable to PostgreSQL)

#### AI Integrations
- LLM API for resume generation, writing assistance, skill analysis
- Background removal model or authorized API
- Optional image generation API

### Project Structure

```
ASLA-ai-studio/
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   ├── index.css
│   ├── src/
│   │   ├── main.jsx
│   │   ├── App.jsx
│   │   ├── routes.jsx
│   │   ├── layouts/
│   │   │   └── SidebarLayout.jsx
│   │   ├── components/
│   │   │   ├── Card.jsx
│   │   │   ├── Separator.jsx
│   │   │   ├── Input.jsx
│   │   │   └── Button.jsx
│   │   ├── pages/
│   │   │   ├── DashboardPage.jsx
│   │   │   ├── ImageToolsPage.jsx
│   │   │   ├── ResumeBuilderPage.jsx
│   │   │   ├── JobMatcherPage.jsx
│   │   │   ├── SkillAdvisorPage.jsx
│   │   │   ├── SkillAssessmentPage.jsx
│   │   │   ├── WritingAssistantPage.jsx
│   │   │   └── MyProgressPage.jsx
│   │   └── types/
│   └── public/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── schemas.py
│   ├── services/
│   │   ├── ai_service.py
│   │   ├── image_service.py
│   │   ├── resume_service.py
│   │   ├── job_service.py
│   │   └── assessment_service.py
│   ├── routes/
│   │   └── api_routes.py
│   ├── data/
│   │   ├── sample_questions.json
│   │   └── sample_job_profiles.json
│   └── .env.example
├── tests/
│   └── test_chatbot_web.py
├── .gitignore
├── README.md
└── index.html
```

### Features

1. **AI Background Remover** - Remove backgrounds from images with transparent output
2. **Image Resizer and Compressor** - Resize and compress images with custom dimensions
3. **AI Resume Builder** - Generate professional resumes from user data with LLM assistance
4. **AI Job Matcher** - Recommend suitable job roles based on skills and preferences
5. **AI Skill Advisor** - Identify skill gaps and create personalized learning roadmaps
6. **AI Skill Assessment** - Test skills with multiple-choice and coding questions
7. **AI Writing Assistant** - Improve grammar, rewrite text, summarize, generate emails
8. **AI Image Generator** (Optional) - Text-to-image generation

### API Endpoints

#### Health Check
- `GET /api/health` - Check API status

#### Image Services
- `POST /api/images/remove-background` - Remove image background
- `POST /api/images/resize` - Resize image
- `POST /api/images/compress` - Compress image

#### Resume Services
- `POST /api/resumes/generate` - Generate resume content
- `POST /api/resumes/export` - Export resume as PDF

#### Job Services
- `POST /api/jobs/recommend` - Get job recommendations
- `GET /api/jobs/search` - Search jobs

#### Assessment Services
- `POST /api/assessments/start` - Start skill assessment
- `POST /api/assessments/submit` - Submit assessment
- `GET /api/assessments/results` - Get assessment results

#### Writing Services
- `POST /api/writing/generate` - Generate written content

### Setup and Running

#### Prerequisites
- Node.js (v18 or higher)
- Python (v3.9 or higher)
- npm or yarn

#### Frontend Setup
```bash
cd ASLA-ai-studio/frontend
npm install
npm run dev
```

#### Backend Setup
```bash
cd ASLA-ai-studio/backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

#### Environment Configuration
Copy `.env.example` to `.env` and add your API keys:
```bash
cp .env.example .env
```

### Development

The application uses a modular architecture with separated concerns:
- **Frontend components** handle UI rendering and user interactions
- **Backend services** contain business logic and AI integrations
- **API routes** mediate between frontend and backend
- **Type definitions** ensure type safety across the stack

### Future Enhancements

- Integrate real AI models (background removal, image generation, LLM)
- Add user authentication and persistent storage
- Implement PostgreSQL database for production
- Add cloud file storage (AWS S3, Google Cloud Storage)
- Integrate with actual job listings APIs
- Add progress tracking and saved items functionality