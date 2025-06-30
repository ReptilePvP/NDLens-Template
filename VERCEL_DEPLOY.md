# 🚀 Vercel Deployment Guide for NDLens

## Prerequisites
- [Vercel account](https://vercel.com)
- [Vercel CLI](https://vercel.com/cli) installed: `npm i -g vercel`
- OpenAI API key

## 🎯 Quick Deploy

### Option 1: GitHub Integration (Recommended)
1. Push your code to GitHub (already done!)
2. Go to [Vercel Dashboard](https://vercel.com/dashboard)
3. Click "New Project"
4. Import `ReptilePvP/NDLens-Template`
5. Vercel will auto-detect the configuration
6. Add environment variable: `OPENAI_API_KEY`
7. Deploy!

### Option 2: CLI Deployment
```bash
# Install Vercel CLI
npm i -g vercel

# Navigate to your project
cd n:\openlens-app

# Login to Vercel
vercel login

# Deploy
vercel

# Add environment variable
vercel env add OPENAI_API_KEY

# Redeploy with environment variable
vercel --prod
```

## ⚙️ Environment Variables

In your Vercel dashboard, add:
- **Key**: `OPENAI_API_KEY`
- **Value**: `sk-proj-your-actual-api-key`
- **Target**: Production, Preview, Development

## 🔗 Your API Endpoints

After deployment, your API will be available at:
```
https://your-project-name.vercel.app/
https://your-project-name.vercel.app/analyze
https://your-project-name.vercel.app/docs  (API documentation)
```

## 🌐 Frontend Integration

### For your Netlify frontend:

```javascript
// Use your Vercel URL
const API_URL = 'https://your-project-name.vercel.app';

const analyzeImage = async (imageFile) => {
  // Convert image to base64
  const base64Image = await convertToBase64(imageFile);
  
  const response = await fetch(`${API_URL}/analyze`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      image: base64Image.split(',')[1] // Remove data:image/jpeg;base64, prefix
    })
  });
  
  const result = await response.json();
  return result;
};

// Helper function
const convertToBase64 = (file) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = error => reject(error);
  });
};
```

### Environment Variables for Netlify

In your Netlify dashboard, add:
```
REACT_APP_API_URL=https://your-project-name.vercel.app
```

## 🔧 Configuration Files

The following files are already configured for Vercel:

### `vercel.json`
```json
{
  "version": 2,
  "builds": [
    {
      "src": "src/main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "src/main.py"
    }
  ],
  "functions": {
    "src/main.py": {
      "runtime": "python3.9",
      "maxDuration": 60
    }
  },
  "env": {
    "OPENAI_API_KEY": "@openai-api-key"
  }
}
```

## 🚨 Important Notes

### Serverless Limitations
- **60-second timeout**: Perfect for image analysis
- **Cold starts**: First request may be slower
- **File system**: Read-only except `/tmp`
- **Memory**: 1GB limit

### File Handling
The app automatically handles temporary files in `/tmp` directory, which is perfect for Vercel's serverless environment.

## 🐛 Troubleshooting

### Common Issues

**Build Fails**
```bash
# Check your requirements.txt
pip install -r requirements.txt
```

**API Key Not Found**
```bash
# Make sure environment variable is set in Vercel dashboard
vercel env ls
```

**CORS Issues**
The app includes CORS headers for all origins, so your Netlify frontend should work without issues.

**Function Timeout**
Large images may timeout. Consider:
- Resizing images on frontend before sending
- Using streaming responses
- Upgrading to Vercel Pro for longer timeouts

## 📊 Monitoring

### Vercel Dashboard
- View function logs
- Monitor performance
- Check error rates
- See deployment history

### API Health Check
```bash
curl https://your-project-name.vercel.app/
```

Should return:
```json
{
  "message": "Google Lens Scraper API is running. Use /analyze endpoint with a base64 encoded image."
}
```

## 🎉 You're Done!

Your NDLens API is now deployed on Vercel and ready to integrate with your Netlify frontend!

Next steps:
1. Test the API endpoints
2. Update your frontend to use the Vercel URL
3. Deploy your Netlify frontend
4. Enjoy your AI-powered image analysis app!
