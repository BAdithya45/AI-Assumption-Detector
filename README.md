# Assumption Detector

A full-stack AI application that uncovers hidden assumptions in text, helping you make better decisions by identifying risks and providing validation suggestions.

## Live Demo

🔗 **[Live Application]([https://your-app.vercel.app](https://github.com/BAdithya45/AI-Assumption-Detector.git))**

## Features

- **Assumption Detection**: Analyzes text to find implicit assumptions
- **Risk Assessment**: Categorizes assumptions as low, medium, or high risk
- **Confidence Scoring**: Shows how confident the AI is about each assumption
- **Validation Suggestions**: Provides actionable ways to verify each assumption
- **Clean UX**: Modern dark theme with smooth interactions

## Tech Stack

**Frontend**
- Vanilla HTML/CSS/JS
- Inter font family
- Responsive design

**Backend**
- FastAPI (Python)
- OpenRouter API for model inference
- Serverless deployment on Vercel

**Model**
- Google Gemma 3 1B (free tier via OpenRouter)

## Local Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/assumption-detector.git
cd assumption-detector
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set environment variables:
```bash
export OPENROUTER_API_KEY=your_key_here
```

5. Run the server:
```bash
uvicorn api:app --reload
```

6. Open http://localhost:8000

## Deployment on Vercel

1. Push your code to GitHub
2. Go to https://vercel.com
3. Import your GitHub repository
4. Add Environment Variable: `OPENROUTER_API_KEY`
5. Deploy

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Serves the frontend |
| GET | `/health` | Health check |
| POST | `/analyze` | Analyze text for assumptions |

### Example Request

```bash
curl -X POST "https://your-app.vercel.app/analyze" \
  -H "Content-Type: application/json" \
  -d '{"text": "We can launch next month if the team stays focused."}'
```

### Example Response

```json
{
  "assumptions": [
    {
      "text": "The team has the capacity to stay focused",
      "risk": "medium",
      "confidence": 0.85,
      "explanation": "Team focus depends on workload, morale, and external factors",
      "validation": "Check current sprint commitments and team availability"
    }
  ],
  "summary": "Found 1 assumption related to team capacity and timeline."
}
```

## Project Structure

```
├── api.py              # FastAPI application
├── agent.py            # AI agent logic
├── schemas.py          # Pydantic models
├── prompts.py          # System prompts
├── openrouterclient.py # OpenRouter HTTP client
├── vercel.json         # Vercel configuration
├── static/
│   ├── index.html      # Frontend HTML
│   ├── styles.css      # Styles
│   └── app.js          # Frontend JavaScript
├── requirements.txt    # Python dependencies
└── README.md
```

## License

MIT
