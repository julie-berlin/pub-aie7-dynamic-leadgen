# pub-aie7-dynamic-leadgen

## 🚀 Quick Start with Docker

### Prerequisites
- Docker and Docker Compose installed
- OpenAI API key
- Supabase account with project credentials

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd pub-aie7-dynamic-surveys
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   # Edit .env and add:
   # - OPENAI_API_KEY
   # - SUPABASE_URL
   # - SUPABASE_PUBLISHABLE_KEY
   # - SUPABASE_SECRET_KEY
   ```

3. **Start all services**
   ```bash
   docker-compose up
   ```

   This will start:
   - Redis cache (port 6379)
   - FastAPI backend (port 8000) - connected to Supabase
   - React form frontend (port 5173)
   - React admin frontend (port 5174)

4. **Access the application**
   - Form App: http://localhost:5173
   - Admin App: http://localhost:5174/admin/
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Docker Commands

```bash
# Start services in background
docker-compose up -d

# View logs
docker-compose logs -f [service-name]

# Stop all services
docker-compose down

# Stop and remove volumes (clean database)
docker-compose down -v

# Rebuild after code changes
docker-compose build
docker-compose up

# Rebuild specific service
docker-compose build admin
docker-compose up admin
```

### Production Deployment

For production deployment, use the production docker-compose file:

```bash
# Copy production environment file
cp .env .env
# Edit .env with production credentials

# Build and start production services
docker-compose -f docker-compose.prod.yml up -d

# This will start:
# - Backend API with production settings
# - Form frontend served by nginx on port 3000
# - Admin frontend served by nginx on port 3001
# - Redis with persistence
# - Nginx reverse proxy on ports 80/443
```

Production URLs (with nginx proxy):
- Form App: http://your-domain.com/
- Admin App: http://your-domain.com/admin/
- API: http://your-domain.com/api/

### Available Test Forms
The Supabase database should be populated with 5 example business scenarios. Test with these form IDs:
- `f1111111-1111-1111-1111-111111111111` - Pawsome Dog Walking
- `f2222222-2222-2222-2222-222222222222` - Metro Realty Group
- `f3333333-3333-3333-3333-333333333333` - TechSolve Consulting
- `f4444444-4444-4444-4444-444444444444` - FitLife Personal Training
- `f5555555-5555-5555-5555-555555555555` - Sparkle Clean Solutions

## ✅ Problem Worth Solving

Businesses spend time customizing multi-step forms and still fail to capture quality leads. Most lead gen funnels are static, hard to personalize, and high-friction. Users either abandon them mid-way or provide low-quality responses.

One traditional way of capturing leads for your business is a lead generation form. Often this is a multi-step form where the prospect answers a series of questions. The answers they provide are used to help qualify them. These "funnels" are difficult to get right and often marketers must make multiple, customized versions to suit each audience and keep them engaged.

What if we leveraged the power of LLMs to vary the questions according to the type of visitor and their answers? We used an LLM to score the lead along the way and ask more questions if the user stays engaged. All of this information is then combined to personalize their messages.

## 🧠 Potential LLM Solution

An LLM-powered form agent that:

- Conversationally adapts to user responses in real time
- Chooses the most relevant next question(s) from a marketer-defined set
- Rephrases and styles questions to suit the user's tone and personality
- Applies persuasion techniques to reduce abandonment and increase truthfulness
- Scores responses against a rubric to qualify leads
- Auto-generates personalized responses, final-page CTAs, and follow-up emails
- Helps the business design the form funnel from scratch, using branding and service info

## 🎯 Target Audience

- Small to medium businesses (SMBs)
- Solo marketers or growth hackers
- Agencies that build web funnels for clients

## 📏 Key Metrics

- Form completion rate
- Lead quality score (as judged by conversion or post-funnel behavior)
- Time to create a working funnel
- Follow-up email open and reply rate

## 📚 Data Sources for RAG and Fine-Tuning

- Background info from the business (e.g. service details, tone, offers)
- Query parameters from the incoming request provides information about the source and campaign
- Question set + required flags + qualification rubric (provided by marketer)
- Conversational UX patterns from high-converting chatbot scripts (could be used to fine-tune)
- Optionally, pre-built industry-specific funnel templates to bootstrap marketers

## Selected Brand Name: Varyq

Domain name available and captures the essence of the idea.
