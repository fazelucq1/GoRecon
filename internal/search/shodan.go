package search

import (
    "fmt"
    "os"
    shodan "github.com/shodan/shodan-go"
)

type Server struct {
    ID  string
    URL string
}

func FindServers(service string) ([]Server, error) {
    apiKey := os.Getenv("SHODAN_API_KEY")
    if apiKey == "" {
        return nil, fmt.Errorf("SHODAN_API_KEY environment variable not set")
    }

    client := shodan.NewClient(nil, apiKey)
    query := fmt.Sprintf("product:%s", service)
    result, err := client.Search(query, nil)
    if err != nil {
        return nil, err
    }

    var servers []Server
    for _, match := range result.Matches {
        url := fmt.Sprintf("http://%s:%d", match.IPStr, match.Port)
        servers = append(servers, Server{ID: match.IPStr, URL: url})
    }

    return servers, nil
}
