package main

import (
    "flag"
    "fmt"
    "log"
    "os"
    "gorecon/internal/report"
    "gorecon/internal/search"
    "gorecon/internal/screenshot"
)

func main() {
    service := flag.String("service", "", "Service to search for (e.g., Gophish)")
    flag.Parse()

    if *service == "" {
        fmt.Println("Please provide a service name using the -service flag.")
        os.Exit(1)
    }

    servers, err := search.FindServers(*service)
    if err != nil {
        log.Fatalf("Error searching for servers: %v", err)
    }

    for _, server := range servers {
        err := screenshot.TakeScreenshot(server.URL, server.ID)
        if err != nil {
            log.Printf("Error taking screenshot for %s: %v", server.URL, err)
        }
    }

    err = report.GenerateReport(servers)
    if err != nil {
        log.Fatalf("Error generating report: %v", err)
    }

    fmt.Println("Report generated successfully as 'report.html'.")
}
