from langchain import PromptTemplate, FewShotPromptTemplate
from langchain.llms import OpenAI

TEMPLATE = """
List all of the facts contained in each of the following prompts.  Make sure the facts you choose:

- Preserve as much of the original prompt as possible.
- Do not correct any factual inaccuracies.
- Do not include any statements about recommending to talk to a doctor.
- Do not include any statements about decisions
- Do not contain the word "personal" or "doctor"
- Are not redundant.  List as few facts as possible.

Prompt:{prompt}
Facts:{facts}
"""

EXAMPLES = [
    {
        "prompt":
"""
A mastectomy is a surgical procedure to remove one or both breasts, and it is sometimes recommended as a preventive measure for people with a high risk of developing breast cancer, including those with a BRCA gene mutation. This is because having the BRCA mutation can increase a person's risk of developing breast cancer by up to 85%.

A mastectomy can lower the risk of breast cancer, but it does not eliminate the risk entirely. Some people choose to have a mastectomy as a proactive step to reduce their risk, while others may opt for frequent monitoring and other risk-reducing measures instead. The decision to have a mastectomy is a personal one and should be made in consultation with a doctor, taking into account individual health history, family history, and personal preferences.

It is important to note that a mastectomy is a major surgery with potential risks and side effects, and that there are other options for risk reduction, such as increased surveillance and chemoprevention, that may be considered before undergoing a mastectomy.
""",
        "facts":
"""
-A mastectomy is a surgical procedure to remove one or both breasts.
-Having the BRCA mutation can increase a person's risk of developing breast cancer by up to 85%.
-A mastectomy can lower the risk of breast cancer, but it does not eliminate the risk entirely.
-A mastectomy is a major surgery with potential risks and side effects.
-There are other options for risk reduction, such as increased surveillance and chemoprevention, that may be considered before undergoing a mastectomy.
"""
    },
]

llm = OpenAI(model_name="text-davinci-003", n=1, best_of=1)

def get_facts(chat_gpt_output: str) -> list[str]:
    single_prompt= PromptTemplate(
        input_variables=["prompt", "facts"],
        template=TEMPLATE,
    )
    few_shot_prompt = FewShotPromptTemplate(
        examples=EXAMPLES,
        example_prompt=single_prompt,
        input_variables=["prompt"],
        suffix="Prompt:\n{prompt}\nFacts:"
    )
    llm_output: list[LLMResult] = llm.generate([few_shot_prompt.format(prompt=chat_gpt_output)])
    facts_string: str = llm_output.generations[0][0].text
    facts: list[str] = facts_string.splitlines()
    pretty_facts: list[str] = [fact[1:] for fact in facts]

    # remove empty lines
    while "" in pretty_facts:
        pretty_facts.remove("")

    return pretty_facts

if __name__ == '__main__':
    user_input = input("Enter your chatGPT output:\n")
    facts = get_facts(user_input)
    print("BEGIN FACTS BELOW------------------------------------------------------")
    for fact in facts:
        print(fact)
