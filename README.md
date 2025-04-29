# GoRecon

Welcome to **GoRecon**, a professional tool written in Go that allows you to find servers running a specified service (e.g., Gophish), take screenshots of their websites, and generate an elegant report using Tailwind CSS. Perfect for researchers, security professionals, and web enthusiasts!

## ✨ Key Features

- **Server Search**: Uses the Shodan API to find servers running the requested service.
- **Automated Screenshots**: Takes screenshots of websites using `chromedp`, a Chrome-based engine.
- **Stylish Report**: Generates an HTML report with Tailwind CSS, making it easy to read and visually appealing.

## 🚀 Installation

Follow these simple steps to get started:

1. **Clone the Repository**  
   Download the project from your terminal:
   ```bash
   git clone https://github.com/fazelucq1/GoRecon.git
   cd gorecon
   ```

2. **Install Dependencies**  
   Make sure you have Go installed, then run:
   ```bash
   go mod tidy
   ```

3. **Set Up Shodan API Key**  
   - Sign up on [Shodan](https://www.shodan.io/) and get your API key.
   - Set the key as an environment variable:
     ```bash
     export SHODAN_API_KEY=your_api_key
     ```

4. **Install Google Chrome**  
   The tool uses `chromedp`, so ensure Chrome is installed on your system.

## 🛠️ Usage

To search for servers running a specific service and generate a report, run:

```bash
go run cmd/main.go -service Gophish
```

### What Happens?
1. The program searches for servers running "Gophish" via Shodan.
2. Takes a screenshot of each found site and saves it in the `screenshots/` folder.
3. Generates a `report.html` file with all the results.

Open `report.html` in your browser to view the report!

## ⚠️ Legal and Ethical Considerations

This tool is designed for educational and research purposes. Ensure you have permission to access and take screenshots of the servers you are analyzing. Unauthorized use may violate local laws or terms of service.

## 🤝 Contributing

Have an idea to improve the project? Open an issue or submit a pull request! Every contribution is welcome.

## 📜 License

This project is released under the [MIT License](LICENSE). Use it freely, but responsibly!

---

**Ready to explore the web? Start now and discover what's out there!**
