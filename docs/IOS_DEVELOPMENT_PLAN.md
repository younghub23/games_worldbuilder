# iOS DEVELOPMENT PLAN: EMPIRE GENESIS
## Technical Architecture & Implementation Strategy

---

## PART 1: TECHNOLOGY STACK DECISION

### **Option A: Native iOS (Swift + SwiftUI) - RECOMMENDED**

**Pros:**
- Best performance on iOS devices
- Native touch gestures and animations
- Lowest battery consumption
- Smallest app size (~50-80MB)
- Full access to iOS APIs
- Apple's Metal for graphics

**Cons:**
- iOS only (separate Android build needed)
- Larger initial development time
- Need iOS-specific developers

**Use this if:** You want the best iOS experience and plan separate Android development

---

### **Option B: Unity (C#) - RECOMMENDED FOR CROSS-PLATFORM**

**Pros:**
- Single codebase for iOS + Android
- Mature 2D/2.5D engine perfect for city builders
- Large asset store
- Visual editor for designers
- Proven for successful mobile games (Clash of Clans, Rise of Kingdoms)
- C# is productive and well-documented

**Cons:**
- Larger app size (~150-200MB)
- Slightly worse battery life than native
- Unity license costs ($185/month Professional)

**Use this if:** You want iOS + Android from same codebase (RECOMMENDED)

---

### **DECISION: Unity + iOS Native Plugins**

**Why:**
1. Cross-platform from day one (reduces total cost by 40%)
2. Proven technology for this genre
3. Faster iteration for designers
4. Large pool of Unity developers
5. Can still use native iOS features via plugins

**Stack:**
- **Frontend:** Unity 2022.3 LTS (C#)
- **Backend:** Node.js + Express (or Go for performance)
- **Database:** PostgreSQL + Redis
- **Cloud:** AWS or Google Cloud
- **Realtime:** Socket.io or native WebSockets
- **Analytics:** Firebase + Mixpanel
- **Monetization:** Unity IAP + RevenueCat
- **Crash Reporting:** Sentry

---

## PART 2: PROJECT ARCHITECTURE

### **2.1 Frontend (Unity) Architecture**

```
Assets/
├── _Project/
│   ├── Scripts/
│   │   ├── Core/
│   │   │   ├── GameManager.cs              # Singleton, game state
│   │   │   ├── SaveManager.cs              # Persistence
│   │   │   ├── NetworkManager.cs           # API calls
│   │   │   ├── AudioManager.cs             # Sound/music
│   │   │   └── EventBus.cs                 # Event system
│   │   ├── Systems/
│   │   │   ├── BuildingSystem/
│   │   │   │   ├── BuildingManager.cs
│   │   │   │   ├── Building.cs             # Base building class
│   │   │   │   ├── ProductionBuilding.cs
│   │   │   │   ├── HousingBuilding.cs
│   │   │   │   └── BuildingData.cs         # ScriptableObject
│   │   │   ├── ResourceSystem/
│   │   │   │   ├── ResourceManager.cs
│   │   │   │   ├── Resource.cs
│   │   │   │   └── ProductionChain.cs
│   │   │   ├── PopulationSystem/
│   │   │   │   ├── PopulationManager.cs
│   │   │   │   └── PopulationClass.cs
│   │   │   ├── HeroSystem/
│   │   │   │   ├── HeroManager.cs
│   │   │   │   ├── Hero.cs
│   │   │   │   ├── HeroAbility.cs
│   │   │   │   └── GachaManager.cs
│   │   │   ├── AllianceSystem/
│   │   │   │   ├── AllianceManager.cs
│   │   │   │   └── AllianceData.cs
│   │   │   ├── MapSystem/
│   │   │   │   ├── MapManager.cs
│   │   │   │   ├── GridSystem.cs           # Hex or square grid
│   │   │   │   └── FogOfWar.cs
│   │   │   └── EconomySystem/
│   │   │       ├── CurrencyManager.cs
│   │   │       ├── ShopManager.cs
│   │   │       └── IAPManager.cs
│   │   ├── UI/
│   │   │   ├── MainHUD.cs
│   │   │   ├── BuildingMenu.cs
│   │   │   ├── HeroMenu.cs
│   │   │   ├── GachaUI.cs
│   │   │   ├── AllianceUI.cs
│   │   │   └── UIAnimation.cs
│   │   ├── Data/
│   │   │   └── ScriptableObjects/
│   │   │       ├── BuildingDataSO/
│   │   │       ├── HeroDataSO/
│   │   │       ├── ResourceDataSO/
│   │   │       └── EraDataSO/
│   │   └── Utilities/
│   │       ├── Timer.cs
│   │       ├── ObjectPool.cs
│   │       └── Extensions.cs
│   ├── Prefabs/
│   │   ├── Buildings/
│   │   ├── UI/
│   │   ├── Heroes/
│   │   └── VFX/
│   ├── Scenes/
│   │   ├── Boot.unity                      # Init scene
│   │   ├── MainMenu.unity
│   │   ├── GamePlay.unity
│   │   └── Tutorial.unity
│   ├── Resources/
│   │   └── Data/                           # JSON imports
│   └── StreamingAssets/
│       └── Config/
└── Plugins/
    ├── iOS/                                # Native iOS plugins
    └── Android/                            # Native Android plugins
```

---

### **2.2 Backend Architecture**

**Microservices Approach:**

```
backend/
├── api-gateway/                            # Entry point, auth
│   ├── src/
│   │   ├── middleware/
│   │   │   ├── auth.js
│   │   │   └── rateLimit.js
│   │   ├── routes/
│   │   └── server.js
│   └── package.json
├── game-service/                           # Game logic
│   ├── src/
│   │   ├── controllers/
│   │   │   ├── buildingController.js
│   │   │   ├── resourceController.js
│   │   │   └── eraController.js
│   │   ├── models/
│   │   │   ├── Player.js
│   │   │   ├── Building.js
│   │   │   ├── Hero.js
│   │   │   └── Alliance.js
│   │   ├── services/
│   │   │   ├── productionService.js
│   │   │   ├── calculationService.js
│   │   │   └── validationService.js
│   │   └── routes/
│   └── package.json
├── hero-service/                           # Gacha, heroes
│   ├── src/
│   │   ├── controllers/
│   │   │   ├── gachaController.js
│   │   │   └── heroController.js
│   │   ├── services/
│   │   │   ├── gachaService.js            # Pity system
│   │   │   └── heroService.js
│   │   └── routes/
│   └── package.json
├── alliance-service/                       # Social features
│   ├── src/
│   │   ├── controllers/
│   │   ├── services/
│   │   └── routes/
│   └── package.json
├── payment-service/                        # IAP, monetization
│   ├── src/
│   │   ├── controllers/
│   │   ├── services/
│   │   │   ├── iapVerification.js         # Receipt validation
│   │   │   └── subscriptionService.js
│   │   └── routes/
│   └── package.json
├── analytics-service/                      # Event tracking
│   └── src/
├── notification-service/                   # Push notifications
│   └── src/
└── shared/
    ├── database/
    │   ├── migrations/
    │   └── seeds/
    ├── models/
    └── utils/
```

**Database Schema:**

```sql
-- PostgreSQL Schema

-- Users & Auth
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    apple_id VARCHAR(255),
    google_id VARCHAR(255),
    email VARCHAR(255),
    username VARCHAR(50) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP
);

-- Player Data
CREATE TABLE players (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    display_name VARCHAR(50),
    level INT DEFAULT 1,
    experience BIGINT DEFAULT 0,
    current_era INT DEFAULT 1,
    population INT DEFAULT 0,
    -- Currencies
    gold BIGINT DEFAULT 100,
    gems INT DEFAULT 50,
    scrolls INT DEFAULT 0,
    prestige_points INT DEFAULT 0,
    -- VIP
    vip_level INT DEFAULT 0,
    vip_points INT DEFAULT 0,
    -- Stats
    city_beauty_score INT DEFAULT 0,
    alliance_id UUID,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Buildings
CREATE TABLE player_buildings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    player_id UUID REFERENCES players(id),
    building_type_id INT NOT NULL,           -- References game_buildings
    level INT DEFAULT 1,
    position_x INT,
    position_y INT,
    is_under_construction BOOLEAN DEFAULT false,
    construction_started_at TIMESTAMP,
    construction_finish_at TIMESTAMP,
    last_collected_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Heroes
CREATE TABLE player_heroes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    player_id UUID REFERENCES players(id),
    hero_type_id INT NOT NULL,               -- References game_heroes
    level INT DEFAULT 1,
    experience INT DEFAULT 0,
    rarity INT,                               -- 4, 5, 6, 7 stars
    is_equipped BOOLEAN DEFAULT false,
    assigned_building_id UUID,
    acquired_at TIMESTAMP DEFAULT NOW()
);

-- Gacha
CREATE TABLE gacha_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    player_id UUID REFERENCES players(id),
    banner_type VARCHAR(50),
    result_type VARCHAR(50),                 -- hero, blueprint
    result_id INT,
    rarity INT,
    pull_number INT,                         -- For pity tracking
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE player_gacha_pity (
    player_id UUID PRIMARY KEY REFERENCES players(id),
    hero_4_star_pity INT DEFAULT 0,
    hero_5_star_pity INT DEFAULT 0,
    hero_6_star_pity INT DEFAULT 0,
    blueprint_5_star_pity INT DEFAULT 0,
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Alliances
CREATE TABLE alliances (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(50) UNIQUE NOT NULL,
    tag VARCHAR(5) UNIQUE NOT NULL,
    description TEXT,
    level INT DEFAULT 1,
    experience BIGINT DEFAULT 0,
    leader_id UUID REFERENCES players(id),
    member_count INT DEFAULT 1,
    max_members INT DEFAULT 50,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE alliance_members (
    alliance_id UUID REFERENCES alliances(id),
    player_id UUID REFERENCES players(id),
    role VARCHAR(20),                        -- leader, officer, elite, member
    joined_at TIMESTAMP DEFAULT NOW(),
    contribution_points INT DEFAULT 0,
    PRIMARY KEY (alliance_id, player_id)
);

-- Purchases & IAP
CREATE TABLE purchases (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    player_id UUID REFERENCES players(id),
    product_id VARCHAR(100),
    platform VARCHAR(20),                    -- ios, android
    receipt TEXT,                            -- Store receipt
    amount_usd DECIMAL(10,2),
    currency VARCHAR(3),
    is_verified BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Sessions & Analytics
CREATE TABLE player_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    player_id UUID REFERENCES players(id),
    session_start TIMESTAMP DEFAULT NOW(),
    session_end TIMESTAMP,
    duration_seconds INT,
    device_type VARCHAR(50),
    os_version VARCHAR(20)
);

-- Game Static Data (loaded from JSON)
CREATE TABLE game_buildings (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    category VARCHAR(50),
    era INT,
    cost_json JSONB,                         -- {"gold": 100, "wood": 50}
    production_json JSONB,
    requirements_json JSONB,
    data JSONB                               -- Full building data
);

CREATE TABLE game_heroes (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    rarity INT,
    element VARCHAR(20),
    role VARCHAR(50),
    abilities_json JSONB,
    data JSONB
);
```

---

### **2.3 API Design**

**RESTful API Endpoints:**

```
Authentication:
POST   /api/v1/auth/login                   # Login with Apple/Google
POST   /api/v1/auth/register
POST   /api/v1/auth/refresh                 # Refresh JWT token

Player:
GET    /api/v1/player/profile
PUT    /api/v1/player/profile
GET    /api/v1/player/resources
GET    /api/v1/player/stats

Buildings:
GET    /api/v1/buildings                    # Get all player buildings
POST   /api/v1/buildings                    # Place new building
PUT    /api/v1/buildings/:id/upgrade
DELETE /api/v1/buildings/:id
POST   /api/v1/buildings/:id/collect        # Collect production
POST   /api/v1/buildings/:id/speed-up       # Use speed-up

Heroes:
GET    /api/v1/heroes                       # Get all player heroes
GET    /api/v1/heroes/:id
PUT    /api/v1/heroes/:id/level-up
PUT    /api/v1/heroes/:id/assign            # Assign to building

Gacha:
POST   /api/v1/gacha/pull                   # Single pull
POST   /api/v1/gacha/pull-10                # 10-pull
GET    /api/v1/gacha/rates                  # Show rates
GET    /api/v1/gacha/history
GET    /api/v1/gacha/pity                   # Pity counter

Alliance:
GET    /api/v1/alliances                    # List alliances
POST   /api/v1/alliances                    # Create alliance
GET    /api/v1/alliances/:id
POST   /api/v1/alliances/:id/join
DELETE /api/v1/alliances/:id/leave
GET    /api/v1/alliances/:id/members
POST   /api/v1/alliances/:id/donate         # Donate resources

Shop:
GET    /api/v1/shop/products                # List IAP products
POST   /api/v1/shop/purchase                # Verify purchase
GET    /api/v1/shop/daily-deals

Trade:
POST   /api/v1/trade/create                 # Create trade offer
GET    /api/v1/trade/offers
POST   /api/v1/trade/:id/accept

Analytics:
POST   /api/v1/analytics/event              # Track events
```

**WebSocket Events (Realtime):**

```
// Client → Server
socket.emit('building:start', {buildingId, type});
socket.emit('building:collect', {buildingId});
socket.emit('alliance:chat', {message});

// Server → Client
socket.on('building:completed', {buildingId, rewards});
socket.on('resource:update', {resources});
socket.on('alliance:message', {sender, message});
socket.on('player:attacked', {attacker, damage});
```

---

## PART 3: iOS-SPECIFIC IMPLEMENTATION

### **3.1 Unity to iOS Bridge**

**Native iOS Features via Plugins:**

```csharp
// Assets/_Project/Scripts/iOS/iOSNativeBridge.cs
#if UNITY_IOS
using System.Runtime.InteropServices;

public class iOSNativeBridge : MonoBehaviour
{
    // Import native iOS functions
    [DllImport("__Internal")]
    private static extern void _VibrateDevice(int intensity);

    [DllImport("__Internal")]
    private static extern void _ShowNativeShare(string text, string imageUrl);

    [DllImport("__Internal")]
    private static extern void _RequestPushPermission();

    [DllImport("__Internal")]
    private static extern string _GetDeviceIdentifier();

    public static void Vibrate(int intensity = 1)
    {
        #if UNITY_IOS && !UNITY_EDITOR
        _VibrateDevice(intensity);
        #endif
    }

    public static void ShowShareSheet(string text, string imageUrl)
    {
        #if UNITY_IOS && !UNITY_EDITOR
        _ShowNativeShare(text, imageUrl);
        #endif
    }
}
#endif
```

**iOS Plugin (Objective-C):**

```objectivec
// Plugins/iOS/iOSBridge.mm
#import <UIKit/UIKit.h>

extern "C" {
    void _VibrateDevice(int intensity) {
        if (intensity == 1) {
            AudioServicesPlaySystemSound(kSystemSoundID_Vibrate);
        } else {
            // Haptic feedback for iOS 10+
            UIImpactFeedbackGenerator *generator = [[UIImpactFeedbackGenerator alloc] initWithStyle:UIImpactFeedbackStyleMedium];
            [generator impactOccurred];
        }
    }

    void _ShowNativeShare(const char* text, const char* imageUrl) {
        NSString *shareText = [NSString stringWithUTF8String:text];
        UIViewController *rootVC = UnityGetGLViewController();

        UIActivityViewController *activityVC = [[UIActivityViewController alloc]
            initWithActivityItems:@[shareText]
            applicationActivities:nil];

        [rootVC presentViewController:activityVC animated:YES completion:nil];
    }
}
```

### **3.2 iOS Optimizations**

**Info.plist Configuration:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN">
<plist version="1.0">
<dict>
    <!-- App Transport Security -->
    <key>NSAppTransportSecurity</key>
    <dict>
        <key>NSAllowsArbitraryLoads</key>
        <false/>
    </dict>

    <!-- Push Notifications -->
    <key>UIBackgroundModes</key>
    <array>
        <string>remote-notification</string>
    </array>

    <!-- Camera (for AR features later) -->
    <key>NSCameraUsageDescription</key>
    <string>Used for AR city viewing</string>

    <!-- Photo Library (for screenshots) -->
    <key>NSPhotoLibraryAddUsageDescription</key>
    <string>Save screenshots of your city</string>

    <!-- Tracking (iOS 14+) -->
    <key>NSUserTrackingUsageDescription</key>
    <string>This helps us provide personalized content</string>

    <!-- Minimum iOS Version -->
    <key>MinimumOSVersion</key>
    <string>13.0</string>
</dict>
</plist>
```

**Build Settings:**

```
Target iOS Version: 13.0+
Architecture: ARM64
Target Devices: iPhone, iPad
Graphics API: Metal
Enable Bitcode: Yes
Strip Engine Code: Yes (for App Store)
Managed Stripping Level: Medium
IL2CPP: Yes (better performance)
```

---

## PART 4: DEVELOPMENT ROADMAP

### **Phase 1: Foundation (Weeks 1-4)**

**Week 1-2: Project Setup**
- [ ] Create Unity project (2022.3 LTS)
- [ ] Set up Git repository with LFS for assets
- [ ] Configure iOS build settings
- [ ] Set up backend boilerplate (Node.js + Express)
- [ ] Set up PostgreSQL database
- [ ] Create CI/CD pipeline (GitHub Actions)

**Week 3-4: Core Systems**
- [ ] Implement GameManager (singleton pattern)
- [ ] Implement SaveManager (local + cloud save)
- [ ] Implement NetworkManager (API wrapper)
- [ ] Create grid system (hex or square grid)
- [ ] Implement camera controls (pan, zoom, rotate)
- [ ] Basic UI framework

**Deliverable:** Playable empty map with camera controls

---

### **Phase 2: MVP - Era 1 (Weeks 5-12)**

**Week 5-6: Resource System**
- [ ] Resource types (Wood, Stone, Food, Water, Gold)
- [ ] ResourceManager with storage
- [ ] Production/consumption calculations
- [ ] UI for resource display

**Week 7-8: Building System**
- [ ] Building placement with grid snapping
- [ ] 12 Era 1 buildings (data from JSON)
- [ ] Construction timer system
- [ ] Production collection
- [ ] Building upgrades

**Week 9-10: Population System**
- [ ] Population classes (Pioneers)
- [ ] Housing capacity
- [ ] Tax income generation
- [ ] Needs fulfillment (food, water)

**Week 11-12: Hero System (Basic)**
- [ ] 3 starter heroes
- [ ] Hero selection screen
- [ ] Hero assignment to buildings
- [ ] Passive ability system

**Deliverable:** Playable Era 1 with all 12 buildings and 3 heroes

---

### **Phase 3: Backend Integration (Weeks 13-16)**

**Week 13-14: Authentication & Player Data**
- [ ] Sign in with Apple integration
- [ ] Player registration/login
- [ ] Cloud save sync
- [ ] Profile management

**Week 15-16: Multiplayer Foundation**
- [ ] Alliance system (create, join, leave)
- [ ] Alliance chat
- [ ] Resource sharing
- [ ] Friend system

**Deliverable:** Multiplayer-ready with cloud saves

---

### **Phase 4: Monetization (Weeks 17-20)**

**Week 17-18: IAP Integration**
- [ ] Unity IAP setup
- [ ] Product catalog
- [ ] Receipt validation
- [ ] Gem purchases
- [ ] Starter pack offer

**Week 19-20: Gacha System**
- [ ] Gacha UI
- [ ] Pull mechanics (single, 10-pull)
- [ ] Pity system implementation
- [ ] Hero animation reveals

**Deliverable:** Monetization-ready build

---

### **Phase 5: Polish & Tutorial (Weeks 21-24)**

**Week 21-22: Tutorial**
- [ ] Onboarding flow
- [ ] Tutorial steps (FTUE)
- [ ] Tooltips system
- [ ] Help screens

**Week 23-24: Polish**
- [ ] Sound effects
- [ ] Background music
- [ ] Particle effects
- [ ] Building animations
- [ ] UI polish
- [ ] Performance optimization

**Deliverable:** TestFlight-ready MVP

---

### **Phase 6: Testing & Soft Launch (Weeks 25-28)**

**Week 25-26: Internal Testing**
- [ ] QA testing
- [ ] Bug fixes
- [ ] Balance adjustments
- [ ] Analytics implementation

**Week 27-28: Soft Launch**
- [ ] Submit to TestFlight
- [ ] Gather feedback
- [ ] Monitor metrics (retention, monetization)
- [ ] Iterate based on data

**Deliverable:** Validated MVP ready for expansion

---

## PART 5: SPRINT BREAKDOWN (First 4 Weeks)

See next document for detailed sprint planning...

---

## PART 6: DEPLOYMENT

### **iOS App Store Submission**

**Requirements:**
1. Apple Developer Account ($99/year)
2. App Store Connect setup
3. Privacy policy URL
4. App Store assets:
   - App icon (1024x1024)
   - Screenshots (6.5" iPhone, 12.9" iPad)
   - Preview video (optional but recommended)
5. Age rating questionnaire
6. Export compliance

**App Store Optimization (ASO):**
- Title: "Empire Genesis: Build & Conquer"
- Subtitle: "City Builder Strategy Game"
- Keywords: city builder, strategy, empire, civilization, gacha
- Description: (First 3 lines critical for visibility)

**Build Process:**
```bash
# Unity Cloud Build or local
1. Build for iOS (Xcode project)
2. Open in Xcode
3. Configure signing & capabilities
4. Archive build
5. Upload to App Store Connect
6. Submit for review (7-14 days)
```

---

## NEXT STEPS

1. **Choose your path:**
   - [ ] Solo developer: Start with Phase 1, 20 hours/week = 6 months
   - [ ] Small team (3-5): Parallel development, 3-4 months to MVP
   - [ ] Funded team (10+): Full roadmap, 6 months to launch

2. **Immediate actions:**
   - [ ] Set up Unity project
   - [ ] Set up backend repository
   - [ ] Create Trello/Jira board with tasks
   - [ ] Start with grid system (most fundamental)

3. **Read the detailed technical docs:**
   - Technical Architecture (next document)
   - Backend API Specification
   - Sprint Planning (4-week sprints)

**Want me to create the detailed sprint plan for the first month of development?**
