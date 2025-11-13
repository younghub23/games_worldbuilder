using UnityEditor;
using UnityEngine;
using System.IO;
using System.Collections.Generic;

/// <summary>
/// Data import tools for automating ScriptableObject creation from JSON/CSV files
/// This enables Claude Code to edit data files, and you to import them into Unity
///
/// Workflow:
/// 1. Claude: Creates/edits JSON files with game data (buildings, heroes, items)
/// 2. You: Click Tools → Import Game Data in Unity
/// 3. Script: Automatically creates/updates ScriptableObjects
/// 4. Result: No manual Inspector work needed!
/// </summary>
public class DataImportTools : EditorWindow
{
    private const string DataPath = "Assets/Resources/Data";
    private const string ConfigPath = "Assets/ScriptableObjects";

    [MenuItem("Tools/Import Game Data")]
    public static void ShowWindow()
    {
        GetWindow<DataImportTools>("Data Import");
    }

    private void OnGUI()
    {
        GUILayout.Label("Import Game Data from JSON", EditorStyles.boldLabel);
        GUILayout.Space(10);

        EditorGUILayout.HelpBox(
            "Import data from JSON files created by Claude Code into ScriptableObjects.\n\n" +
            "Place JSON files in Assets/Resources/Data/",
            MessageType.Info
        );

        GUILayout.Space(10);

        if (GUILayout.Button("Import All Data", GUILayout.Height(40)))
        {
            ImportAllData();
        }

        GUILayout.Space(10);

        EditorGUILayout.LabelField("Individual Imports", EditorStyles.boldLabel);

        if (GUILayout.Button("Import Buildings"))
        {
            ImportBuildings();
        }

        if (GUILayout.Button("Import Heroes"))
        {
            ImportHeroes();
        }

        if (GUILayout.Button("Import Items"))
        {
            ImportItems();
        }

        if (GUILayout.Button("Import Quests"))
        {
            ImportQuests();
        }

        GUILayout.Space(20);

        if (GUILayout.Button("Validate All Configs"))
        {
            ValidateAllConfigs();
        }
    }

    /// <summary>
    /// Import all data types at once
    /// CLI: -executeMethod DataImportTools.ImportAllData
    /// </summary>
    [MenuItem("Tools/Import All Game Data")]
    public static void ImportAllData()
    {
        Debug.Log("=== Importing All Game Data ===");

        ImportBuildings();
        ImportHeroes();
        ImportItems();
        ImportQuests();

        Debug.Log("=== Import Complete ===");
        AssetDatabase.SaveAssets();
        AssetDatabase.Refresh();
    }

    /// <summary>
    /// Import building configurations from JSON
    /// Expected format: Assets/Resources/Data/buildings.json
    /// </summary>
    public static void ImportBuildings()
    {
        string jsonPath = Path.Combine(Application.dataPath, "Resources/Data/buildings.json");

        if (!File.Exists(jsonPath))
        {
            Debug.LogWarning($"Buildings JSON not found: {jsonPath}");
            return;
        }

        try
        {
            string json = File.ReadAllText(jsonPath);
            BuildingDataArray data = JsonUtility.FromJson<BuildingDataArray>($"{{\"buildings\":{json}}}");

            string outputFolder = Path.Combine(Application.dataPath, "ScriptableObjects/Buildings");
            Directory.CreateDirectory(outputFolder);

            int count = 0;
            foreach (var buildingData in data.buildings)
            {
                string assetPath = $"Assets/ScriptableObjects/Buildings/{buildingData.id}.asset";

                // Try to load existing asset
                BuildingConfig config = AssetDatabase.LoadAssetAtPath<BuildingConfig>(assetPath);

                if (config == null)
                {
                    // Create new asset
                    config = ScriptableObject.CreateInstance<BuildingConfig>();
                    AssetDatabase.CreateAsset(config, assetPath);
                    Debug.Log($"Created new building config: {buildingData.id}");
                }
                else
                {
                    Debug.Log($"Updated building config: {buildingData.id}");
                }

                // Update properties (example - adjust based on your actual BuildingConfig class)
                config.name = buildingData.name;
                // config.buildingName = buildingData.name;
                // config.description = buildingData.description;
                // config.goldCost = buildingData.cost.gold;
                // config.woodCost = buildingData.cost.wood;
                // config.buildTime = buildingData.buildTime;

                EditorUtility.SetDirty(config);
                count++;
            }

            AssetDatabase.SaveAssets();
            Debug.Log($"✓ Imported {count} buildings");
        }
        catch (System.Exception e)
        {
            Debug.LogError($"Failed to import buildings: {e.Message}");
        }
    }

    /// <summary>
    /// Import hero configurations from JSON
    /// Expected format: Assets/Resources/Data/heroes.json
    /// </summary>
    public static void ImportHeroes()
    {
        string jsonPath = Path.Combine(Application.dataPath, "Resources/Data/heroes.json");

        if (!File.Exists(jsonPath))
        {
            Debug.LogWarning($"Heroes JSON not found: {jsonPath}");
            return;
        }

        Debug.Log("✓ Hero import template ready (implement based on HeroConfig class)");
        // TODO: Implement similar to ImportBuildings once HeroConfig is defined
    }

    /// <summary>
    /// Import item configurations from JSON
    /// Expected format: Assets/Resources/Data/items.json
    /// </summary>
    public static void ImportItems()
    {
        string jsonPath = Path.Combine(Application.dataPath, "Resources/Data/items.json");

        if (!File.Exists(jsonPath))
        {
            Debug.LogWarning($"Items JSON not found: {jsonPath}");
            return;
        }

        Debug.Log("✓ Item import template ready (implement based on ItemConfig class)");
        // TODO: Implement similar to ImportBuildings once ItemConfig is defined
    }

    /// <summary>
    /// Import quest configurations from JSON
    /// Expected format: Assets/Resources/Data/quests.json
    /// </summary>
    public static void ImportQuests()
    {
        string jsonPath = Path.Combine(Application.dataPath, "Resources/Data/quests.json");

        if (!File.Exists(jsonPath))
        {
            Debug.LogWarning($"Quests JSON not found: {jsonPath}");
            return;
        }

        Debug.Log("✓ Quest import template ready (implement based on QuestConfig class)");
        // TODO: Implement similar to ImportBuildings once QuestConfig is defined
    }

    /// <summary>
    /// Validate all ScriptableObject configurations
    /// CLI: -executeMethod DataImportTools.ValidateAllConfigs
    /// </summary>
    [MenuItem("Tools/Validate All Configs")]
    public static void ValidateAllConfigs()
    {
        Debug.Log("=== Validating All Configs ===");

        bool allValid = true;

        // Find all ScriptableObjects in project
        string[] guids = AssetDatabase.FindAssets("t:ScriptableObject", new[] { "Assets/ScriptableObjects" });

        Debug.Log($"Found {guids.Length} ScriptableObjects to validate");

        foreach (string guid in guids)
        {
            string path = AssetDatabase.GUIDToAssetPath(guid);
            ScriptableObject obj = AssetDatabase.LoadAssetAtPath<ScriptableObject>(path);

            if (obj == null)
            {
                Debug.LogError($"✗ Failed to load: {path}");
                allValid = false;
                continue;
            }

            // Basic validation (extend based on your needs)
            if (string.IsNullOrEmpty(obj.name))
            {
                Debug.LogError($"✗ ScriptableObject has no name: {path}");
                allValid = false;
            }

            // Add type-specific validation here
            // Example:
            // if (obj is BuildingConfig building)
            // {
            //     if (building.goldCost < 0)
            //         Debug.LogError($"✗ {building.name} has negative gold cost");
            // }
        }

        if (allValid)
        {
            Debug.Log("=== All Configs Valid ===");
        }
        else
        {
            Debug.LogError("=== Validation Failed ===");
        }
    }

    /// <summary>
    /// Export current ScriptableObjects to JSON for backup
    /// CLI: -executeMethod DataImportTools.ExportToJSON
    /// </summary>
    [MenuItem("Tools/Export Configs to JSON")]
    public static void ExportToJSON()
    {
        string outputPath = Path.Combine(Application.dataPath, "../Exports");
        Directory.CreateDirectory(outputPath);

        // Example: Export all buildings
        var buildings = FindAllAssets<BuildingConfig>();
        if (buildings.Count > 0)
        {
            string json = JsonUtility.ToJson(new { buildings }, prettyPrint: true);
            File.WriteAllText(Path.Combine(outputPath, "buildings.json"), json);
            Debug.Log($"✓ Exported {buildings.Count} buildings to {outputPath}/buildings.json");
        }

        AssetDatabase.Refresh();
        Debug.Log("=== Export Complete ===");
    }

    /// <summary>
    /// Find all assets of a specific type
    /// </summary>
    private static List<T> FindAllAssets<T>() where T : ScriptableObject
    {
        List<T> assets = new List<T>();
        string[] guids = AssetDatabase.FindAssets($"t:{typeof(T).Name}");

        foreach (string guid in guids)
        {
            string path = AssetDatabase.GUIDToAssetPath(guid);
            T asset = AssetDatabase.LoadAssetAtPath<T>(path);
            if (asset != null)
            {
                assets.Add(asset);
            }
        }

        return assets;
    }
}

// ===== Data structures for JSON deserialization =====
// These match the format Claude Code will create in JSON files

[System.Serializable]
public class BuildingDataArray
{
    public BuildingData[] buildings;
}

[System.Serializable]
public class BuildingData
{
    public string id;
    public string name;
    public string description;
    public BuildingCost cost;
    public int buildTime;
    public int maxLevel;
}

[System.Serializable]
public class BuildingCost
{
    public int gold;
    public int wood;
    public int stone;
}

// TODO: Define these as you create the actual ScriptableObject classes
// These are placeholders for the import system
public class BuildingConfig : ScriptableObject
{
    // Will be implemented in Assets/Scripts/ScriptableObjects/BuildingConfig.cs
}

public class HeroConfig : ScriptableObject
{
    // Will be implemented in Assets/Scripts/ScriptableObjects/HeroConfig.cs
}

public class ItemConfig : ScriptableObject
{
    // Will be implemented in Assets/Scripts/ScriptableObjects/ItemConfig.cs
}

public class QuestConfig : ScriptableObject
{
    // Will be implemented in Assets/Scripts/ScriptableObjects/QuestConfig.cs
}
