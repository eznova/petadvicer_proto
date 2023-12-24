# Установка библиотеки transformers, если она еще не установлена
# !pip install transformers

# Загрузка предварительно обученной модели GPT-2
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Используем GPT-2, так как transformers предоставляет бесплатный API к этой модели
model_name = "gpt2"
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Функция для генерации совета
def generate_advice():
    prompt = "How to calm down angry pet? Get random advice"
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    output = model.generate(input_ids, max_length=200,  no_repeat_ngram_size=2, top_p=0.95, temperature=0.7)
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    return generated_text