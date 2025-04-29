package screenshot

import (
    "context"
    "fmt"
    "log"
    "os"
    "time"
    "github.com/chromedp/chromedp"
)

func TakeScreenshot(url, id string) error {
    ctx, cancel := chromedp.NewContext(context.Background())
    defer cancel()

    ctx, cancel = context.WithTimeout(ctx, 30*time.Second)
    defer cancel()

    var buf []byte
    err := chromedp.Run(ctx,
        chromedp.Navigate(url),
        chromedp.WaitVisible(`body`, chromedp.ByQuery),
        chromedp.CaptureScreenshot(&buf),
    )
    if err != nil {
        return err
    }

    filename := fmt.Sprintf("screenshots/%s.png", id)
    if err := os.MkdirAll("screenshots", 0755); err != nil {
        return err
    }
    err = os.WriteFile(filename, buf, 0644)
    if err != nil {
        return err
    }

    log.Printf("Screenshot saved: %s", filename)
    return nil
}
