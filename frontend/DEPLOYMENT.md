# Frontend Deployment Guide - Vercel

This guide covers deploying the Todo App frontend to Vercel.

## Prerequisites

- [Vercel Account](https://vercel.com/signup) (free tier works)
- Backend API deployed and accessible (provide URL)
- GitHub repository access

## Quick Deploy (Recommended)

### Option 1: Deploy via Vercel Dashboard

1. **Go to Vercel Dashboard**
   - Visit https://vercel.com/new
   - Sign in with GitHub

2. **Import Git Repository**
   - Click "Add New" → "Project"
   - Select your GitHub repository: `MHassaanQureshi/hackathon-2`
   - Vercel will auto-detect Next.js

3. **Configure Project**
   - **Framework Preset:** Next.js (auto-detected)
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build` (auto-filled)
   - **Output Directory:** `.next` (auto-filled)
   - **Install Command:** `npm install` (auto-filled)

4. **Set Environment Variables**
   Click "Environment Variables" and add:
   ```
   Key: NEXT_PUBLIC_API_URL
   Value: https://your-backend-api.com/api/v1
   ```
   ```
   Key: NEXT_PUBLIC_APP_NAME
   Value: Todo App
   ```

5. **Deploy**
   - Click "Deploy"
   - Wait 2-3 minutes for build to complete
   - Your app will be live at: `https://your-project.vercel.app`

### Option 2: Deploy via Vercel CLI

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Navigate to Frontend Directory**
   ```bash
   cd frontend
   ```

3. **Login to Vercel**
   ```bash
   vercel login
   ```

4. **Deploy**
   ```bash
   vercel
   ```
   - Follow the prompts
   - Set up project settings
   - Add environment variables when prompted

5. **Deploy to Production**
   ```bash
   vercel --prod
   ```

## Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API base URL | `https://api.example.com/api/v1` |
| `NEXT_PUBLIC_APP_NAME` | Application name | `Todo App` |

### Setting Environment Variables

**Via Vercel Dashboard:**
1. Go to Project Settings → Environment Variables
2. Add each variable with appropriate values
3. Select environments: Production, Preview, Development
4. Save and redeploy

**Via CLI:**
```bash
vercel env add NEXT_PUBLIC_API_URL
# Enter value when prompted
```

## Backend Configuration

⚠️ **Important:** Your backend must be configured to accept requests from your Vercel domain.

**Update backend CORS settings:**

In `backend/app/main.py`, add your Vercel URL to allowed origins:
```python
origins = [
    "http://localhost:3000",
    "https://your-project.vercel.app",  # Add your Vercel URL
    "https://your-custom-domain.com",   # Add custom domain if any
]
```

## Custom Domain (Optional)

1. Go to Project Settings → Domains
2. Add your custom domain
3. Configure DNS records as instructed
4. Update backend CORS settings

## Build & Deploy Process

Vercel automatically:
1. Detects Next.js framework
2. Installs dependencies (`npm install`)
3. Runs build command (`npm run build`)
4. Deploys to global CDN
5. Provides HTTPS by default

## Performance Optimizations

✅ **Already Configured:**
- SWC Minification enabled
- Compression enabled
- React Strict Mode
- Static optimization
- Image optimization ready

## Monitoring & Logs

**View Deployment Logs:**
1. Go to Vercel Dashboard → Deployments
2. Click on a deployment
3. View build logs and runtime logs

**Analytics (Optional):**
- Enable Vercel Analytics in Project Settings
- Free tier includes basic analytics

## Troubleshooting

### Build Fails

**Error: "Module not found"**
- Solution: Check `package.json` dependencies
- Run `npm install` locally to verify

**Error: "Environment variable not set"**
- Solution: Add missing variables in Vercel dashboard
- Redeploy after adding variables

### Runtime Issues

**Error: "Failed to fetch"**
- Check `NEXT_PUBLIC_API_URL` is correct
- Verify backend CORS settings
- Check browser console for errors

**Error: "Unauthorized" on API calls**
- Verify JWT token storage (localStorage)
- Check token expiration (24 hours)

### CORS Errors

- Add Vercel URL to backend CORS origins
- Restart backend after CORS changes
- Clear browser cache and try again

## Deployment Checklist

Before deploying, ensure:

- [ ] Backend API is deployed and accessible
- [ ] Environment variables are configured
- [ ] Backend CORS includes frontend URL
- [ ] `npm run build` works locally
- [ ] All environment-specific settings updated
- [ ] .env.production file configured

## Local Testing Before Deploy

```bash
cd frontend

# Install dependencies
npm install

# Create production build
npm run build

# Test production build locally
npm start

# Open http://localhost:3000
```

## Automatic Deployments

Vercel automatically deploys:
- **Production:** Commits to `main` branch
- **Preview:** Pull requests and other branches

Each deployment gets a unique URL for testing.

## Rollback

If a deployment fails:
1. Go to Vercel Dashboard → Deployments
2. Find a previous working deployment
3. Click "..." → "Promote to Production"

## Support

- [Vercel Documentation](https://vercel.com/docs)
- [Next.js Deployment](https://nextjs.org/docs/deployment)
- [Vercel Support](https://vercel.com/support)

## Cost

- **Free Tier:** Perfect for this project
  - Unlimited deployments
  - Automatic HTTPS
  - Global CDN
  - 100GB bandwidth/month

## Next Steps After Deployment

1. Test all features on production URL
2. Update README with production URL
3. Share app with users
4. Monitor performance and errors
5. Set up custom domain (optional)

---

**Your frontend is now Vercel deployment-ready!** 🚀
