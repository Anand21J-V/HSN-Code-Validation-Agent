import os
import pandas as pd
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain_groq import ChatGroq

os.environ["GROQ_API_KEY"] = "your_groq_api_key"  


df = pd.read_excel("HSN_SAC.xlsx")

# Debug original columns
print("📊 Raw columns from Excel:", df.columns.tolist())

# Normalize and clean column names
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "")

# Ensure required columns exist
if "hsncode" not in df.columns or "description" not in df.columns:
    raise ValueError("❌ Excel file must contain columns: 'HSN Code' and 'Description'")

# Rename and prepare DataFrame
df = df.rename(columns={"hsncode": "HSNCode", "description": "Description"})
df["HSNCode"] = df["HSNCode"].astype(str).str.strip()
df = df.set_index("HSNCode")

# ====== STEP 3: Validation Logic ======
def validate_hsn(code: str) -> str:
    code = code.strip()
    if not code.isdigit() or not (2 <= len(code) <= 8):
        return f"❌ '{code}' is an invalid format (must be numeric and 2–8 digits)."
    elif code in df.index:
        return f"✅ '{code}' is valid: {df.loc[code]['Description']}"
    else:
        # Optional: Check parent hierarchy
        for i in range(len(code) - 2, 1, -2):
            parent = code[:i]
            if parent in df.index:
                return f"⚠️ '{code}' not found. Closest match: '{parent}' → {df.loc[parent]['Description']}"
        return f"⚠️ '{code}' not found in master data."

# ====== STEP 4: Create LangChain Tool ======
hsn_tool = Tool(
    name="ValidateHSNCode",
    func=validate_hsn,
    description="Use this to validate an HSN code from the Excel master data. Input must be a single numeric code."
)

# ====== STEP 5: Setup LangChain Agent with Groq ======
llm = ChatGroq(
    model="llama3-70b-8192",  # LLaMA 3.3 70B Versatile
    temperature=0.2
)

agent = initialize_agent(
    tools=[hsn_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# ====== STEP 6: Interactive Loop ======
print("🧠 HSN Code Validation Agent (Groq + LLaMA 3.3 70B)")
print("💬 Type 'exit' to stop.")

while True:
    query = input("\nAsk your agent (e.g., Validate 0101, 99999999): ")
    if query.lower().strip() in ["exit", "quit"]:
        print("👋 Exiting agent.")
        break
    try:
        response = agent.run(query)
        print("\n🔍 Result:\n", response)
    except Exception as e:
        print("⚠️ Error:", e)
