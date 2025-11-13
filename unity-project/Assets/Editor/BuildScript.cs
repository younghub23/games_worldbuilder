using UnityEditor;
using UnityEditor.Build.Reporting;
using UnityEngine;
using System.IO;

/// <summary>
/// Build automation scripts for command-line builds and CI/CD
/// These methods can be called from Unity CLI or from Unity Editor menu
///
/// Usage from command line:
/// unity-editor -quit -batchmode -executeMethod BuildScript.BuildIOS
/// </summary>
public class BuildScript
{
    // Build output directory
    private static readonly string BuildPath = Path.Combine(
        Directory.GetParent(Application.dataPath).FullName,
        "Builds"
    );

    /// <summary>
    /// Build for iOS platform
    /// Menu: Build → iOS Build
    /// CLI: -executeMethod BuildScript.BuildIOS
    /// </summary>
    [MenuItem("Build/iOS Build")]
    public static void BuildIOS()
    {
        string outputPath = Path.Combine(BuildPath, "iOS");

        BuildPlayerOptions options = new BuildPlayerOptions
        {
            scenes = GetScenePaths(),
            locationPathName = outputPath,
            target = BuildTarget.iOS,
            options = BuildOptions.None
        };

        ExecuteBuild(options, "iOS");
    }

    /// <summary>
    /// Build for iOS platform (Development)
    /// Menu: Build → iOS Build (Development)
    /// CLI: -executeMethod BuildScript.BuildIOSDevelopment
    /// </summary>
    [MenuItem("Build/iOS Build (Development)")]
    public static void BuildIOSDevelopment()
    {
        string outputPath = Path.Combine(BuildPath, "iOS-Dev");

        BuildPlayerOptions options = new BuildPlayerOptions
        {
            scenes = GetScenePaths(),
            locationPathName = outputPath,
            target = BuildTarget.iOS,
            options = BuildOptions.Development | BuildOptions.AllowDebugging
        };

        ExecuteBuild(options, "iOS Development");
    }

    /// <summary>
    /// Build for Android platform
    /// Menu: Build → Android Build
    /// CLI: -executeMethod BuildScript.BuildAndroid
    /// </summary>
    [MenuItem("Build/Android Build")]
    public static void BuildAndroid()
    {
        string outputPath = Path.Combine(BuildPath, "Android", "empire-genesis.apk");

        BuildPlayerOptions options = new BuildPlayerOptions
        {
            scenes = GetScenePaths(),
            locationPathName = outputPath,
            target = BuildTarget.Android,
            options = BuildOptions.None
        };

        ExecuteBuild(options, "Android");
    }

    /// <summary>
    /// Build for Android platform (Development)
    /// Menu: Build → Android Build (Development)
    /// CLI: -executeMethod BuildScript.BuildAndroidDevelopment
    /// </summary>
    [MenuItem("Build/Android Build (Development)")]
    public static void BuildAndroidDevelopment()
    {
        string outputPath = Path.Combine(BuildPath, "Android", "empire-genesis-dev.apk");

        BuildPlayerOptions options = new BuildPlayerOptions
        {
            scenes = GetScenePaths(),
            locationPathName = outputPath,
            target = BuildTarget.Android,
            options = BuildOptions.Development | BuildOptions.AllowDebugging
        };

        ExecuteBuild(options, "Android Development");
    }

    /// <summary>
    /// Build all platforms sequentially
    /// Menu: Build → Build All Platforms
    /// CLI: -executeMethod BuildScript.BuildAll
    /// </summary>
    [MenuItem("Build/Build All Platforms")]
    public static void BuildAll()
    {
        Debug.Log("=== Building All Platforms ===");

        BuildIOS();
        BuildAndroid();

        Debug.Log("=== All Builds Complete ===");
    }

    /// <summary>
    /// Get all scenes in build settings
    /// </summary>
    private static string[] GetScenePaths()
    {
        var scenes = new string[EditorBuildSettings.scenes.Length];

        for (int i = 0; i < scenes.Length; i++)
        {
            scenes[i] = EditorBuildSettings.scenes[i].path;
        }

        // Validate we have scenes
        if (scenes.Length == 0)
        {
            Debug.LogError("No scenes found in Build Settings! Add scenes via File → Build Settings");
            return new[] { "Assets/Scenes/SampleScene.unity" }; // Fallback
        }

        return scenes;
    }

    /// <summary>
    /// Execute a build with proper logging and error handling
    /// </summary>
    private static void ExecuteBuild(BuildPlayerOptions options, string platformName)
    {
        Debug.Log($"=== Starting {platformName} Build ===");
        Debug.Log($"Output: {options.locationPathName}");
        Debug.Log($"Scenes: {string.Join(", ", options.scenes)}");

        // Ensure build directory exists
        Directory.CreateDirectory(Path.GetDirectoryName(options.locationPathName));

        // Execute build
        BuildReport report = BuildPipeline.BuildPlayer(options);
        BuildSummary summary = report.summary;

        // Log results
        if (summary.result == BuildResult.Succeeded)
        {
            Debug.Log($"✓ {platformName} build succeeded!");
            Debug.Log($"  Size: {summary.totalSize / (1024 * 1024)} MB");
            Debug.Log($"  Time: {summary.totalTime.TotalSeconds:F1} seconds");
            Debug.Log($"  Output: {summary.outputPath}");

            // Exit with success code for CI/CD
            if (Application.isBatchMode)
            {
                EditorApplication.Exit(0);
            }
        }
        else
        {
            Debug.LogError($"✗ {platformName} build failed!");
            Debug.LogError($"  Result: {summary.result}");
            Debug.LogError($"  Errors: {summary.totalErrors}");
            Debug.LogError($"  Warnings: {summary.totalWarnings}");

            // Print detailed errors
            foreach (BuildStep step in report.steps)
            {
                foreach (BuildStepMessage message in step.messages)
                {
                    if (message.type == LogType.Error || message.type == LogType.Exception)
                    {
                        Debug.LogError($"  {message.content}");
                    }
                }
            }

            // Exit with error code for CI/CD
            if (Application.isBatchMode)
            {
                EditorApplication.Exit(1);
            }
        }
    }

    /// <summary>
    /// Validate build settings before building
    /// Menu: Build → Validate Build Settings
    /// CLI: -executeMethod BuildScript.ValidateBuildSettings
    /// </summary>
    [MenuItem("Build/Validate Build Settings")]
    public static void ValidateBuildSettings()
    {
        Debug.Log("=== Validating Build Settings ===");

        bool isValid = true;

        // Check scenes
        if (EditorBuildSettings.scenes.Length == 0)
        {
            Debug.LogError("✗ No scenes in build settings");
            isValid = false;
        }
        else
        {
            Debug.Log($"✓ {EditorBuildSettings.scenes.Length} scenes in build");
        }

        // Check product name
        if (string.IsNullOrEmpty(PlayerSettings.productName))
        {
            Debug.LogError("✗ Product name not set");
            isValid = false;
        }
        else
        {
            Debug.Log($"✓ Product name: {PlayerSettings.productName}");
        }

        // Check bundle identifier (iOS/Android)
        if (string.IsNullOrEmpty(PlayerSettings.applicationIdentifier))
        {
            Debug.LogError("✗ Bundle identifier not set");
            isValid = false;
        }
        else
        {
            Debug.Log($"✓ Bundle identifier: {PlayerSettings.applicationIdentifier}");
        }

        // Check version
        Debug.Log($"  Version: {PlayerSettings.bundleVersion}");
        Debug.Log($"  iOS Build: {PlayerSettings.iOS.buildNumber}");
        Debug.Log($"  Android Version Code: {PlayerSettings.Android.bundleVersionCode}");

        if (isValid)
        {
            Debug.Log("=== Build Settings Valid ===");
        }
        else
        {
            Debug.LogError("=== Build Settings Invalid ===");
            if (Application.isBatchMode)
            {
                EditorApplication.Exit(1);
            }
        }
    }

    /// <summary>
    /// Increment version numbers for new build
    /// Menu: Build → Increment Version
    /// CLI: -executeMethod BuildScript.IncrementVersion
    /// </summary>
    [MenuItem("Build/Increment Version")]
    public static void IncrementVersion()
    {
        // Parse current version
        string currentVersion = PlayerSettings.bundleVersion;
        string[] parts = currentVersion.Split('.');

        if (parts.Length == 3 && int.TryParse(parts[2], out int patch))
        {
            patch++;
            PlayerSettings.bundleVersion = $"{parts[0]}.{parts[1]}.{patch}";
        }

        // Increment iOS build number
        int iosBuild = int.Parse(PlayerSettings.iOS.buildNumber);
        PlayerSettings.iOS.buildNumber = (iosBuild + 1).ToString();

        // Increment Android version code
        int androidCode = PlayerSettings.Android.bundleVersionCode;
        PlayerSettings.Android.bundleVersionCode = androidCode + 1;

        Debug.Log($"Version updated to: {PlayerSettings.bundleVersion}");
        Debug.Log($"iOS build: {PlayerSettings.iOS.buildNumber}");
        Debug.Log($"Android code: {PlayerSettings.Android.bundleVersionCode}");

        AssetDatabase.SaveAssets();
    }
}
