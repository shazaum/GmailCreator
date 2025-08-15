# GmailCreator

Um estudo com Selenium para automatizar a criação de contas do Gmail.
O mapeamento dos campos e a navegação nos elementos de formulario.

A utilização também de proxy e aleatoriedade de user agents.

---

## Table of Contents
1. [Features](#features)
2. [Requirements](#requirements)
3. [Setup and Installation](#setup-and-installation)
4. [Usage](#usage)
5. [Configuration](#configuration)
6. [Troubleshooting](#troubleshooting)

---

### Features

- **Automated Gmail Creation**: Uses Selenium to automate the Gmail sign-up process.
- **Random User Details**: Generates random names, user agents, and other details to create a unique account each time.
- **Proxy Support**: Integrates with `FreeProxy` to avoid IP bans during account creation.
- **Randomized User Agent**: Randomly user agents to prevent detection by Gmail.
- **Logging and Debugging**: Provides banners and notifications for ease of debugging and monitoring the process.

---

### Requirements

1. **Python** 3.6 or higher
2. **Google Chrome** (Browser)
3. **Chromedriver** (Corresponding to your Chrome version)
4. **Python Packages**:
   - `selenium`
   - `requests`
   - `unidecode`
   - `free-proxy` (FreeProxy)
   - `Faker`
   - `fake_useragent`
   - `lxml`

Para instalar os pacotes necessários, use o seguinte comando:

```bash
pip install -r requirements.txt
```

---

### Setup and Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/shazaum/GmailCreator.git
   cd GmailCreator
   ```

2. **Create a virtualenv and Install Required Python Packages**
   ```bash
   python3 -mvenv env
   source env/bin/active
   pip install -r requirements.txt
   ```

---

### Usage

1. **Run the Script**
   - Run command:
     ```bash
     python3 gmailCreator.py
     ```
   - The script start creating a Gmail account using randomly generated details.

2. **Script Flow**
   - Launches Chrome in automated mode.
   - Uses a randomly chosen user agent for each session.
   - Connects to a proxy server to mask the IP address.
   - Creates an account with a randomly generated name and other details.

---

### Configuration

- **Proxy Configuration**: This script uses `FreeProxy` for handling proxies. To change proxy settings, refer to the `FreeProxy` documentation.
- **User Agents**: User agents are stored in a list, and you can add or modify entries to improve randomization or cater to specific needs.

### Code Overview

Here’s a breakdown of the main components:

1. **Proxy Integration**: Uses `FreeProxy` to fetch a proxy IP, reducing the chances of getting blocked.
3. **User Agent Randomization**: Uses the faker library to generate a user agent to emulate various devices and browsers.
4. **Account Creation**: Uses Selenium commands to automate filling out the Gmail sign-up form.
5. **Error Handling**: Contains try-except blocks to manage common issues and delays to prevent detection.

### Troubleshooting

- **Chromedriver Compatibility**: Ensure that the version of Chromedriver matches your installed Chrome version.
- **Proxy Errors**: Some proxies may be unreliable. Restart the script to fetch a new proxy if errors persist.
- **Element Not Found**: If Gmail updates its sign-up form, some elements may need to be updated in the code.

---

### Example Code Snippet

Here’s an example of how the script initializes the WebDriver:

```python
options = ChromeOptions()
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")

# Set a random user agent
user_agent = random.choice(user_agents)
options.add_argument(f"user-agent={user_agent}")

# Set a proxy
proxy = FreeProxy().get()
options.add_argument(f"--proxy-server={proxy}")

driver = webdriver.Chrome(service=ChromeService(), options=options)
```

This code configures Chrome with a randomized user agent and proxy to improve anonymity.

---

### License
Based on the project: https://github.com/ShadowHackrs/Auto-Gmail-Creator

This project is licensed under the MIT License. For more information, 

