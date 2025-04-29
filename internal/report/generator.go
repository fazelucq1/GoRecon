package report

import (
    "html/template"
    "os"
    "gorecon/internal/search"
)

func GenerateReport(servers []search.Server) error {
    tmpl, err := template.ParseFiles("templates/report.html")
    if err != nil {
        return err
    }

    data := struct {
        Servers []search.Server
    }{
        Servers: servers,
    }

    f, err := os.Create("report.html")
    if err != nil {
        return err
    }
    defer f.Close()

    err = tmpl.Execute(f, data)
    if err != nil {
        return err
    }

    return nil
}
