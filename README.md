
# HSN Code Validation Agent

## Overview

This project provides an HSN (Harmonized System of Nomenclature) code validation system using LangChain and Groq. The tool validates and checks HSN codes against a provided Excel master file and interacts with users to confirm the correctness of the input codes.

The system uses a LLaMA 3.3 70B model to validate and process user queries in an interactive loop, leveraging Groq for model execution.

## Features

* **HSN Code Validation**: Validate an HSN code based on a predefined Excel master list.
* **Flexible Hierarchy Matching**: If the exact HSN code isn't found, the system checks the closest parent codes.
* **Interactive Agent**: The agent runs in an interactive loop where users can input codes for validation.
* **Customizable**: Easily update the Excel file to include new HSN codes or descriptions.

## Requirements

* Python 3.x
* `pandas`: For reading and processing the Excel file.
* `langchain`: For building the language chain and tools.
* `langchain_groq`: For utilizing Groq and LLaMA models for the agent.
* `openai` (if using OpenAI's models instead of Groq for a different agent setup).
* A valid `GROQ_API_KEY` for Groq API access.

## Installation

1. Install required packages:

   ```bash
   pip install pandas langchain langchain_groq openai
   ```

2. Obtain an API key from [Groq](https://groq.com/) and set it as an environment variable:

   ```bash
   export GROQ_API_KEY="your_groq_api_key"
   ```

3. Ensure you have the master Excel file `HSN_SAC.xlsx` containing the HSN codes and their corresponding descriptions.

## Setup

1. Prepare the Excel file (`HSN_SAC.xlsx`) with at least two columns:

   * `HSN Code`
   * `Description`

2. Make sure the column names are in the proper format (no spaces, lowercase, etc.), as the code normalizes them.

3. The code reads this file and initializes the HSN code validation tool using LangChain, linking it with the Groq API.

## Usage

1. Start the agent by running the script:

   ```bash
   python hsn_validation_agent.py
   ```

2. Once running, you will see the interactive prompt. Type an HSN code to validate or type `exit` to stop.

   Example interaction:

   ```bash
   🧠 HSN Code Validation Agent (Groq + LLaMA 3.3 70B)
   💬 Type 'exit' to stop.

   Ask your agent (e.g., Validate 0101, 99999999): 0101
   🔍 Result:
   ✅ '0101' is valid: [Description for 0101]
   ```

3. If an invalid code is entered, or a close match is found, the system will notify you with the appropriate message.

## How It Works

1. **Reading the Excel File**: The system reads the Excel file to extract the HSN codes and descriptions.

2. **Data Normalization**: The column names are stripped of spaces and converted to lowercase to ensure proper matching.

3. **Validation**: The `validate_hsn` function checks if the provided HSN code exists in the data, and if not, attempts to find the closest parent code.

4. **Agent Setup**: LangChain initializes a tool with the validation function and sets up an agent using Groq's LLaMA 3.3 model to process user queries.

5. **Interactive Querying**: The agent listens for user input, processes it using the validation logic, and provides a response.

## Customization

* **HSN Code Data**: Update the `HSN_SAC.xlsx` file with new HSN codes or descriptions.
* **Model Customization**: You can replace the LLaMA model used in the `ChatGroq` function with any other supported models by Groq or LangChain.
* **Agent Logic**: Modify the validation function to include more sophisticated validation or error handling as needed.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Anand Kumar Vishwakarma

