# 🌐 Fronte### Option 2: Heroku
1.### Option 4: Vercel (Serverless)
1. Install Vercel CLI: `npm i -g vercel`
2. Run `vercel` in your project directory
3. Add environment variable: `OPENAI_API_KEY`
4. Your API will be at: `https://your-project.vercel.app`tall Heroku CLI
2. Run these commands:
```bash
heroku create your-ndlens-api
heroku config:set OPENAI_API_KEY=your_actual_key
git push heroku main
```
3. Your API will be at: `https://your-ndlens-api.herokuapp.com`

### Option 3: DigitalOcean App Platform
1. Go to [DigitalOcean Apps](https://cloud.digitalocean.com/apps)
2. Import from GitHub repository
3. Use the included `.do/app.yaml` configuration  
4. Add environment variable: `OPENAI_API_KEY`
5. Your API will be at: `https://your-app-name.ondigitalocean.app`

### Option 4: Vercel (Serverless)ration Guide

## 🚀 Deploy Your Backend

### Option 1: Render (Recommended - Free Tier)
1. Go to [Render.com](https://render.com)
2. Connect your GitHub repository
3. Use the included `render.yaml` configuration
4. Add environment variable: `OPENAI_API_KEY`
5. Your API will be at: `https://your-app.onrender.com`

### Option 2: Heroku
1. Go to [Render.com](https://render.com)
2. Connect your GitHub repository
3. Use the included `render.yaml` configuration
4. Add environment variable: `OPENAI_API_KEY`
5. Your API will be at: `https://your-app.onrender.com`

### Option 3: Vercel (Serverless)
1. Install Vercel CLI: `npm i -g vercel`
2. Run `vercel` in your project directory
3. Add environment variable: `OPENAI_API_KEY`

## 🔗 Frontend Integration

### API Endpoint
Your deployed backend will have one main endpoint:

```
POST https://your-api-domain.com/analyze
```

### Request Format
```javascript
const analyzeImage = async (imageFile) => {
  // Convert image to base64
  const base64Image = await convertToBase64(imageFile);
  
  const response = await fetch('https://your-api-domain.com/analyze', {
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

// Helper function to convert file to base64
const convertToBase64 = (file) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = error => reject(error);
  });
};
```

### Response Format
```javascript
{
  "analysis": "Detailed AI analysis of the image...",
  "request_id": "uuid-string",
  "google_lens_links_found": 10,
  "scraped_content_length": 5000,
  "csv_file": "csv/results_uuid.csv",
  "content_file": "txt/content_uuid.txt"
}
```

## 🖥️ Example React Component

```jsx
import React, { useState } from 'react';

const ImageAnalyzer = () => {
  const [analysis, setAnalysis] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleImageUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setLoading(true);
    setError('');
    
    try {
      // Convert to base64
      const base64 = await convertToBase64(file);
      const base64Data = base64.split(',')[1];

      // Send to your deployed API
      const response = await fetch('https://your-api-domain.com/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          image: base64Data
        })
      });

      if (!response.ok) {
        throw new Error('Analysis failed');
      }

      const result = await response.json();
      setAnalysis(result.analysis);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const convertToBase64 = (file) => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => resolve(reader.result);
      reader.onerror = error => reject(error);
    });
  };

  return (
    <div className="image-analyzer">
      <h2>AI Image Analysis</h2>
      
      <input
        type="file"
        accept="image/*"
        onChange={handleImageUpload}
        disabled={loading}
      />
      
      {loading && <p>Analyzing image...</p>}
      {error && <p style={{color: 'red'}}>Error: {error}</p>}
      
      {analysis && (
        <div className="analysis-result">
          <h3>Analysis Result:</h3>
          <p>{analysis}</p>
        </div>
      )}
    </div>
  );
};

export default ImageAnalyzer;
```

## 🔧 Netlify Configuration

For your Netlify frontend, add these environment variables in your Netlify dashboard:

```
REACT_APP_API_URL=https://your-api-domain.com
```

Then use it in your code:
```javascript
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const response = await fetch(`${API_URL}/analyze`, {
  // ... rest of your fetch configuration
});
```

## 🚦 CORS Configuration

The backend already includes CORS headers that allow all origins, so your Netlify frontend should work without issues.

## 📱 Error Handling

Handle common scenarios:
- **Network errors**: API is down
- **400 errors**: Invalid image format
- **500 errors**: Processing failed
- **Timeout**: Large images may take time

```javascript
const analyzeWithRetry = async (imageFile, maxRetries = 3) => {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await analyzeImage(imageFile);
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)));
    }
  }
};
```

## 🔒 Security Notes

- Your OpenAI API key is stored securely on the backend
- Frontend only sends base64 image data
- No sensitive information exposed to client
- Rate limiting recommended for production

## 📊 Performance Tips

- **Image optimization**: Resize large images before sending
- **Loading states**: Show progress indicators
- **Caching**: Consider caching results by image hash
- **Error boundaries**: Wrap components in error boundaries

Your frontend is now ready to integrate with the NDLens backend! 🎉
