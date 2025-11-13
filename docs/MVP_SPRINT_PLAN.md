# MVP SPRINT PLAN - FIRST 4 WEEKS
## Building Era 1 Foundation

---

## SPRINT 1: PROJECT FOUNDATION (Week 1)

### Sprint Goal
**Set up complete development environment with basic game loop running on iOS device**

### Team Capacity
- **Solo Dev:** 40 hours (full-time week)
- **Small Team (3):** 120 hours total

---

### MONDAY: Project Initialization (8 hours)

**Morning (4h): Unity Setup**
- [ ] Create Unity 2022.3 LTS project
- [ ] Configure iOS build settings
- [ ] Set up Git repository with LFS
- [ ] Install required packages (DOTween, TMPro, Newtonsoft Json)
- [ ] Create folder structure (`_Project/`, `Scripts/`, etc.)

**Afternoon (4h): Backend Setup**
- [ ] Initialize Node.js project
- [ ] Set up Express server skeleton
- [ ] Configure PostgreSQL with Docker
- [ ] Create initial database schema
- [ ] Set up environment variables

**Deliverable:** Empty projects running locally

---

### TUESDAY: Core Systems (8 hours)

**Morning (4h): Game Manager**

**File:** `Assets/_Project/Scripts/Core/GameManager.cs`

```csharp
using UnityEngine;
using System;

public class GameManager : MonoBehaviour
{
    public static GameManager Instance { get; private set; }

    [Header("Game State")]
    public GameState currentState = GameState.MainMenu;

    [Header("Managers")]
    public ResourceManager resourceManager;
    public BuildingManager buildingManager;
    public SaveManager saveManager;
    public NetworkManager networkManager;

    public event Action<GameState> OnGameStateChanged;

    private void Awake()
    {
        if (Instance == null)
        {
            Instance = this;
            DontDestroyOnLoad(gameObject);
            InitializeManagers();
        }
        else
        {
            Destroy(gameObject);
        }
    }

    private void Start()
    {
        ChangeState(GameState.Loading);
        LoadGameData();
    }

    private void InitializeManagers()
    {
        resourceManager = GetComponent<ResourceManager>();
        buildingManager = GetComponent<BuildingManager>();
        saveManager = GetComponent<SaveManager>();
        networkManager = GetComponent<NetworkManager>();
    }

    private async void LoadGameData()
    {
        // Load from local save first
        bool localSaveExists = await saveManager.LoadLocal();

        if (localSaveExists)
        {
            ChangeState(GameState.Playing);
        }
        else
        {
            // New player - show tutorial
            ChangeState(GameState.Tutorial);
        }
    }

    public void ChangeState(GameState newState)
    {
        currentState = newState;
        OnGameStateChanged?.Invoke(newState);
        Debug.Log($"Game State Changed: {newState}");
    }
}

public enum GameState
{
    MainMenu,
    Loading,
    Tutorial,
    Playing,
    Paused,
    BuildingMenu,
    HeroMenu
}
```

**Afternoon (4h): Resource System**

**File:** `Assets/_Project/Scripts/Systems/ResourceSystem/ResourceManager.cs`

```csharp
using UnityEngine;
using System.Collections.Generic;
using System;

[System.Serializable]
public class ResourceData
{
    public ResourceType type;
    public long amount;
    public long capacity;

    public bool CanAdd(long value) => amount + value <= capacity;
    public void Add(long value) => amount = Mathf.Min(amount + value, capacity);
    public bool CanSubtract(long value) => amount >= value;
    public void Subtract(long value) => amount = Mathf.Max(0, amount - value);
}

public class ResourceManager : MonoBehaviour
{
    [Header("Resources")]
    public Dictionary<ResourceType, ResourceData> resources = new Dictionary<ResourceType, ResourceData>();

    public event Action<ResourceType, long> OnResourceChanged;

    private void Awake()
    {
        InitializeResources();
    }

    private void InitializeResources()
    {
        // Initialize starting resources
        resources[ResourceType.Gold] = new ResourceData { type = ResourceType.Gold, amount = 100, capacity = 10000 };
        resources[ResourceType.Wood] = new ResourceData { type = ResourceType.Wood, amount = 50, capacity = 1000 };
        resources[ResourceType.Stone] = new ResourceData { type = ResourceType.Stone, amount = 50, capacity = 1000 };
        resources[ResourceType.Food] = new ResourceData { type = ResourceType.Food, amount = 30, capacity = 500 };
        resources[ResourceType.Water] = new ResourceData { type = ResourceType.Water, amount = 20, capacity = 500 };
    }

    public bool AddResource(ResourceType type, long amount)
    {
        if (resources[type].CanAdd(amount))
        {
            resources[type].Add(amount);
            OnResourceChanged?.Invoke(type, resources[type].amount);
            return true;
        }
        return false;
    }

    public bool SubtractResource(ResourceType type, long amount)
    {
        if (resources[type].CanSubtract(amount))
        {
            resources[type].Subtract(amount);
            OnResourceChanged?.Invoke(type, resources[type].amount);
            return true;
        }
        return false;
    }

    public bool HasResources(Dictionary<ResourceType, long> costs)
    {
        foreach (var cost in costs)
        {
            if (resources[cost.Key].amount < cost.Value)
                return false;
        }
        return true;
    }

    public long GetResourceAmount(ResourceType type)
    {
        return resources[type].amount;
    }
}

public enum ResourceType
{
    Gold,
    Wood,
    Stone,
    Food,
    Water,
    Gems // Premium currency
}
```

**Deliverable:** Core managers functional

---

### WEDNESDAY: Grid System (8 hours)

**Full Day: Isometric/Hex Grid**

**File:** `Assets/_Project/Scripts/Systems/MapSystem/GridSystem.cs`

```csharp
using UnityEngine;
using System.Collections.Generic;

public class GridSystem : MonoBehaviour
{
    [Header("Grid Settings")]
    public int gridWidth = 20;
    public int gridHeight = 20;
    public float cellSize = 1f;

    [Header("Visual")]
    public GameObject gridCellPrefab;
    public Material defaultMaterial;
    public Material highlightMaterial;

    private GridCell[,] grid;
    private Dictionary<Vector2Int, Building> buildingsOnGrid = new Dictionary<Vector2Int, Building>();

    private void Start()
    {
        InitializeGrid();
    }

    private void InitializeGrid()
    {
        grid = new GridCell[gridWidth, gridHeight];

        for (int x = 0; x < gridWidth; x++)
        {
            for (int y = 0; y < gridHeight; y++)
            {
                Vector3 worldPos = GridToWorldPosition(x, y);
                GridCell cell = Instantiate(gridCellPrefab, worldPos, Quaternion.identity, transform).GetComponent<GridCell>();
                cell.Initialize(x, y);
                grid[x, y] = cell;
            }
        }
    }

    public Vector3 GridToWorldPosition(int x, int y)
    {
        // Isometric conversion
        float worldX = (x - y) * cellSize * 0.5f;
        float worldZ = (x + y) * cellSize * 0.25f;
        return new Vector3(worldX, 0, worldZ);
    }

    public Vector2Int WorldToGridPosition(Vector3 worldPos)
    {
        // Reverse isometric conversion
        int x = Mathf.RoundToInt((worldPos.x / cellSize + worldPos.z / (cellSize * 0.5f)));
        int y = Mathf.RoundToInt((worldPos.z / (cellSize * 0.5f) - worldPos.x / cellSize));
        return new Vector2Int(x, y);
    }

    public bool IsCellOccupied(int x, int y)
    {
        return buildingsOnGrid.ContainsKey(new Vector2Int(x, y));
    }

    public bool CanPlaceBuilding(int x, int y, int width, int height)
    {
        for (int i = 0; i < width; i++)
        {
            for (int j = 0; j < height; j++)
            {
                int checkX = x + i;
                int checkY = y + j;

                if (checkX < 0 || checkX >= gridWidth || checkY < 0 || checkY >= gridHeight)
                    return false;

                if (IsCellOccupied(checkX, checkY))
                    return false;
            }
        }
        return true;
    }

    public void PlaceBuilding(Building building, int x, int y)
    {
        buildingsOnGrid[new Vector2Int(x, y)] = building;
        building.transform.position = GridToWorldPosition(x, y);
    }

    public void HighlightCell(int x, int y, bool valid)
    {
        if (x >= 0 && x < gridWidth && y >= 0 && y < gridHeight)
        {
            grid[x, y].Highlight(valid ? Color.green : Color.red);
        }
    }
}

public class GridCell : MonoBehaviour
{
    public int gridX;
    public int gridY;
    private Renderer cellRenderer;

    public void Initialize(int x, int y)
    {
        gridX = x;
        gridY = y;
        cellRenderer = GetComponent<Renderer>();
    }

    public void Highlight(Color color)
    {
        cellRenderer.material.color = color;
    }
}
```

**Deliverable:** Working grid system with isometric view

---

### THURSDAY: Camera Controls (8 hours)

**File:** `Assets/_Project/Scripts/Core/CameraController.cs`

```csharp
using UnityEngine;

public class CameraController : MonoBehaviour
{
    [Header("Movement")]
    public float panSpeed = 20f;
    public float edgePanThreshold = 50f; // pixels from edge
    public Vector2 panLimit = new Vector2(50, 50);

    [Header("Zoom")]
    public float zoomSpeed = 10f;
    public float minZoom = 5f;
    public float maxZoom = 20f;

    [Header("Rotation")]
    public float rotationSpeed = 100f;

    private Camera cam;
    private Vector3 lastMousePosition;
    private bool isDragging = false;

    private void Start()
    {
        cam = Camera.main;
    }

    private void Update()
    {
        HandleKeyboardMovement();
        HandleMouseMovement();
        HandleTouchMovement();
        HandleZoom();
        HandleRotation();
    }

    private void HandleKeyboardMovement()
    {
        Vector3 move = Vector3.zero;

        if (Input.GetKey(KeyCode.W) || Input.GetKey(KeyCode.UpArrow))
            move.z += panSpeed * Time.deltaTime;
        if (Input.GetKey(KeyCode.S) || Input.GetKey(KeyCode.DownArrow))
            move.z -= panSpeed * Time.deltaTime;
        if (Input.GetKey(KeyCode.A) || Input.GetKey(KeyCode.LeftArrow))
            move.x -= panSpeed * Time.deltaTime;
        if (Input.GetKey(KeyCode.D) || Input.GetKey(KeyCode.RightArrow))
            move.x += panSpeed * Time.deltaTime;

        MoveCamera(move);
    }

    private void HandleMouseMovement()
    {
        // Middle mouse drag
        if (Input.GetMouseButtonDown(2))
        {
            isDragging = true;
            lastMousePosition = Input.mousePosition;
        }
        else if (Input.GetMouseButtonUp(2))
        {
            isDragging = false;
        }

        if (isDragging)
        {
            Vector3 delta = Input.mousePosition - lastMousePosition;
            Vector3 move = new Vector3(-delta.x, 0, -delta.y) * panSpeed * Time.deltaTime * 0.01f;
            MoveCamera(move);
            lastMousePosition = Input.mousePosition;
        }

        // Edge panning
        if (Input.mousePosition.x < edgePanThreshold)
            MoveCamera(Vector3.left * panSpeed * Time.deltaTime);
        if (Input.mousePosition.x > Screen.width - edgePanThreshold)
            MoveCamera(Vector3.right * panSpeed * Time.deltaTime);
        if (Input.mousePosition.y < edgePanThreshold)
            MoveCamera(Vector3.back * panSpeed * Time.deltaTime);
        if (Input.mousePosition.y > Screen.height - edgePanThreshold)
            MoveCamera(Vector3.forward * panSpeed * Time.deltaTime);
    }

    private void HandleTouchMovement()
    {
        if (Input.touchCount == 1)
        {
            Touch touch = Input.GetTouch(0);

            if (touch.phase == TouchPhase.Moved)
            {
                Vector2 delta = touch.deltaPosition;
                Vector3 move = new Vector3(-delta.x, 0, -delta.y) * panSpeed * Time.deltaTime * 0.1f;
                MoveCamera(move);
            }
        }

        // Pinch to zoom (two finger)
        if (Input.touchCount == 2)
        {
            Touch touch1 = Input.GetTouch(0);
            Touch touch2 = Input.GetTouch(1);

            Vector2 touch1PrevPos = touch1.position - touch1.deltaPosition;
            Vector2 touch2PrevPos = touch2.position - touch2.deltaPosition;

            float prevMagnitude = (touch1PrevPos - touch2PrevPos).magnitude;
            float currentMagnitude = (touch1.position - touch2.position).magnitude;

            float difference = currentMagnitude - prevMagnitude;

            Zoom(difference * 0.01f);
        }
    }

    private void HandleZoom()
    {
        float scroll = Input.GetAxis("Mouse ScrollWheel");
        Zoom(scroll * zoomSpeed);
    }

    private void Zoom(float increment)
    {
        float newSize = cam.orthographicSize - increment;
        cam.orthographicSize = Mathf.Clamp(newSize, minZoom, maxZoom);
    }

    private void HandleRotation()
    {
        if (Input.GetKey(KeyCode.Q))
            transform.Rotate(Vector3.up, -rotationSpeed * Time.deltaTime);
        if (Input.GetKey(KeyCode.E))
            transform.Rotate(Vector3.up, rotationSpeed * Time.deltaTime);
    }

    private void MoveCamera(Vector3 move)
    {
        Vector3 newPos = transform.position + move;
        newPos.x = Mathf.Clamp(newPos.x, -panLimit.x, panLimit.x);
        newPos.z = Mathf.Clamp(newPos.z, -panLimit.y, panLimit.y);
        transform.position = newPos;
    }
}
```

**Deliverable:** Smooth camera controls on iOS device

---

### FRIDAY: Backend API + UI (8 hours)

**Morning (4h): Backend REST API**

**File:** `backend/src/server.js`

```javascript
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
require('dotenv').config();

const app = express();

// Middleware
app.use(helmet());
app.use(cors());
app.use(express.json());
app.use(morgan('dev'));

// Health check
app.get('/api/v1/health', (req, res) => {
  res.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  });
});

// Routes
app.use('/api/v1/auth', require('./routes/authRoutes'));
app.use('/api/v1/player', require('./routes/playerRoutes'));
app.use('/api/v1/buildings', require('./routes/buildingRoutes'));

// Error handling
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Something went wrong!' });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`);
});
```

**Afternoon (4h): Basic UI**

**File:** `Assets/_Project/Scripts/UI/MainHUD.cs`

```csharp
using UnityEngine;
using TMPro;

public class MainHUD : MonoBehaviour
{
    [Header("Resource Display")]
    public TextMeshProUGUI goldText;
    public TextMeshProUGUI woodText;
    public TextMeshProUGUI stoneText;
    public TextMeshProUGUI foodText;
    public TextMeshProUGUI waterText;

    [Header("Buttons")]
    public GameObject buildMenuButton;
    public GameObject heroMenuButton;

    private ResourceManager resourceManager;

    private void Start()
    {
        resourceManager = GameManager.Instance.resourceManager;
        resourceManager.OnResourceChanged += UpdateResourceDisplay;

        // Initial display
        UpdateAllResources();
    }

    private void UpdateResourceDisplay(ResourceType type, long amount)
    {
        switch (type)
        {
            case ResourceType.Gold:
                goldText.text = FormatNumber(amount);
                break;
            case ResourceType.Wood:
                woodText.text = FormatNumber(amount);
                break;
            case ResourceType.Stone:
                stoneText.text = FormatNumber(amount);
                break;
            case ResourceType.Food:
                foodText.text = FormatNumber(amount);
                break;
            case ResourceType.Water:
                waterText.text = FormatNumber(amount);
                break;
        }
    }

    private void UpdateAllResources()
    {
        UpdateResourceDisplay(ResourceType.Gold, resourceManager.GetResourceAmount(ResourceType.Gold));
        UpdateResourceDisplay(ResourceType.Wood, resourceManager.GetResourceAmount(ResourceType.Wood));
        UpdateResourceDisplay(ResourceType.Stone, resourceManager.GetResourceAmount(ResourceType.Stone));
        UpdateResourceDisplay(ResourceType.Food, resourceManager.GetResourceAmount(ResourceType.Food));
        UpdateResourceDisplay(ResourceType.Water, resourceManager.GetResourceAmount(ResourceType.Water));
    }

    private string FormatNumber(long number)
    {
        if (number >= 1000000)
            return (number / 1000000f).ToString("0.0") + "M";
        if (number >= 1000)
            return (number / 1000f).ToString("0.0") + "K";
        return number.ToString();
    }

    public void OnBuildMenuClicked()
    {
        GameManager.Instance.ChangeState(GameState.BuildingMenu);
    }
}
```

**Deliverable:** Working UI showing resources

---

### SPRINT 1 REVIEW

**Friday Afternoon:**
- [ ] Demo on iOS device
- [ ] Sprint retrospective
- [ ] Plan Sprint 2

**Success Criteria:**
✅ Unity project builds to iOS
✅ Camera controls work with touch
✅ Grid system renders correctly
✅ Resources display in UI
✅ Backend API responds to health check

**Known Issues to Address:**
- Performance optimization needed
- UI needs polish
- No actual buildings yet

---

## SPRINT 2: BUILDING SYSTEM (Week 2)

### Sprint Goal
**Implement first 3 buildings (Tent, Forester's Hut, Quarry) with placement, construction, and production**

[Continue with Sprint 2-4 detailed plans...]

---

## VELOCITY TRACKING

**Expected Story Points:**
- Sprint 1: 40 points
- Sprint 2: 45 points (team learning curve)
- Sprint 3: 50 points
- Sprint 4: 50 points

**Burndown:**
Track daily progress, adjust scope if behind.

---

**Ready to start? Set up your environment with [DEVELOPMENT_SETUP.md](../DEVELOPMENT_SETUP.md) first!**
