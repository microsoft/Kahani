from unittest import TestCase
from prompts import ExtractCulturePrompt
from dotenv import load_dotenv
load_dotenv()

class TestExtractCulture(TestCase):

    def test_empty(self):
        out = ExtractCulturePrompt(
            cultural_context="""- The presence of a king indicates a hierarchical societal structure, possibly a monarchy that values royal lineage and authority.
- The name "Moocha Raja" suggests a South Asian culture, with "Raja" being a title for a monarch, historically used in the Indian subcontinent.
- A monkey as a significant character points towards regions where monkeys are indigenous and culturally significant, such as India where monkeys are often associated with the Hindu deity Hanuman.
- The exchange of fruits and clothes between the king and the monkey indicates a traditional system of patronage and reward for service rendered.
- The unfavorable view of the monkey by the king's ministers reflects a class or caste distinction, possibly hinting at tension between established court protocol and non-traditional elements.
- Animal fables are a common element in South Asian folklore, which often carry moral lessons about power, friendship, and forgiveness.
- The final reconciliation could reflect cultural values of mercy, recognizing faults, and the value of companionship over protocol.""",
            user_input="Write a story where a monkey sneaks into King Moocha Raja's bedroom through an open window. The monkey starts fanning the king while he sleeps, and they become friends. The king likes the monkey and gives it fruits and clothes. But the king's ministers don't like the monkey. One day, the monkey tries to hit a fly on the king's nose and hurts the king by mistake. The king gets mad and sends the monkey away. Later, the king feels bad and misses the monkey, so he tries to get it back. In the end, they reunite and the king realizes he was too harsh.",
            debug=True
        )

        print(out)

#     def test_update(self):
#         out = ExtractCulturePrompt(
#             cultural_context="""
# - Salma might be of Middle Eastern or South Asian descent, as "Abu" can signify father or paternal grandfather in Arabic or a term of endearment.
# - The term suggests a close family bond, respecting elders.
# - Visiting family during summer holidays could indicate the importance of family unity and spending time with extended family in her culture.
# - Enjoyment of warm weather might imply she's accustomed to or culturally aligns with a hot climate.""",
#             user_input="Salma likes to eat kulfis",
#             debug=True
#         )

#         print(out)

        self.assertIn("Moocha", out)
        # self.assertIn("Arabic", out)
