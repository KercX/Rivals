package scanner

import (
    "context"
    "fmt"
    "net/http"
    "sync"
    "time"
    "encoding/json"
    "github.com/fatih/color"
    "rivals/internal/proxy"
)

type Platform struct {
    Name    string
    URL     string
    Method  string
    Status  bool
}

type ScanResult struct {
    Username    string              `json:"username"`
    Timestamp   time.Time           `json:"timestamp"`
    Platforms   []PlatformResult    `json:"platforms"`
    Summary     ScanSummary         `json:"summary"`
}

type PlatformResult struct {
    Name        string    `json:"name"`
    URL         string    `json:"url"`
    Exists      bool      `json:"exists"`
    StatusCode  int       `json:"status_code"`
    ResponseTime int64    `json:"response_time_ms"`
}

type ScanSummary struct {
    Total       int     `json:"total"`
    Found       int     `json:"found"`
    NotFound    int     `json:"not_found"`
    Errors      int     `json:"errors"`
}

type Scanner struct {
    username    string
    threads     int
    timeout     time.Duration
    proxyPool   *proxy.Pool
    platforms   []Platform
}

func NewScanner(username string, threads int, timeout int, proxyFile string) *Scanner {
    s := &Scanner{
        username: username,
        threads:  threads,
        timeout:  time.Duration(timeout) * time.Second,
    }
    
    if proxyFile != "" {
        s.proxyPool = proxy.NewPool(proxyFile)
    }
    
    s.initPlatforms()
    return s
}

func (s *Scanner) initPlatforms() {
    s.platforms = []Platform{
        {"GitHub", "https://github.com/%s", "GET", false},
        {"Twitter/X", "https://twitter.com/%s", "GET", false},
        {"Instagram", "https://www.instagram.com/%s/", "GET", false},
        {"Reddit", "https://www.reddit.com/user/%s", "GET", false},
        {"LinkedIn", "https://www.linkedin.com/in/%s", "GET", false},
        {"YouTube", "https://youtube.com/@%s", "GET", false},
        {"Facebook", "https://facebook.com/%s", "GET", false},
        {"TikTok", "https://tiktok.com/@%s", "GET", false},
        {"Telegram", "https://t.me/%s", "GET", false},
        {"Pinterest", "https://pinterest.com/%s", "GET", false},
        {"Snapchat", "https://snapchat.com/add/%s", "GET", false},
        {"Medium", "https://medium.com/@%s", "GET", false},
        {"Dev.to", "https://dev.to/%s", "GET", false},
        {"HackerNews", "https://news.ycombinator.com/user?id=%s", "GET", false},
        {"Keybase", "https://keybase.io/%s", "GET", false},
    }
}

func (s *Scanner) Run() *ScanResult {
    results := &ScanResult{
        Username:  s.username,
        Timestamp: time.Now(),
        Platforms: make([]PlatformResult, 0),
        Summary:   ScanSummary{Total: len(s.platforms)},
    }
    
    var wg sync.WaitGroup
    semaphore := make(chan struct{}, s.threads)
    resultChan := make(chan PlatformResult, len(s.platforms))
    
    // Process platforms concurrently
    for _, platform := range s.platforms {
        wg.Add(1)
        go func(p Platform) {
            defer wg.Done()
            semaphore <- struct{}{}
            defer func() { <-semaphore }()
            
            result := s.checkPlatform(p)
            resultChan <- result
            
            if result.Exists {
                color.Green("✓ %s: %s", p.Name, result.URL)
            } else if result.StatusCode == 404 {
                color.Red("✗ %s: Not found", p.Name)
            } else {
                color.Yellow("? %s: Error (HTTP %d)", p.Name, result.StatusCode)
            }
        }(platform)
    }
    
    // Close channel after all goroutines complete
    go func() {
        wg.Wait()
        close(resultChan)
    }()
    
    // Collect results
    for result := range resultChan {
        results.Platforms = append(results.Platforms, result)
        if result.Exists {
            results.Summary.Found++
        } else if result.StatusCode == 404 {
            results.Summary.NotFound++
        } else {
            results.Summary.Errors++
        }
    }
    
    s.printSummary(results)
    return results
}

func (s *Scanner) checkPlatform(platform Platform) PlatformResult {
    start := time.Now()
    url := fmt.Sprintf(platform.URL, s.username)
    
    client := &http.Client{
        Timeout: s.timeout,
    }
    
    // Apply proxy if available
    if s.proxyPool != nil {
        if proxyURL := s.proxyPool.GetNext(); proxyURL != nil {
            client.Transport = &http.Transport{Proxy: http.ProxyURL(proxyURL)}
        }
    }
    
    req, _ := http.NewRequest("GET", url, nil)
    req.Header.Set("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    req.Header.Set("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
    
    resp, err := client.Do(req)
    responseTime := time.Since(start).Milliseconds()
    
    result := PlatformResult{
        Name:         platform.Name,
        URL:          url,
        Exists:       false,
        StatusCode:   0,
        ResponseTime: responseTime,
    }
    
    if err != nil {
        return result
    }
    defer resp.Body.Close()
    
    result.StatusCode = resp.StatusCode
    
    // Check if profile exists (200 OK and not a "user not found" page)
    if resp.StatusCode == 200 {
        // Additional content-based validation can be added here
        result.Exists = true
    }
    
    return result
}

func (s *Scanner) printSummary(results *ScanResult) {
    color.Cyan("\n📊 Scan Summary")
    color.Cyan("==============")
    color.White("Total checked: %d", results.Summary.Total)
    color.Green("Found: %d", results.Summary.Found)
    color.Red("Not found: %d", results.Summary.NotFound)
    color.Yellow("Errors: %d", results.Summary.Errors)
}
