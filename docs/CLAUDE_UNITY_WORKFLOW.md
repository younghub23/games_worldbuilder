# Claude Code & Unity Hub: Efficient Workflow Guide

## Understanding the Division of Labor

### What Claude Code CAN Do

**1. All C# Script Development**
- Create and edit C# scripts for Unity components
- Implement game logic, managers, controllers
- Write Unity MonoBehaviour classes
- Create ScriptableObjects for data management
- Implement interfaces and custom editors

**2. Project File Management**
- Create folder structures in Assets/
- Manage .meta files (Unity's metadata)
- Create and modify .asmdef files (assembly definitions)
- Set up Packages/manifest.json for dependencies

**3. Unity Project Configuration Files**
- Edit ProjectSettings/*.asset files (text-based YAML)
- Modify Packages/manifest.json for UPM packages
- Configure .gitignore for Unity projects
- Set up CI/CD for Unity Cloud Build

**4. Asset Creation (Text-Based)**
- Create .prefab files (YAML format)
- Create .unity scene files (YAML format)
- Create ScriptableObject .asset files
- Configure .anim and .controller files for animations

**5. Testing & Automation**
- Write Unity Test Framework tests (PlayMode/EditMode)
- Create Editor scripts for automation
- Build shell scripts for command-line Unity builds
- Set up batch operations via Unity CLI

**6. Debugging Support**
- Analyze Unity console logs
- Review stack traces and error messages
- Suggest fixes for compilation errors
- Help interpret Unity-specific errors

### What You Need to Do Manually in Unity Hub/Editor

**1. Unity Hub Operations**
- Install Unity Editor versions
- Manage Unity licenses
- Open projects in Unity Editor
- Switch between Unity versions

**2. Visual/Interactive Tasks in Unity Editor**
- Arrange GameObjects in Scene view
- Configure Inspector properties (transforms, materials)
- Set up Prefab hierarchies visually
- Configure UI Canvas and RectTransforms
- Test gameplay in Play Mode
- Adjust lighting and post-processing
- Set up particle systems visually
- Configure physics colliders by dragging

**3. Asset Import & Configuration**
- Import 3D models, textures, audio files
- Configure import settings (texture compression, audio format)
- Set up sprite sheets and animations
- Configure asset bundles

**4. Build Settings**
- Add scenes to build
- Configure player settings in UI
- Set up platform-specific settings
- Generate Xcode projects for iOS

---

## Efficient Workflow Patterns

### Pattern 1: Script-First Development

**Optimal Flow:**
```
1. You: "I need a BuildingManager that handles construction"
2. Claude: Creates BuildingManager.cs with full implementation
3. You: Open Unity, attach script to GameObject
4. Claude: Creates BuildingConfig ScriptableObject template
5. You: Create ScriptableObject instances in Unity
6. Claude: Creates Editor script to batch-create configs
7. You: Run Editor script via Tools menu
```

**Why This Works:**
- All logic is in code (Claude's strength)
- Manual work is limited to drag-drop and visual setup

### Pattern 2: Test-Driven Unity Development

**Optimal Flow:**
```
1. Claude: Creates test file Tests/BuildingManagerTests.cs
2. Claude: Creates BuildingManager.cs to pass tests
3. You: Open Unity Test Runner window
4. You: Click "Run All" to verify
5. You: Report failures (if any)
6. Claude: Fixes implementation based on test output
```

**Why This Works:**
- Tests run in Unity's environment but code lives in files
- Clear pass/fail feedback loop
- No need for Play Mode testing initially

### Pattern 3: Editor Scripting for Automation

**Optimal Flow:**
```
1. You: "I need to set up 50 building prefabs"
2. Claude: Creates Editor script with [MenuItem]
3. Claude: Script reads CSV/JSON and generates prefabs
4. You: Open Unity, click Tools > Generate Buildings
5. Script creates all prefabs automatically
```

**Example Editor Script:**
```csharp
using UnityEditor;
using UnityEngine;

public class BuildingPrefabGenerator : EditorWindow
{
    [MenuItem("Tools/Generate Building Prefabs")]
    static void GeneratePrefabs()
    {
        // Read building data
        var buildings = JsonUtility.FromJson<BuildingData[]>(
            File.ReadAllText("Assets/Data/buildings.json")
        );

        // Create prefabs
        foreach (var building in buildings)
        {
            GameObject prefab = new GameObject(building.name);
            // Add components...

            // Save as prefab
            PrefabUtility.SaveAsPrefabAsset(
                prefab,
                $"Assets/Prefabs/Buildings/{building.name}.prefab"
            );
            DestroyImmediate(prefab);
        }

        AssetDatabase.Refresh();
        Debug.Log($"Generated {buildings.Length} building prefabs");
    }
}
```

### Pattern 4: Configuration-Driven Development

**Optimal Flow:**
```
1. Claude: Creates data classes and ScriptableObject templates
2. Claude: Creates JSON files with all building data
3. Claude: Creates Editor script to import JSON → ScriptableObjects
4. You: Run import script in Unity
5. You: Visual tweaks only (if needed)
```

**Why This Works:**
- Data lives in JSON (Claude can edit)
- Bulk operations avoid manual Inspector work
- Version control friendly

---

## Command-Line Unity Integration

### Unity CLI Commands I Can Help Generate

**1. Batch Mode Builds**
```bash
# iOS build via command line
/Applications/Unity/Hub/Editor/2022.3.15f1/Unity.app/Contents/MacOS/Unity \
  -quit -batchmode -nographics \
  -projectPath /home/user/games_worldbuilder/unity-project \
  -executeMethod BuildScript.BuildIOS \
  -logFile ./build.log
```

**2. Running Tests Headlessly**
```bash
unity-editor \
  -runTests \
  -batchmode \
  -projectPath ./unity-project \
  -testResults ./test-results.xml \
  -testPlatform PlayMode
```

**3. Asset Bundle Building**
```bash
unity-editor \
  -quit -batchmode \
  -projectPath ./unity-project \
  -executeMethod AssetBundleBuilder.BuildBundles
```

### Setting Up Build Scripts

**Claude creates:** `Assets/Editor/BuildScript.cs`
```csharp
using UnityEditor;
using UnityEditor.Build.Reporting;

public class BuildScript
{
    [MenuItem("Build/iOS")]
    public static void BuildIOS()
    {
        BuildPlayerOptions options = new BuildPlayerOptions();
        options.scenes = new[] {
            "Assets/Scenes/MainMenu.unity",
            "Assets/Scenes/GamePlay.unity"
        };
        options.locationPathName = "Builds/iOS";
        options.target = BuildTarget.iOS;
        options.options = BuildOptions.None;

        BuildReport report = BuildPipeline.BuildPlayer(options);

        if (report.summary.result == BuildResult.Succeeded)
        {
            Debug.Log("Build succeeded: " + report.summary.totalSize + " bytes");
        }
        else
        {
            Debug.LogError("Build failed");
        }
    }
}
```

**You can then run:**
```bash
# From Unity Editor
Build → iOS (menu item)

# OR from command line (for CI/CD)
unity-editor -quit -batchmode -executeMethod BuildScript.BuildIOS
```

---

## Practical Workflow Examples

### Example 1: Adding a New Game Feature

**Feature:** Add resource production system

**Collaborative Steps:**
```
1. You: "Add resource production to buildings"

2. Claude:
   - Creates IResourceProducer interface
   - Creates ResourceProductionComponent.cs
   - Creates ProductionConfig ScriptableObject
   - Creates Editor inspector for ProductionConfig
   - Writes tests for production logic

3. You in Unity:
   - Open existing building prefab
   - Add ResourceProductionComponent
   - Assign ProductionConfig ScriptableObject
   - Test in Play Mode

4. Claude (if issues found):
   - Fixes based on your console log paste
   - Adds validation to prevent setup errors

5. You:
   - Verify fix works
   - Replicate to other building prefabs
```

**Time Saved:** ~80% of implementation time is automated

### Example 2: Debugging a Unity Issue

**Issue:** Buildings not producing resources

**Collaborative Steps:**
```
1. You:
   - Run game in Unity Play Mode
   - Copy console errors/warnings
   - Paste to Claude Code

2. Claude:
   - Analyzes stack trace
   - Identifies null reference in ResourceProductionComponent.cs:42
   - Suggests fix: add null check for productionConfig

3. Claude:
   - Implements fix with validation
   - Adds helpful error messages
   - Adds [RequireComponent] attribute

4. You:
   - Unity auto-recompiles
   - Test again in Play Mode
   - Confirm fix
```

**Time Saved:** Immediate analysis vs. manual debugging

### Example 3: Bulk Asset Creation

**Task:** Create 100 building configurations

**Collaborative Steps:**
```
1. Claude:
   - Creates buildings.csv with all data
   - Creates BuildingConfigImporter.cs editor script
   - Script reads CSV and creates ScriptableObjects

2. You in Unity:
   - Tools → Import Building Configs
   - Script creates 100 .asset files in seconds
   - Visually verify a few samples

3. Claude (if tweaks needed):
   - Modifies CSV data
   - You re-run import script
   - Overwrites old configs
```

**Time Saved:** Hours of manual Inspector work → 30 seconds

---

## Best Practices for Maximum Efficiency

### 1. Use Version Control for Everything

**Claude can:**
- Create .gitignore for Unity (already done)
- Commit C# scripts, prefabs, scenes
- Review diffs in YAML files
- Create branches for features

**You should:**
- Commit after major Unity Editor changes
- Use meaningful commit messages
- Pull before opening Unity (avoid merge conflicts)

### 2. Prefer Code Over Editor Configuration

**Instead of:**
- Manually setting 50 Inspector values

**Do this:**
```csharp
// Claude creates initialization script
public class BuildingInitializer : MonoBehaviour
{
    void Start()
    {
        // Set all values in code
        GetComponent<Building>().Initialize(
            health: 1000,
            defense: 50,
            productionRate: 10.0f
        );
    }
}
```

### 3. Use ScriptableObjects for Data

**Benefits:**
- Claude can create the class structure
- You create instances in Unity (quick)
- Claude can create bulk-import scripts
- Easy to version control

**Example Flow:**
```csharp
// Claude creates this
[CreateAssetMenu(fileName = "BuildingConfig", menuName = "Game/Building Config")]
public class BuildingConfig : ScriptableObject
{
    public string buildingName;
    public int cost;
    public float productionRate;
    public Sprite icon;
}
```

**Then you in Unity:**
- Right-click → Create → Game → Building Config
- Fill in a few values
- Or use Claude's import script for bulk creation

### 4. Leverage Unity Test Framework

**Claude creates comprehensive tests:**
```csharp
[UnityTest]
public IEnumerator Building_Produces_Resources_Over_Time()
{
    var building = new GameObject().AddComponent<Building>();
    building.productionRate = 10f;

    yield return new WaitForSeconds(5f);

    Assert.AreEqual(50, building.GetProducedAmount(), 1f);
}
```

**You run in Unity:**
- Window → General → Test Runner
- Click "Run All"
- Report failures to Claude
- Claude fixes and you re-run

### 5. Create Custom Unity Editor Tools

**Claude can create powerful tools:**

**Example: Scene Validator**
```csharp
[MenuItem("Tools/Validate Scene")]
static void ValidateScene()
{
    var allBuildings = FindObjectsOfType<Building>();

    foreach (var building in allBuildings)
    {
        if (building.config == null)
        {
            Debug.LogError($"Building {building.name} missing config!", building);
        }
    }

    Debug.Log($"Validated {allBuildings.Length} buildings");
}
```

**Benefits:**
- Run before commits
- Catch configuration errors early
- No manual checking needed

---

## Communication Patterns

### When You Need Help

**❌ Less Efficient:**
"My buildings aren't working"

**✅ More Efficient:**
"BuildingManager shows this error: `NullReferenceException: Object reference not set to an instance of an object at BuildingManager.Update() [0x00023]` when I click the Build button"

**Why:** Specific errors let me fix immediately vs. guessing

### When Requesting Features

**❌ Less Efficient:**
"Add alliances"

**✅ More Efficient:**
"Add alliance system where:
- Players can create/join alliances (max 50 members)
- Alliance has shared chat
- Members can donate resources
- Need AllianceManager.cs, Alliance.cs, and AllianceUI.cs"

**Why:** Clear requirements = better code on first attempt

### When Reporting Issues

**✅ Always Include:**
1. Unity console errors (copy exact text)
2. What you expected to happen
3. What actually happened
4. Steps to reproduce

**Example:**
```
I added the ResourceProductionComponent to my Farm prefab and assigned
the FarmConfig ScriptableObject. When I press Play, I see:

"NullReferenceException: Object reference not set to an instance of
an object at ResourceProductionComponent.Update() line 23"

Expected: Farm should produce 10 food per second
Actual: Error thrown and no production happens

Steps:
1. Open Scenes/GamePlay
2. Place Farm prefab in scene
3. Enter Play Mode
4. Wait 1 second → error appears
```

---

## Automation Opportunities

### 1. Git Hooks for Unity

**Claude can create:** `.git/hooks/pre-commit`
```bash
#!/bin/bash
# Validate Unity meta files exist
for file in $(git diff --cached --name-only --diff-filter=A | grep "^Assets/"); do
    if [ ! -f "$file.meta" ]; then
        echo "Error: Missing .meta file for $file"
        exit 1
    fi
done
```

### 2. Watch Scripts for Auto-Generation

**Claude can create:** `scripts/watch-data.sh`
```bash
#!/bin/bash
# Watch for changes in data files and regenerate assets
fswatch -o Assets/Data/*.json | while read; do
    echo "Data changed, regenerating assets..."
    unity-editor -quit -batchmode \
      -executeMethod DataImporter.ImportAll
done
```

### 3. CI/CD Integration

**Claude can enhance:** `.github/workflows/unity-build.yml`
```yaml
# Add automatic test running
- name: Run Unity Tests
  uses: game-ci/unity-test-runner@v2
  with:
    testMode: PlayMode

# Add automatic builds on PR
- name: Build Project
  if: github.event_name == 'pull_request'
  uses: game-ci/unity-builder@v2
```

---

## Quick Reference

### Claude Code Strengths
- C# script creation and editing
- Unity Test Framework tests
- Editor scripts and tools
- Data file management (JSON, CSV)
- Build script automation
- CI/CD pipeline configuration
- Debugging and error analysis

### Unity Editor Strengths
- Visual scene composition
- GameObject hierarchy management
- Inspector-based configuration
- Play Mode testing
- Asset import and configuration
- Platform build settings
- Visual debugging (Scene/Game view)

### Optimal Collaboration
1. **Claude**: Creates code, tests, data structures
2. **You**: Visual setup, testing, configuration
3. **Claude**: Fixes based on your feedback
4. **You**: Verify and iterate

### Golden Rule
**If it can be defined in code or data files, let Claude handle it.**
**If it requires visual composition or Play Mode testing, you handle it.**

---

## Next Steps

To maximize our efficiency:

1. **Tell me when you hit Unity errors** - Paste the exact console output
2. **Request Editor scripts** - If you find yourself doing repetitive tasks
3. **Use Test Runner** - I'll create tests, you run them and report results
4. **Leverage CLI builds** - For CI/CD, I can set up command-line builds
5. **Keep data in files** - CSV/JSON I can edit vs. Inspector values I can't see

Together we can build this game efficiently by leveraging each other's strengths!
