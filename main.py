import anthropic
from rich.console import Console
from rich.panel import Panel

import config

total = {'input': 0, 'output': 0}
client = anthropic.Anthropic(api_key=config.API_KEY)
max_tokens = 200
console = Console()
all_messages = []


def chat(user_input, messages):
    messages.append({
        "role": "user",
        "content": user_input,
    })
    assistant_text = ""
    with client.messages.stream(
            model="claude-sonnet-4-6",  # обязательно
            max_tokens=max_tokens,
            messages=messages
    ) as stream:
        for text in stream.text_stream:
            console.print(text, end='', highlight=False)
            assistant_text += text
        console.print()
        final_message = stream.get_final_message()
    messages.append({
        "role": "assistant",
        "content": assistant_text,
    })
    total['input'] += final_message.usage.input_tokens
    total['output'] += final_message.usage.output_tokens
    console.print(final_message.usage)
    console.print(final_message.content[0].text)
    return assistant_text, final_message.usage


def calc_cost(input_tokens, output_tokens):
    input_price = 3 / 1000000
    output_price = 15 / 1000000
    return (input_tokens * input_price + output_tokens * output_price)


def show_stats():

    console.print(f"Input: [bold cyan]{total["input"]}[/] ", f"Output: [bold yellow]{total["output"]}[/] ")
    cost = calc_cost(total["input"], total["output"])
    console.print(f"[bold blue]{cost}[/] ")


def main():
    global all_messages
    while True:
        try:
            q = console.input("[bold blue]Ты:[/] ")
        except KeyboardInterrupt:
            show_stats()
            console.print(f"[bold red]You exit a chat[/] ")
            break
        if q == "/clear":
            all_messages = []
            console.print(f"[bold red]You cleared all messages from your chat[/] ")
        elif q == "/exit":
            show_stats()
            console.print(f"[bold red]You exit a chat[/] ")
            break
        elif q == "/stats":
            show_stats()
        else:
            console.print(Panel(
                f"Ты:{q}",
                title="Заголовок",
                border_style="blue"
            ))
            try:
                chat(q, all_messages)
            except anthropic.APIConnectionError:
                console.print(Panel(
                    f"Error: Can't connect to API",
                    title="Заголовок",
                    border_style="red"
                ))
            except anthropic.AuthenticationError:
                console.print(Panel(
                    f"Error: Wrong API key",
                    title="Заголовок",
                    border_style="red"
                ))


if __name__ == '__main__':
    main()
