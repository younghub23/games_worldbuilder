# Quick Start Guide: Building Empire Genesis with Claude Code

This guide will get you from zero to running game in under 30 minutes.

## Prerequisites Check

Before starting, ensure you have:
- ✅ macOS or Windows PC
- ✅ Unity Hub installed
- ✅ Unity 2022.3 LTS installed via Unity Hub
- ✅ Xcode installed (macOS only, for iOS builds)
- ✅ Node.js 18+ installed
- ✅ Docker Desktop installed (for local database)
- ✅ Git configured

## Step 1: Open Unity Project (5 minutes)

### In Unity Hub:
1. Click **"Add"** → **"Add project from disk"**
2. Navigate to: `/home/user/games_worldbuilder/unity-project`
3. Select the folder and click **"Add Project"**
4. Click on the project to open it in Unity Editor

**First-time open will take 3-5 minutes** as Unity imports assets and compiles scripts.

### Verify Setup:
Once Unity opens, you should see:
- **Hierarchy** panel (left): Empty scene
- **Project** panel (bottom): Assets folder
- **Console** panel: No errors (warnings are OK)

✅ **Success Check:** If Console shows no red errors, you're ready!

## Step 2: Set Up Backend (5 minutes)

### In Terminal:

```bash
# Navigate to backend folder
cd /home/user/games_worldbuilder/backend

# Install dependencies
npm install

# Start PostgreSQL and Redis via Docker
docker-compose up -d

# Verify containers are running
docker ps
# Should show: postgres and redis containers

# Start the backend API server
npm run dev
```

**You should see:**
```
🚀 Server running on port 3000
📊 Database connected
💾 Redis connected
```

### Test the API:
Open a new terminal and run:
```bash
curl http://localhost:3000/api/v1/health
```

**Expected response:**
```json
{
  "status": "ok",
  "timestamp": "2025-11-13T...",
  "uptime": 2.345
}
```

✅ **Success Check:** If you get a JSON response, backend is ready!

## Step 3: First Build Test (5 minutes)

### In Unity Editor:

1. Go to **File → Build Settings**
2. Click **"Add Open Scenes"** (adds current scene)
3. Select **iOS** platform
4. Click **"Switch Platform"** (takes 1-2 minutes)
5. Click **"Build"** (or just close - we're just testing setup)

### Alternative: Command-Line Test

```bash
# From project root
./scripts/unity-helpers.sh validate
```

**Expected output:**
```
✓ Project validation passed
```

✅ **Success Check:** No errors during platform switch!

## Step 4: Create Your First Script with Claude Code (5 minutes)

### In Claude Code (Terminal):

**You say:**
> "Create a ResourceManager script that tracks gold, wood, and stone"

**Claude will create:**
- `unity-project/Assets/Scripts/Managers/ResourceManager.cs`
- Complete implementation with events and validation
- XML documentation comments

### Test It in Unity:

1. Unity auto-recompiles (watch bottom-right progress bar)
2. **Hierarchy** → Right-click → **Create Empty** → Name it "GameManagers"
3. **Inspector** → **Add Component** → Search "ResourceManager" → Add it
4. Click **Play** button (top-center)
5. **Console** should show: "ResourceManager initialized"

✅ **Success Check:** Script compiles and runs without errors!

## Step 5: Import Sample Building Data (5 minutes)

### In Unity Editor:

1. **Tools** → **Import Game Data** (opens import window)
2. Click **"Import Buildings"** button
3. **Console** should show: `✓ Imported 10 buildings`

### Verify Import:

1. **Project** panel → Navigate to **Assets/ScriptableObjects/Buildings/**
2. You should see 10 building config files:
   - town_hall.asset
   - gold_mine.asset
   - lumber_mill.asset
   - etc.

3. Click on `gold_mine.asset` → **Inspector** shows its properties

### What Just Happened?

- Claude Code created the JSON file: `Assets/Resources/Data/buildings.json`
- You ran the import tool in Unity
- Tool automatically created 10 ScriptableObject assets
- **Zero manual Inspector work needed!**

✅ **Success Check:** You see 10 .asset files created!

## Step 6: Understanding the Workflow (5 minutes)

### The Claude Code + Unity Collaboration Pattern:

```
┌─────────────────┐         ┌─────────────────┐
│   Claude Code   │         │   You in Unity  │
│  (File Editor)  │         │  (Visual Setup) │
└────────┬────────┘         └────────┬────────┘
         │                           │
         │ 1. Creates C# scripts     │
         ├──────────────────────────>│
         │                           │
         │                           │ 2. Unity auto-compiles
         │                           │ 3. Attach to GameObjects
         │                           │ 4. Test in Play Mode
         │                           │
         │ 5. Paste console errors   │
         │<──────────────────────────┤
         │                           │
         │ 6. Fixes code             │
         ├──────────────────────────>│
         │                           │
         │                           │ 7. Unity recompiles
         │                           │ 8. Test again
         │                           │
         └───────────────────────────┘
```

### Key Principles:

1. **Claude handles:** All code, data files, configuration
2. **You handle:** Visual layout, testing, GameObj ect hierarchy
3. **Communication:** You paste errors, Claude fixes immediately
4. **Automation:** Use Editor scripts for repetitive tasks

## Common First-Time Commands for Claude Code

Try saying these to Claude Code:

### Creating Game Systems:
```
"Create a BuildingManager that handles building placement on a grid"

"Create a HeroInventory system that manages hero equipment"

"Create a QuestSystem with quest tracking and rewards"
```

### Creating Tests:
```
"Write Unity tests for the ResourceManager"

"Create PlayMode tests for building construction"
```

### Creating Editor Tools:
```
"Create an Editor script to validate all building configs"

"Create a tool to generate 50 random hero configurations"
```

### Debugging:
```
"This error occurred: [paste error]"

"The BuildingManager isn't spawning buildings correctly. Here's the log: [paste log]"
```

## Workflow Examples

### Example 1: Adding a New Building Type

**You say to Claude:**
> "Add a Hospital building that heals troops over time"

**Claude creates:**
1. Adds hospital to `buildings.json`
2. Creates `HospitalComponent.cs` script
3. Updates `BuildingTypes.cs` enum

**You do in Unity:**
1. **Tools → Import Buildings** (updates hospital config)
2. Create hospital prefab
3. Add HospitalComponent
4. Test in Play Mode

**Total time: 3 minutes** (vs. 15 minutes manually)

### Example 2: Fixing a Bug

**You see in Unity Console:**
```
NullReferenceException: Object reference not set to an instance
at ResourceManager.AddResource() line 42
```

**You say to Claude:**
> "Getting this error when collecting gold: [paste full error]"

**Claude analyzes and responds:**
> "The error is on line 42 because `resourceData` can be null. I'm adding a null check and validation."

**Claude fixes it immediately**, Unity recompiles, you test again.

**Total time: 30 seconds** (vs. 10 minutes debugging)

### Example 3: Bulk Data Creation

**You say to Claude:**
> "Create 100 different quest configurations with varied rewards"

**Claude creates:**
1. `quests.json` with 100 quest definitions
2. `QuestImporter.cs` Editor script

**You do in Unity:**
1. **Tools → Import Quests**
2. 100 ScriptableObjects created instantly

**Total time: 2 minutes** (vs. hours of manual work)

## Next Steps

Now that you have the basics:

### Read the Full Documentation:
- **docs/IOS_DEVELOPMENT_PLAN.md** - Complete technical architecture
- **docs/CLAUDE_UNITY_WORKFLOW.md** - Detailed collaboration patterns
- **docs/API_SPECIFICATION.md** - Backend API reference
- **DEVELOPMENT_SETUP.md** - Complete environment setup

### Start Building Features:
1. **Core Game Loop:**
   - "Create a tutorial system for first-time players"
   - "Implement the building upgrade system"
   - "Create the resource production loop"

2. **Hero System:**
   - "Create the hero gacha summoning system"
   - "Implement hero equipment and inventory"
   - "Create hero skill trees"

3. **Combat System:**
   - "Create the troop training system"
   - "Implement PvE battle mechanics"
   - "Create the alliance war system"

### Testing:
```bash
# Run Unity tests via command line
./scripts/unity-helpers.sh test

# Validate project structure
./scripts/unity-helpers.sh validate

# Build for iOS
./scripts/unity-helpers.sh build-ios
```

### Backend Development:
```bash
# Start backend with hot reload
cd backend
npm run dev

# Run backend tests
npm test

# View API documentation
# Open docs/API_SPECIFICATION.md
```

## Troubleshooting

### Unity Won't Open
**Problem:** Unity Hub shows error when opening project

**Solution:**
1. Check Unity version is 2022.3 LTS
2. Try: Right-click project → Show in Finder → Delete Library/ folder
3. Re-open project (Unity will regenerate Library/)

### Backend Won't Start
**Problem:** `npm run dev` shows database connection error

**Solution:**
```bash
# Check Docker containers
docker ps

# If not running, start them
docker-compose up -d

# Check logs
docker-compose logs
```

### Scripts Won't Compile
**Problem:** Unity Console shows compilation errors

**Solution:**
1. Copy the full error message
2. Paste to Claude Code: "Getting this compilation error: [error]"
3. Claude will fix and explain the issue

### Import Tool Not Working
**Problem:** "Import Buildings" button does nothing

**Solution:**
1. Check **Console** for errors
2. Verify JSON exists: `Assets/Resources/Data/buildings.json`
3. Paste error to Claude Code for diagnosis

## Getting Help

### From Claude Code:
Just describe the issue in natural language:
- "The buildings aren't showing up in game"
- "How do I add a new resource type?"
- "This error keeps appearing: [error]"

### From Documentation:
- Check **docs/CLAUDE_UNITY_WORKFLOW.md** for workflow patterns
- Check **docs/API_SPECIFICATION.md** for backend endpoints
- Check **docs/IOS_DEVELOPMENT_PLAN.md** for architecture decisions

### From Unity Console:
- **Red errors:** Copy full message to Claude Code
- **Yellow warnings:** Usually safe to ignore initially
- **Blue logs:** Informational, confirm things are working

## You're Ready!

You now have:
- ✅ Unity project running
- ✅ Backend API running
- ✅ Understanding of Claude Code + Unity workflow
- ✅ Sample building data imported
- ✅ First script created and tested

**Start building your empire!** 🏰

Next: Read **docs/MVP_SPRINT_PLAN.md** for the first 4 weeks of development tasks.
