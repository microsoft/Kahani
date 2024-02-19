from unittest import TestCase
from prompts import SummariseCulturePrompt
from dotenv import load_dotenv
load_dotenv()

class TestSummariseCulture(TestCase):
        
    def test_empty(self):
        out = SummariseCulturePrompt(
                user_input ="""- The presence of a king indicates a hierarchical societal structure, possibly a monarchy that values royal lineage and authority.
- The name "Moocha Raja" suggests a South Asian or imaginary culture, with "Raja" being a title for a monarch, historically used in the Indian subcontinent.
- A monkey as a significant character points towards regions where monkeys are indigenous and culturally significant, such as India where monkeys are often associated with the Hindu deity Hanuman.
- The exchange of fruits and clothes between the king and the monkey indicates a traditional system of patronage and reward for service rendered.
- The unfavorable view of the monkey by the king's ministers reflects a class or caste distinction, possibly hinting at tension between established court protocol and non-traditional elements.
- Animal fables are a common element in South Asian folklore, which often carry moral lessons about power, friendship, and forgiveness.
- The final reconciliation could reflect cultural values of mercy, recognising faults, and value of companionship over protocol.""",
                debug=True
        )

        print(out)