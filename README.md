# Google Complaint Bot GUI

A graphical user interface application for automating the submission of complaints about Google search autocomplete suggestions. Built with Python, Tkinter, and Selenium WebDriver.

## Warning

This application is provided **for educational purposes only**. Using automated tools to submit complaints may violate Google's Terms of Service and could be considered abuse of the system. Use at your own risk.

## Features

- **Graphical Interface**: User-friendly Tkinter GUI
- **Multi-threading**: Responsive UI during automation
- **Batch Processing**: Process multiple queries from a list
- **Detailed Logging**: Real-time log of all actions with timestamps
- **Error Handling**: Continues processing even when individual queries fail
- **Configurable Delays**: Adjustable timing between actions
- **Headless Mode**: Option to run browser invisibly
- **Query Management**: Load and save query lists as JSON or text files

## Requirements

- Python 3.7 or higher
- Google Chrome browser
- Internet connection

## Installation

1. Clone the repository:
```bash
git clone https://github.com/stukenov/google-complaint-bot-gui.git
cd google-complaint-bot-gui
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python google_complaint_bot.py
```

2. **Enter Queries**: Type search queries in the top text area, one per line

3. **Configure Settings**:
   - Delay between actions (recommended: 2-5 seconds)
   - Headless mode (run browser without visible window)

4. **Start Processing**: Click the "Start" button to begin

5. **Monitor Progress**: Watch the execution log for real-time updates

6. **Stop Anytime**: Use the "Stop" button to halt processing

## How It Works

For each query, the application:

1. Opens Google in Chrome browser
2. Enters the search query
3. Waits for autocomplete suggestions to appear
4. Locates the "Report inappropriate predictions" button
5. Selects the target suggestion
6. Fills out the complaint form:
   - Category: "Harassment or bullying of individuals"
   - Message: Standard complaint about artificially generated queries
7. Submits the complaint

## File Menu

- **Load Queries**: Import queries from JSON or text file
- **Save Queries**: Export current queries to JSON or text file
- **Exit**: Close the application

## Example Queries File

JSON format (`example_queries.json`):
```json
{
  "queries": [
    "example search query 1",
    "example search query 2",
    "test automation query"
  ],
  "created": "2024-01-01 12:00:00",
  "description": "Example search queries"
}
```

Text format (one query per line):
```
example search query 1
example search query 2
test automation query
```

## Technical Details

- **GUI Framework**: Tkinter (Python standard library)
- **Browser Automation**: Selenium WebDriver
- **Browser**: Google Chrome (ChromeDriver managed automatically)
- **Language**: Python 3.7+
- **Threading**: Background worker thread for browser automation

## Troubleshooting

**ChromeDriver not found:**
- The webdriver-manager package handles ChromeDriver installation automatically
- Ensure Chrome browser is installed

**Elements not found:**
- Google may have changed their page structure
- Try increasing delays between actions

**Automation blocked:**
- Google may detect and block automated requests
- Use longer delays or different IP address

**CAPTCHA appears:**
- May require manual CAPTCHA solving
- Disable headless mode to interact manually

**Solutions:**
- Increase delays between actions (Settings)
- Disable headless mode to observe the process
- Check your internet connection
- Update Chrome to the latest version

## Project Structure

```
.
├── google_complaint_bot.py  # Main application
├── example_queries.json     # Example query list
├── requirements.txt         # Python dependencies
├── LICENSE                  # MIT License
└── README.md               # This file
```

## Legal and Ethical Considerations

- This tool automates interaction with Google's services
- Review Google's Terms of Service before use
- Consider the ethical implications of automated complaint submissions
- The author assumes no liability for misuse of this tool
- Intended for educational purposes only

## License

MIT License - Copyright (c) 2025 Saken Tukenov

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## Disclaimer

This software is provided "as is" without warranty of any kind. The author is not responsible for any use of this software. Use responsibly and at your own risk. 