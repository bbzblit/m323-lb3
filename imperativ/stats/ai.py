from datetime import date
from .helper import _from_csv 
from langchain.agents import create_pandas_dataframe_agent
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
from langchain.callbacks import get_openai_callback

def ask_ai(question: str, date: date):
    df = _from_csv(date)
    df = df.drop("FAHRT_ID", axis=1)
    df = df.drop("Unnamed: 0", axis=1)

    sufix = f"""
The dataframe contains a list of all stops of trains on the given day.
Please note that the the trains drive in both directions and multiple times a day.
SO always return unique values for STOP_NAME if you want to get the correct results.
You can identify if a stop is the start of the line when there is no EXPECTED_ARRIVAL, and if it is the end of the line when there is no EXPECTED_DEPARTURE. 
There are the following columns in the dataframe:
LINIEN_TEXT: The number of the train. It is always one singel word. For example IR75.
AN_PROGNOSE: The time the train arrives at the station.
AB_PROGNOSE: The time the train departs from the station.
HALTESTELLEN_NAME: The name of the station where the train stops.
DELAY_ANKUFT: The delay of the train in seconds at the arrival.
DELAY_ABFAHRT: The delay of the train in seconds at the departure.


This is the result of `print(df.head())`: {df.head()}

Please never return the generated code directly.
"""

    agent = create_pandas_dataframe_agent(ChatOpenAI(temperature=0),df, AgentType.OPENAI_FUNCTIONS, suffix=sufix, include_df_in_prompt=None, handle_parsing_errors="Please make sure that the tool input hase to be a valid JSON in the format {query: \"generated code\"}")

    return agent.run(question)
