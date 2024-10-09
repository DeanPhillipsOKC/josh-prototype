# JOSH - Jesus-Oriented Shepherd of Hearts (Prototype)

JOSH is a compassionate AI chatbot designed to provide biblically grounded advice and guidance. It reflects the love, kindness, patience, and compassion of Jesus while offering supportive, scripturally-based responses. JOSH is powered by OpenAI and built with Python.

## Features

- Thoughtful, biblically grounded advice, often citing specific scripture.
- Interactive conversations with a Christian perspective.
- Support for OpenAI API integration via UI, `.env` file, or environment variables.

## Requirements

- Python 3.12 or higher
- `requirements.txt` for dependencies

## Setup Instructions

1. **Clone the repository:**

```bash
git clone https://github.com/your-repo/josh.git
cd josh
```

2. Set up a virtual environment (optional but recommended):
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. OpenAI API Key Configuration:
- Using a `.env` file: create a `.env` file in the root directory and add your OpenAI API key:
```bash
OPENAI_API_KEY=your-api-key
```

- Using environment variables:  Set the `OPENAI_API_KEY` in your environment:
```bash
export OPENAI_API_KEY=your-api-key
```

- Via the UI: Run the application and enter your OpenAI API key in the sidebar

5. Running the Application:
To start the application, run:
```bash
streamlit run app.py
```

## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests to improve the project.

## License
This project is licensed under the MIT License.
