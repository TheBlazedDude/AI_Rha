
from transformers import GPT2LMHeadModel, GPT2Tokenizer, Trainer, TrainingArguments, TextDataset, DataCollatorForLanguageModeling
import os

def fine_tune_model(data_path="data/training_dataset.json", output_dir="models/chat-model"):
    if not os.path.exists(data_path):
        print("No training data found.")
        return

    import json
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    formatted_data = ["<|startoftext|>" + s["prompt"] + "\n" + s["response"] + "<|endoftext|>" for s in data]
    with open("data/dialogue.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(formatted_data))

    tokenizer = GPT2Tokenizer.from_pretrained("distilgpt2")
    model = GPT2LMHeadModel.from_pretrained("distilgpt2")

    dataset = TextDataset(
        tokenizer=tokenizer,
        file_path="data/dialogue.txt",
        block_size=64,
    )

    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer, mlm=False,
    )

    training_args = TrainingArguments(
        output_dir=output_dir,
        overwrite_output_dir=True,
        num_train_epochs=3,
        per_device_train_batch_size=2,
        save_steps=10_000,
        save_total_limit=2,
        logging_steps=100
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=dataset,
    )

    trainer.train()
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)
    print("Training complete.")

if __name__ == "__main__":
    fine_tune_model()
