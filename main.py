import json
from difflib import get_close_matches

# Load the knowledge base from the json file
def load_knowledge_base(file_path: str) -> dict:
  with open(file_path, 'r') as file:
    data: dict = json.load(file)
    return data
    
#Save the dictionary to the knowledge base so we can have old responses in the memory
def save_knowledge_base(file_path: str, data: dict):
  with open(file_path, 'w') as file:
    json.dump(data,file, indent=2)

def find_best_match(user_question: str, questions: list[str]) -> str | None:
  matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6) #n=3 will return top 3 answers
  return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
  for q in knowledge_base["questions"]:
    if q["question"] == question:
      return q["answer"]
    return None
   
def chat_bot():
   knowledge_base: dict = load_knowledge_base('knowledgebase.json')
   while True:
      user_input: str = input('You: ')

      if user_input.lower() = 'quit':
         break
        
      best_match: str | None = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])
      if best_match:
        answer: str | None = get_answer_for_question(best_match, knowledge_base)
        if answer:
          print(f'Bot: {answer}')
        else:
          print("Bot: I found a close match but no corresponding answer. This shouldn't happen, please check the knowledge base.")
      else:
        print("Bot: I don't know the answer. Can you teach me?")
        new_answer: str = input("Type the answer or 'skip' to skip: ")
        if new_answer.lower() != 'skip':
          knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
          save_knowledge_base('knowledgebase.json', knowledge_base)
          print('Bot: Thank you! I learned a new response!')

if __name__ == '__main__':
    chat_bot()
