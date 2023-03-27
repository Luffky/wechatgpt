from bridge.context import *
from channel.channel import Channel
import sys

terminal_role_map = {
    "fitting-translator": "在运动医学背景下，用通俗易懂地语言将下面的话转译成中文，只输出翻译后的内容给我：\n"
}

class TerminalChannel(Channel):
    current_role = ""

    def startup(self):
        context = Context()
        print("\nPlease input your question")
        while True:
            try:
                prompt = self.get_input("User:\n")
            except KeyboardInterrupt:
                print("\nExiting...")
                sys.exit()
            if self.current_role is "":
                if prompt in terminal_role_map:
                    self.current_role = prompt
                    print("Bot: 角色扮演开始，从现在开始我将: " + terminal_role_map[self.current_role])
                    continue

            if self.current_role is not "":
                if prompt == "stop":
                    self.current_role = ""
                    print("Bot: 从现在开始我将停止角色扮演: ")
                    continue
                else:
                    prompt = terminal_role_map[self.current_role] + prompt
            context.type = ContextType.TEXT
            context['session_id'] = "User"
            context.content = prompt
            print("Bot:")
            sys.stdout.flush()
            res = super().build_reply_content(prompt, context).content
            print(res)


    def get_input(self, prompt):
        """
        Multi-line input function
        """
        print(prompt, end="")
        line = input()
        return line
