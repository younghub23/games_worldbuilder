# DEVELOPMENT SETUP GUIDE
## Get Started Building Empire Genesis

---

## PREREQUISITES

### Required Software

**For Unity Development:**
- [ ] Unity Hub (latest version)
- [ ] Unity 2022.3 LTS
- [ ] Visual Studio Code or JetBrains Rider
- [ ] Git with LFS
- [ ] Xcode 14+ (Mac only, for iOS builds)

**For Backend Development:**
- [ ] Node.js 18+ and npm
- [ ] PostgreSQL 14+
- [ ] Redis 7+
- [ ] Docker & Docker Compose (recommended)
- [ ] Postman or Insomnia (API testing)

**For iOS Native:**
- [ ] Xcode 14+
- [ ] CocoaPods
- [ ] macOS 12+ (required for iOS development)

###Apple Developer Account
- [ ] Apple Developer Program ($99/year) - required for App Store deployment
- [ ] Sign in with Apple configured
- [ ] Push notification certificates

---

## QUICK START (5 Minutes)

### 1. Clone Repository
```bash
git clone <repository-url>
cd games_worldbuilder
```

### 2. Install Dependencies

**Backend:**
```bash
cd backend
npm install
cp .env.example .env
# Edit .env with your database credentials
```

**Unity:**
```bash
# Open Unity Hub
# Click "Add" → Select "unity-project" folder
# Unity will import packages automatically
```

### 3. Start Development Servers

**Backend:**
```bash
cd backend
docker-compose up -d  # Start PostgreSQL + Redis
npm run dev           # Start API server (port 3000)
```

**Unity:**
```bash
# Open Unity project in Unity Hub
# Press Play to run in editor
```

---

## DETAILED SETUP

### Unity Project Setup

**1. Create New Project:**
```bash
# Via Unity Hub:
1. Open Unity Hub
2. Click "New Project"
3. Template: "2D Core" or "3D Core"
4. Name: EmpireGenesis
5. Location: ./unity-project
6. Unity Version: 2022.3 LTS
```

**2. Install Required Packages:**

Open Package Manager (Window → Package Manager):
- [ ] Newtonsoft Json (com.unity.nuget.newtonsoft-json)
- [ ] DOTween (Asset Store - free)
- [ ] Unity IAP
- [ ] Unity Analytics
- [ ] Unity Ads (optional)
- [ ] TextMeshPro

**3. Configure Project Settings:**

```
Edit → Project Settings:

Player:
- Company Name: [Your Company]
- Product Name: Empire Genesis
- Bundle Identifier: com.[company].empiregenesis
- Version: 0.1.0
- Minimum iOS Version: 13.0
- Target Devices: iPhone + iPad
- Orientation: Landscape or Auto Rotation

Graphics:
- Color Space: Linear
- Graphics API: Metal (iOS)
- Auto Graphics API: No

Quality:
- Anti Aliasing: 4x Multi Sampling
- Shadow Resolution: Medium
- Shadow Distance: 75

Other Settings:
- Scripting Backend: IL2CPP
- API Compatibility Level: .NET Standard 2.1
- Managed Stripping Level: Medium
```

**4. Folder Structure:**

```bash
unity-project/
├── Assets/
│   ├── _Project/           # Our game files
│   ├── Plugins/            # Native plugins
│   ├── Resources/          # Runtime assets
│   ├── StreamingAssets/    # Config files
│   └── TextMesh Pro/       # Auto-installed
├── Packages/
├── ProjectSettings/
└── UserSettings/
```

---

### Backend Setup

**1. Initialize Node.js Project:**

```bash
cd backend
npm init -y

# Install dependencies
npm install express cors helmet morgan
npm install dotenv jsonwebtoken bcryptjs
npm install pg redis socket.io
npm install joi                    # Validation
npm install winston                # Logging

# Dev dependencies
npm install --save-dev nodemon typescript @types/node
npm install --save-dev @types/express jest supertest
```

**2. Database Setup:**

```bash
# Start PostgreSQL (Docker)
docker run --name empiregenesis-db \
  -e POSTGRES_PASSWORD=devpassword \
  -e POSTGRES_DB=empiregenesis \
  -p 5432:5432 \
  -d postgres:14

# Or use docker-compose (see backend/docker-compose.yml)
docker-compose up -d
```

**3. Run Migrations:**

```bash
cd backend
npm run migrate:up

# Seed initial data (game buildings, heroes, etc.)
npm run seed
```

**4. Environment Variables:**

Create `backend/.env`:
```env
NODE_ENV=development
PORT=3000

# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=empiregenesis
DB_USER=postgres
DB_PASSWORD=devpassword

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# JWT
JWT_SECRET=your-super-secret-key-change-in-production
JWT_EXPIRES_IN=7d

# Apple IAP
APPLE_SHARED_SECRET=your-apple-shared-secret

# Firebase (Push notifications)
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_PRIVATE_KEY=your-private-key
FIREBASE_CLIENT_EMAIL=your-client-email
```

**5. Start Server:**

```bash
npm run dev
# Server running on http://localhost:3000
```

**6. Verify Setup:**

```bash
curl http://localhost:3000/api/v1/health
# Should return: {"status": "ok", "timestamp": "..."}
```

---

### iOS Native Plugin Setup

**1. Create iOS Plugin:**

```bash
cd ios-native
pod init

# Edit Podfile:
platform :ios, '13.0'

target 'EmpireGenesisBridge' do
  use_frameworks!

  pod 'Firebase/Analytics'
  pod 'Firebase/Messaging'
end

pod install
```

**2. Build Plugin:**

```bash
xcodebuild -workspace EmpireGenesisBridge.xcworkspace \
           -scheme EmpireGenesisBridge \
           -sdk iphoneos \
           -configuration Release \
           build

# Copy .framework to Unity project
cp -R build/Release-iphoneos/EmpireGenesisBridge.framework \
   ../unity-project/Assets/Plugins/iOS/
```

---

## DEVELOPMENT WORKFLOW

### Daily Development

**1. Start Backend:**
```bash
cd backend
docker-compose up -d
npm run dev
```

**2. Open Unity:**
```bash
# Open Unity Hub → Open Project → EmpireGenesis
# Press Play in editor
```

**3. Hot Reload (Backend):**
- Backend auto-reloads on file changes (nodemon)
- Unity requires manual play after code changes

### Testing

**Backend Unit Tests:**
```bash
cd backend
npm test                  # Run all tests
npm test -- --watch       # Watch mode
npm run test:coverage     # Coverage report
```

**Unity Play Mode Tests:**
```bash
# In Unity:
# Window → General → Test Runner
# PlayMode tab → Run All
```

### Building for iOS

**1. Build from Unity:**
```
File → Build Settings
- Platform: iOS
- Switch Platform
- Player Settings:
  - Bundle Identifier: com.[company].empiregenesis
  - Signing Team: [Your Apple Developer Team]
- Build

# Unity creates Xcode project in /Build/iOS
```

**2. Open in Xcode:**
```bash
cd Build/iOS
open Unity-iPhone.xcodeproj
```

**3. Configure Signing:**
```
Xcode → Project Settings → Signing & Capabilities
- Team: [Your Apple Developer Team]
- Bundle Identifier: com.[company].empiregenesis
- Automatically manage signing: ✓
```

**4. Build & Run:**
```bash
# Connect iPhone via USB
# Xcode → Product → Run (⌘+R)
# Or build for simulator
```

### TestFlight Deployment

**1. Archive Build:**
```
Xcode → Product → Archive
# Wait for build (5-15 minutes)
```

**2. Upload to App Store Connect:**
```
Window → Organizer → Archives
- Select your build
- Click "Distribute App"
- Method: App Store Connect
- Upload
```

**3. Add to TestFlight:**
```
App Store Connect → TestFlight
- Select build
- Add external testers (up to 10,000)
```

---

## TROUBLESHOOTING

### Unity Issues

**"Assembly not found" errors:**
```bash
# Delete Library folder, restart Unity
rm -rf Library/
# Unity will reimport everything
```

**iOS build fails:**
```bash
# Check Xcode version (must be 14+)
xcodebuild -version

# Update CocoaPods
sudo gem install cocoapods
pod repo update
```

### Backend Issues

**Database connection fails:**
```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# Restart container
docker-compose restart postgres
```

**Port 3000 already in use:**
```bash
# Find process using port 3000
lsof -ti:3000

# Kill process
kill -9 $(lsof -ti:3000)
```

### iOS Issues

**Code signing error:**
```
1. Xcode → Preferences → Accounts
2. Add Apple ID
3. Download Manual Profiles
4. Project Settings → Signing → Select Team
```

**"Provisioning profile doesn't include signing certificate":**
```
1. Revoke old certificates in Apple Developer Portal
2. Delete all provisioning profiles
3. Xcode → Preferences → Accounts → Download Manual Profiles
4. Clean build folder (⇧⌘K)
5. Rebuild
```

---

## RECOMMENDED VS CODE EXTENSIONS

```json
{
  "recommendations": [
    "ms-dotnettools.csharp",              // C# for Unity
    "unity.unity-debug",                   // Unity debugger
    "kleber-swf.unity-code-snippets",     // Unity snippets
    "dbaeumer.vscode-eslint",             // ESLint for backend
    "esbenp.prettier-vscode",             // Code formatter
    "ms-vscode.vscode-typescript-next",   // TypeScript
    "bradlc.vscode-tailwindcss",          // CSS (if using web admin)
    "eamodio.gitlens"                     // Git enhanced
  ]
}
```

---

## GIT WORKFLOW

**Branch Strategy:**
```
main                    # Production-ready
├── develop             # Integration branch
├── feature/grid-system
├── feature/buildings
└── bugfix/resource-overflow
```

**Commit Messages:**
```
feat: Add building placement system
fix: Resolve resource calculation bug
docs: Update API documentation
refactor: Optimize grid rendering
test: Add unit tests for HeroManager
```

**Pull Request Process:**
1. Create feature branch
2. Implement feature
3. Write tests
4. Create PR to `develop`
5. Code review
6. Merge to `develop`
7. Periodic merge `develop` → `main` for releases

---

## NEXT STEPS

1. **Complete Setup:** Check off all prerequisites above
2. **Run Sample Project:** Verify Unity and backend work
3. **Read Architecture:** Review IOS_DEVELOPMENT_PLAN.md
4. **Start Sprint 1:** Begin with MVP_SPRINT_PLAN.md
5. **Daily Standups:** Track progress, blockers

**Questions? Check documentation in `/docs` or create GitHub issue.**

---

## USEFUL COMMANDS CHEAT SHEET

```bash
# Unity
# (All in Unity Editor, no CLI)

# Backend
npm run dev                 # Start dev server
npm test                    # Run tests
npm run migrate:up          # Run migrations
npm run migrate:down        # Rollback migrations
npm run seed                # Seed database

# Docker
docker-compose up -d        # Start all services
docker-compose down         # Stop all services
docker-compose logs -f      # Follow logs
docker-compose restart      # Restart services

# iOS
xcodebuild -list            # List schemes
xcodebuild clean            # Clean build
pod install                 # Install CocoaPods dependencies

# Git
git checkout -b feature/x   # Create branch
git add .                   # Stage changes
git commit -m "message"     # Commit
git push origin branch      # Push to remote
```

---

**Ready to build? Start with [MVP_SPRINT_PLAN.md](MVP_SPRINT_PLAN.md)!**
