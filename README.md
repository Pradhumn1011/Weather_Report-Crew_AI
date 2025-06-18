# 🌤️ Weather Report Generator with CrewAI

This project is a smart weather report generator that:

- Fetches historical and forecast weather data using **WeatherAPI**
- Saves the data to an **Excel file**
- Generates a natural language summary using **CrewAI**

---

## 📦 Features

✅ Fetch weather data (past & forecast) for a custom date range  
✅ Save structured weather info to Excel  
✅ Use LLM agents via CrewAI to summarize weather trends  

---

## 🛠️ Technologies Used

- Python
- [WeatherAPI](https://www.weatherapi.com/)
- Pandas
- OpenAI GPT-3.5
- CrewAI
- dotenv
- OpenPyXL

---

## 🚀 How to Run

### 1. Clone the repository
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

### 2. Create a virtual environment and install dependencies
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

### 3. Create a .env file in the root directory
OPENAI_API_KEY=your_openai_key_here

Run the script.
