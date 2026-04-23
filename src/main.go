package main

import (
    "fmt"
    "os"
    "github.com/spf13/cobra"
    "github.com/fatih/color"
    "rivals/internal/scanner"
    "rivals/internal/output"
)

var (
    username   string
    proxyFile  string
    outputFile string
    threads    int
    timeout    int
)

func main() {
    var rootCmd = &cobra.Command{
        Use:   "rivals [username]",
        Short: "Rivals - Advanced OSINT intelligence tool",
        Long:  `Rivals performs comprehensive OSINT gathering across multiple platforms`,
        Args:  cobra.MaximumNArgs(1),
        Run:   runScan,
    }

    rootCmd.Flags().StringVarP(&proxyFile, "proxy", "p", "", "Proxy list file (HTTP/SOCKS5)")
    rootCmd.Flags().StringVarP(&outputFile, "output", "o", "results.json", "Output file (json/csv/txt)")
    rootCmd.Flags().IntVarP(&threads, "threads", "t", 20, "Number of concurrent threads")
    rootCmd.Flags().IntVarP(&timeout, "timeout", "T", 5, "HTTP timeout in seconds")

    if err := rootCmd.Execute(); err != nil {
        color.Red("Error: %v", err)
        os.Exit(1)
    }
}

func runScan(cmd *cobra.Command, args []string) {
    if len(args) > 0 {
        username = args[0]
    }
    
    if username == "" {
        color.Red("Error: username is required")
        cmd.Usage()
        os.Exit(1)
    }

    color.Cyan("\n🚀 Rivals OSINT Scanner v1.0")
    color.Cyan("================================")
    color.Yellow("Target: %s", username)
    color.Yellow("Threads: %d | Timeout: %ds\n", threads, timeout)

    // Initialize scanner
    s := scanner.NewScanner(username, threads, timeout, proxyFile)
    
    // Run scan
    results := s.Run()
    
    // Export results
    if err := output.Export(results, outputFile); err != nil {
        color.Red("Export error: %v", err)
    }
    
    color.Green("\n✅ Scan completed! Results saved to: %s", outputFile)
}
