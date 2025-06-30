# 🔍 NDLens - AI-Powered Image Analysis Template

> **Clean, Organized Application Structure**

NDLens combines Google Lens search capabilities with AI analysis to provide comprehensive insights about images. Upload any image and get detailed analysis powered by Google Lens results and OpenAI.

## 📁 Project Structure

```
openlens-app/
├── 📁 src/                     # Source code
│   ├── main.py                 # FastAPI server
│   ├── config.py               # Configuration
│   ├── selenium_lens_scraper.py
│   ├── bs4_small_scraper.py
│   ├── llm_analysis.py
│   └── secret_key.py
├── 📁 web/                     # Web interface
│   └── index.html              # Beautiful web UI
├── 📁 scripts/                 # Launcher scripts
│   ├── start_openlens_full.py
│   ├── start_openlens_full.bat
│   ├── start_openlens_full.ps1
│   └── start_openlens_full.sh
├── 📁 data/                    # Runtime data
│   ├── csv/                    # Google Lens results
│   ├── txt/                    # Scraped content
│   └── images/                 # Temporary images
├── start.py                    # Main launcher
├── start.bat                   # Windows launcher
├── requirements.txt            # Dependencies
└── README.md                   # This file
```

## 🚀 Quick Start

### Windows (Easiest)
Just double-click:
```
start.bat
```

### Cross-Platform
```bash
python start.py
```

### Manual Launch
```bash
# From openlens-app directory
python scripts/start_openlens_full.py
```

## 🌐 Access Points

Once started, access these URLs:
- **Web Interface**: http://127.0.0.1:3000
- **API Server**: http://127.0.0.1:8000
- **API Documentation**: http://127.0.0.1:8000/docs

## ⚙️ Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Keys
Copy the template and add your API key:
```bash
# Copy the template file
copy src\secret_key_template.py src\secret_key.py
```
Then edit `src/secret_key.py`:
```python
OPENAI_API_KEY = "sk-proj-your-actual-api-key-here"
```

### 3. Start Application
```bash
python start.py
```

## 🔧 Configuration

Edit `src/config.py` to customize:
- **Selenium settings** (headless mode, etc.)
- **Scraping limits** (max URLs, character limits)
- **File paths** (data directories)
- **OpenAI settings** (model, temperature)
- **Analysis prompts**

## 📊 Features

### 🖼️ Image Analysis
- **Upload**: Drag & drop or click to select images
- **Google Lens**: Automatic reverse image search
- **Web Scraping**: Extract content from relevant websites
- **AI Analysis**: GPT-4o-mini powered comprehensive analysis

### 🌟 Modern Web Interface
- **Responsive Design**: Works on desktop and mobile
- **Real-time Updates**: Live progress indicators
- **Beautiful UI**: Modern gradient design
- **File Management**: Preview, info, and easy clearing

### 🔌 API Access
- **RESTful API**: Full programmatic access
- **JSON Responses**: Structured data output
- **CORS Enabled**: Ready for web integration
- **Auto Documentation**: Swagger UI at `/docs`

## 🛠️ Development

### Project Structure Benefits
- **Clean Separation**: Source, web, scripts, and data separated
- **Easy Maintenance**: Each component in its own directory
- **Scalable**: Add new modules without clutter
- **Professional**: Industry-standard organization

### Adding Features
1. **Backend**: Add modules to `src/`
2. **Frontend**: Modify `web/index.html`
3. **Scripts**: Add utilities to `scripts/`
4. **Data**: Output goes to `data/`

### Custom Launchers
The `scripts/` directory contains launchers for different platforms:
- `start_openlens_full.py` - Cross-platform Python launcher
- `start_openlens_full.bat` - Windows batch file
- `start_openlens_full.ps1` - PowerShell script
- `start_openlens_full.sh` - Bash script (Linux/Mac)

## 🔍 How It Works

1. **Image Upload** → Web interface accepts image files
2. **Google Lens** → Selenium scrapes Google Lens results
3. **Web Scraping** → BeautifulSoup extracts content from top results
4. **AI Analysis** → OpenAI analyzes content and generates insights
5. **Results** → Comprehensive analysis returned to user

## 🛑 Stopping the Application

- Press `Ctrl+C` in the terminal
- Close the terminal window
- Use the browser to navigate away

## 🔧 Troubleshooting

### Common Issues

**Python Not Found**
```bash
# Install Python from python.org
# Ensure it's added to PATH
```

**Missing Dependencies**
```bash
pip install -r requirements.txt
```

**Port Already in Use**
```bash
# Kill processes on ports 8000 or 3000
# Or modify ports in scripts/start_openlens_full.py
```

**OpenAI API Key**
```bash
# Copy template and add your key to src/secret_key.py
copy src\secret_key_template.py src\secret_key.py
# Then edit src/secret_key.py with your actual key
OPENAI_API_KEY = "sk-..."
```

## 💡 Tips

- **First Run**: Browser opens automatically to web interface
- **Organized Data**: All temporary files go to `data/` directories
- **Clean Structure**: Easy to navigate and maintain
- **Cross-Platform**: Works on Windows, Linux, and Mac
- **Development Ready**: Easy to extend and modify

## 🏗️ Migration from Old Structure

This organized structure replaces the previous flat file layout:
- All Python modules → `src/`
- Web interface → `web/`
- Launcher scripts → `scripts/`
- Runtime data → `data/`
- Main entry points → Root directory

## 📄 License

This project is part of the OpenLens application suite.

---

**Enjoy using OpenLens!** 🎉

For support or questions, check the main project documentation.
