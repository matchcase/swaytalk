# SwayTalk - © Sarthak Shah (matchcase), 2025
# Licensed under GPLv3 or Later.
from langchain_ollama.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import ConfigurableField
from langchain_core.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor

from i3ipc import Connection

import subprocess

sway = Connection()

@tool
def get_focused_window() -> str:
    "Get the name and workspace of the focused window."
    focused = sway.get_tree().find_focused()
    return f"{focused.name} on workspace {focused.workspace().name}"

@tool
def focus(focus_cmd: str):
    """
    The argument to this function should be a string of the form 'focus <arguments>'. Here is a description of the possible arguments:
           focus up|right|down|left
	  Moves focus to the next container in the specified direction.

       focus prev|next [sibling]
	  Moves focus to the previous or next container in the current layout. By default, the last active  child  of	the
	  newly  focused  container  will be focused. The sibling option indicates not to immediately focus a child of the
	  container.

       focus child
	  Moves focus to the last-focused child of the focused container.

       focus parent
	  Moves focus to the parent of the focused container.

       focus output up|right|down|left
	  Moves focus to the next output in the specified direction.

       focus output <name>
	  Moves focus to the named output.

       focus tiling
	  Sets focus to the last focused tiling container.

       focus floating
	  Sets focus to the last focused floating container.

       focus mode_toggle
	  Moves focus between the floating and tiled layers.
    """
    if "focus" not in focus_cmd:
        focus_cmd = "focus " + focus_cmd
    sway.command(focus_cmd)

@tool
def move(move_cmd: str):
    """
    The argument to this function should be a string of the form 'move <arguments>'. Here is a description of the possible arguments:
       move left|right|up|down [<px> px]
	  Moves  the  focused	container in the direction specified. The optional px argument specifies how many pixels to
	  move the container. If unspecified, the default is 10 pixels. Pixels are ignored when moving tiled containers.

       move [absolute] position <pos_x> [px|ppt] <pos_y> [px|ppt]
	  Moves the focused container to the specified position in the workspace. The position can be specified in  pixels
	  or percentage points, omitting the unit defaults to pixels. If absolute is used, the position is relative to all
	  outputs. absolute can not be used with percentage points.

       move [absolute] position center
	  Moves  the  focused container to be centered on the workspace. If absolute is used, it is moved to the center of
	  all outputs.

       move position cursor|mouse|pointer
	  Moves the focused container to be centered on the cursor.

       move [container|window] [to] mark <mark>
	  Moves the focused container to the specified mark.

       move [--no-auto-back-and-forth] [container|window] [to] workspace [number] <name>
	  Moves the focused container to the specified workspace. The string number is optional and is	used  to  match  a
	  workspace with the same number, even if it has a different name.

       move [container|window] [to] workspace prev|next|current
	  Moves  the  focused container to the previous, next or current workspace on this output, or if no workspaces re‐
	  main, the previous or next output.

       move [container|window] [to] workspace prev_on_output|next_on_output
	  Moves the focused container to the previous or next workspace on this output, wrapping around if already at	the
	  first or last workspace.

       move [container|window] [to] workspace back_and_forth
	  Moves the focused container to previously focused workspace.

       move [container|window] [to] output <name-or-id>|current
	  Moves the focused container to the specified output.

       move [container|window] [to] output up|right|down|left
	  Moves the focused container to next output in the specified direction.

       move [container|window] [to] scratchpad
	  Moves the focused container to the scratchpad.

       move workspace [to] output <name-or-id>|current
	  Moves the focused workspace to the specified output.

       move workspace to [output] <name-or-id>|current
	  Moves the focused workspace to the specified output.

       move workspace [to] output up|right|down|left
	  Moves the focused workspace to next output in the specified direction.

       move workspace to [output] up|right|down|left
	  Moves the focused workspace to next output in the specified direction.
    """
    if "move" not in move_cmd:
        move_cmd = "move " + move_cmd
    sway.command(move_cmd)
    
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an LLM agent that runs commands to manage the Sway window manager."), 
    ("human", "{input}"), 
    ("placeholder", "{agent_scratchpad}"),
])

tools = [get_focused_window, focus, move]

llm = ChatOllama(model="mistral-nemo", temperature=0)


agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

result = subprocess.run(["fuzzel", "-d", "-p", "> "], capture_output=True, text=True)
if result.returncode == 0:
    agent_executor.invoke({"input": f"{result.stdout.strip()}", })
else:
    print("No input provided.")

