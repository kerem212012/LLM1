import anthropic
from rich.console import Console
from rich.panel import Panel

import config


total = {'input': 0, 'output': 0}
client = anthropic.Anthropic(api_key=config.API_KEY)
max_tokens = 200
console = Console()
all_messages = []
while True:
    def chat(user_input, messages):
        messages.append({
            "role":"user",
            "content": user_input,
        })
        assistant_text = ""
        with client.messages.stream(
            model="claude-sonnet-4-6",   # обязательно
            max_tokens=max_tokens,
            messages=messages
        ) as stream:
            for text in stream.text_stream:
                console.print(text, end='', highlight=False)
                assistant_text += text
            console.print()
            final_message= stream.get_final_message()
        messages.append({
            "role": "assistant",
            "content": assistant_text,
        })
        total['input'] += final_message.usage.input_tokens
        total['output'] += final_message.usage.output_tokens
        console.print(final_message.usage)
        console.print(final_message.content[0].text)
        return assistant_text,final_message.usage

    def calc_cost(input_tokens, output_tokens):
        input_price = 3/1000000
        output_price = 15/1000000
        return (input_tokens*input_price+output_tokens*output_price)

    q= console.input("[bold blue]Ты:[/] ")

    console.print(Panel(
        f"Ты:{q}",
        title="Заголовок",
        border_style="blue"
    ))

    chat(q,all_messages)
    console.print(f"Input: [bold cyan]{total["input"]}[/] ",f"Output: [bold yellow]{total["output"]}[/] ")
    cost=calc_cost(total["input"],total["output"])
    console.print(f"[bold blue]{cost}[/] ")