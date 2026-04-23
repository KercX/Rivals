package output

import (
    "encoding/csv"
    "encoding/json"
    "fmt"
    "os"
    "rivals/internal/scanner"
    "strings"
    "time"
)

func Export(results *scanner.ScanResult, filename string) error {
    ext := strings.ToLower(filename[strings.LastIndex(filename, "."):])
    
    switch ext {
    case ".json":
        return exportJSON(results, filename)
    case ".csv":
        return exportCSV(results, filename)
    case ".txt":
        return exportTXT(results, filename)
    default:
        return exportJSON(results, filename)
    }
}

func exportJSON(results *scanner.ScanResult, filename string) error {
    data, err := json.MarshalIndent(results, "", "  ")
    if err != nil {
        return err
    }
    return os.WriteFile(filename, data, 0644)
}

func exportCSV(results *scanner.ScanResult, filename string) error {
    file, err := os.Create(filename)
    if err != nil {
        return err
    }
    defer file.Close()
    
    writer := csv.NewWriter(file)
    defer writer.Flush()
    
    writer.Write([]string{"Platform", "URL", "Exists", "Status Code", "Response Time (ms)"})
    
    for _, p := range results.Platforms {
        writer.Write([]string{
            p.Name,
            p.URL,
            fmt.Sprintf("%t", p.Exists),
            fmt.Sprintf("%d", p.StatusCode),
            fmt.Sprintf("%d", p.ResponseTime),
        })
    }
    return nil
}

func exportTXT(results *scanner.ScanResult, filename string) error {
    file, err := os.Create(filename)
    if err != nil {
        return err
    }
    defer file.Close()
    
    file.WriteString(fmt.Sprintf("Rivals OSINT Scan Results\n"))
    file.WriteString(fmt.Sprintf("=========================\n"))
    file.WriteString(fmt.Sprintf("Username: %s\n", results.Username))
    file.WriteString(fmt.Sprintf("Timestamp: %s\n", results.Timestamp.Format(time.RFC3339)))
    file.WriteString(fmt.Sprintf("\nFound Profiles:\n"))
    file.WriteString(fmt.Sprintf("---------------\n"))
    
    for _, p := range results.Platforms {
        if p.Exists {
            file.WriteString(fmt.Sprintf("✓ %s: %s\n", p.Name, p.URL))
        }
    }
    
    return nil
}
