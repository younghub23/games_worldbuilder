# Empire Genesis - Unity Project

Unity client for Empire Genesis mobile game.

## Requirements

- Unity 2022.3 LTS or later
- Xcode 14+ (for iOS builds)
- JDK 11+ (for Android builds)

## Setup

1. **Open in Unity Hub:**
   ```
   Open Unity Hub → Add → Select this folder
   ```

2. **Install Required Packages:**
   - Window → Package Manager
   - Install:
     - Newtonsoft Json
     - DOTween (Asset Store)
     - Unity IAP
     - TextMeshPro

3. **Configure iOS Build Settings:**
   ```
   File → Build Settings → iOS
   - Bundle Identifier: com.[company].empiregenesis
   - Minimum iOS Version: 13.0
   - Architecture: ARM64
   ```

4. **Import Game Data:**
   - Copy JSON files from `/data` to `Assets/Resources/Data/`
   - These will be loaded at runtime

## Project Structure

```
Assets/
├── _Project/              # Our game code
│   ├── Scenes/           # Unity scenes
│   ├── Scripts/          # C# scripts
│   ├── Prefabs/          # Prefabs
│   ├── UI/               # UI assets
│   └── Resources/        # Runtime assets
├── Plugins/              # Native plugins
└── StreamingAssets/      # Config files
```

## Building

### iOS
```
File → Build Settings → iOS → Build
Open in Xcode → Archive → Upload to App Store Connect
```

### Android
```
File → Build Settings → Android → Build
```

## Testing

Press Play in Unity Editor to test in Play Mode.

For iOS device testing:
1. Connect iPhone via USB
2. File → Build Settings → Build and Run
3. Xcode will deploy to device

## Scripts Overview

- **GameManager.cs** - Main game singleton
- **ResourceManager.cs** - Resource system
- **BuildingManager.cs** - Building placement & management
- **NetworkManager.cs** - API communication
- **SaveManager.cs** - Local & cloud saves

## Debugging

Enable debug logs in GameManager:
```csharp
public bool debugMode = true;
```

View logs in Unity Console (Ctrl+Shift+C / Cmd+Shift+C)
