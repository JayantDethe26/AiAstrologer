# 🌟 RashiVerse - AI-Powered Astrology Reading Platform

## ✨ Overview

RashiVerse is a sophisticated AI-powered astrology platform that generates personalized horoscope readings using Google's Gemini AI. The platform combines traditional astrological wisdom with modern AI capabilities to provide users with detailed, personalized cosmic insights based on their birth details and specific questions.

### 🔮 Key Features

- **Personalized Readings**: Generate unique astrology readings based on birth date, time, location, and personal questions
- **Advanced AI Integration**: Powered by Google Gemini 2.0 Flash for intelligent, contextual responses
- **Beautiful UI**: Cosmic-themed interface with animations, particle effects, and responsive design
- **Zodiac Intelligence**: Accurate zodiac sign calculation with detail
ed characteristics
- **Multiple Reading Styles**: 4 different AI prompt styles for varied reading approaches
- **Export Functionality**: Save and share readings in multiple formats
- **Life Stage Analysis**: Contextual readings based on astrological life phases
- **Real-time Processing**: Dynamic loading animations and cosmic particle effects

## 🚀 Technology Stack

- **Backend**: Flask (Python)
- **AI Engine**: Google Gemini 2.0 Flash
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: Bootstrap 5, Custom CSS with animations
- **Icons**: Font Awesome 6
- **Fonts**: Google Fonts (Cinzel, Poppins)
- **Containerization**: Docker & Docker Compose

## 📋 Prerequisites

- Python 3.8 or higher
- Google Gemini API key
- Docker (optional, for containerized deployment)
- Modern web browser with JavaScript enabled

## 🛠️ Installation & Setup

### Method 1: Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/JayantDethe26/AiAstrologer.git
   cd rashiverse
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Create .env file
   echo "GEMINI_API_KEY=your-google-gemini-api-key" > .env
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

### Method 2: Docker Deployment

1. **Clone and navigate to project**
   ```bash
   git clone https://github.com/JayantDethe26/AiAstrologer.git
   cd rashiverse
   ```

2. **Create environment file**
   ```bash
   echo "GEMINI_API_KEY=your-google-gemini-api-key" > .env
   ```

3. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

## 🐳 Docker Configuration

### Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
ENV FLASK_ENV=production

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  rashiverse:
    build: .
    ports:
      - "5000:5000"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
    volumes:
      - ./templates:/app/templates
      - ./static:/app/static
    restart: unless-stopped
    
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - rashiverse
    restart: unless-stopped
```

## 📁 Project Structure

```
rashiverse/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose setup
├── .env
├── templates/
│   └── index.html       # Main HTML template
└── README.md
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Required
GEMINI_API_KEY=your-google-gemini-api-key-here

# Optional
FLASK_ENV=production
FLASK_DEBUG=False
PORT=5000
HOST=0.0.0.0
```

### API Configuration

The application uses Google Gemini 2.0 Flash with optimized settings:

```python
generation_config = genai.types.GenerationConfig(
    temperature=0.9,        
    top_p=0.85,            
    top_k=35,              
    max_output_tokens=450,
    candidate_count=1      
)
```

## 🎯 API Endpoints

### Main Endpoints

- `GET /` - Main application interface
- `POST /result` - Generate astrology reading (form submission)
- `POST /api/reading` - Generate reading (JSON API)

### API Usage Example

```javascript
// POST /api/reading
{
  "name": "John Doe",
  "dob": "1990-05-15",
  "tob": "14:30",
  "pob": "New York, USA",
  "question": "What does my career future hold?"
}

// Response
{
  "success": true,
  "reading": {
    "name": "John Doe",
    "zodiac_sign": {
      "name": "Taurus",
      "symbol": "♉",
      "full": "Taurus ♉"
    },
    "cosmic_guidance": "Detailed AI-generated reading...",
    "life_stage": "first Saturn return approach - foundational years"
  }
}
```

## 🌟 Features Deep Dive

### Zodiac Calculation Engine
- Accurate sun sign calculation based on birth date
- Support for all 12 zodiac signs with symbols and traits
- Life stage analysis based on astrological cycles

### AI Reading Generation
- 4 specialized prompt templates for different reading styles
- Personalized context creation based on user data
- Question categorization for targeted responses
- Fallback reading system for error handling

### User Interface
- Cosmic-themed design with animated backgrounds
- Particle effects and floating elements
- Responsive design for all devices
- Progressive loading with cosmic messaging
- Export and sharing functionality

## 🧪 Testing

Run the test suite:

```bash
# Install test dependencies
pip install pytest pytest-flask

# Run tests
pytest tests/

# Run with coverage
pytest --cov=app tests/
```

### Test Coverage
- Zodiac calculation accuracy
- API endpoint functionality
- Error handling scenarios
- Reading generation quality

## 🚀 Deployment

### Production Deployment

1. **Using Docker (Recommended)**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

2. **Traditional Deployment**
   ```bash
   # Install production server
   pip install gunicorn
   
   # Run with Gunicorn
   gunicorn --bind 0.0.0.0:5000 --workers 4 app:app
   ```

3. **Cloud Deployment**
   - **Heroku**: Use provided `Procfile`
   - **AWS ECS**: Use Docker configuration
   - **Google Cloud Run**: Deploy with Docker
   - **Azure Container Instances**: Use container setup

### Performance Optimizations

- Gunicorn with multiple workers
- Nginx reverse proxy for static files
- API response caching
- Optimized AI generation parameters
- Compressed static assets

## 🔐 Security Considerations

- Environment variable protection for API keys
- Input validation and sanitization
- Rate limiting for API endpoints
- CORS configuration for cross-origin requests
- Secure headers implementation

## 📈 Monitoring & Analytics

### Health Check Endpoint
```python
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'timestamp': datetime.now().isoformat()}
```

### Logging Configuration
```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guide
- Add docstrings to all functions
- Include tests for new features
- Update documentation as needed

## 🐛 Troubleshooting

### Common Issues

1. **API Key Issues**
   ```bash
   Error: Invalid API key
   Solution: Verify your GEMINI_API_KEY in .env file
   ```

2. **Port Already in Use**
   ```bash
   Error: Port 5000 is already in use
   Solution: Change port in app.py or kill existing process
   ```

3. **Docker Build Issues**
   ```bash
   Solution: Clear Docker cache with docker system prune
   ```

### Debug Mode
```python
# Enable debug mode for development
export FLASK_DEBUG=1
python app.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Gemini AI for powerful text generation
- Bootstrap team for responsive framework
- Font Awesome for beautiful icons
- Astrological community for traditional wisdom
- Open source contributors

## 📞 Support

- 📧 Email: dethe@gmail.com

## 🔮 Future Enhancements

- [ ] Multi-language support
- [ ] User accounts and reading history
- [ ] Advanced birth chart calculations
- [ ] Real-time astrological updates
- [ ] Mobile app development
- [ ] Voice-powered readings
- [ ] Integration with calendar systems
- [ ] Compatibility analysis features

---

<div align="center">
  <p><strong>Made with ❤️ and ✨ cosmic energy</strong></p>
  <p><em>The stars guide but never command. Trust your intuition.</em></p>
</div>