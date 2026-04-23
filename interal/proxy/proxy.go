package proxy

import (
    "bufio"
    "net/url"
    "os"
    "sync/atomic"
)

type Pool struct {
    proxies []*url.URL
    counter uint64
}

func NewPool(filename string) *Pool {
    file, err := os.Open(filename)
    if err != nil {
        return &Pool{proxies: []*url.URL{}}
    }
    defer file.Close()
    
    proxies := []*url.URL{}
    scanner := bufio.NewScanner(file)
    for scanner.Scan() {
        proxyURL, err := url.Parse(scanner.Text())
        if err == nil {
            proxies = append(proxies, proxyURL)
        }
    }
    
    return &Pool{proxies: proxies}
}

func (p *Pool) GetNext() *url.URL {
    if len(p.proxies) == 0 {
        return nil
    }
    idx := atomic.AddUint64(&p.counter, 1) % uint64(len(p.proxies))
    return p.proxies[idx]
}
