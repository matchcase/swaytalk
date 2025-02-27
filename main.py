# SwayTalk - © Sarthak Shah (matchcase), 2025
# Licensed under GPLv3 or Later.
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import ConfigurableField
from langchain_core.tools import tool, BaseTool
from langchain.agents import AgentExecutor, create_tool_calling_agent
from typing import List, Dict, Any, Optional, Callable, Type
from langchain.callbacks.manager import CallbackManagerForToolRun
from PyQt6.QtWidgets import QApplication, QInputDialog

from i3ipc import Connection

import subprocess

sway = Connection()


def border(criteria: str):
    """
    The argument to this function should be a string of the form 'border <arguments>'. Here is a description of the possible arguments:
       border none|normal|csd|pixel [<n>]
           Set  border style for focused window. normal includes a border of thickness n and a title bar. pixel is a border
           without title bar n pixels thick. The title bar always shows in stacking or tabbed layouts.  csd  is  short  for
           client-side-decorations,  which  allows  the  client  to draw its own decorations. Default is normal with border
           thickness 2.

       border toggle
           Cycles through the available border styles.
    """
    if "border" not in criteria:
        criteria = "border " + criteria
    sway.command(criteria)


def exit():
    """
    This function exits the window manager.
    """
    sway.command("exit")


def floating(criteria: str):
    """
    The argument to this function should be a string of the form 'floating <arguments>'. Here is a description of the possible arguments:
       floating enable|disable|toggle
           Make focused view floating, non-floating, or the opposite of what it is now.
    """
    if "floating" not in criteria:
        criteria = "floating " + criteria
    sway.command(criteria)
    

def focus(criteria: str):
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
    if "focus" not in criteria:
        criteria = "focus " + criteria
    sway.command(criteria)


def fullscreen(criteria: str):
    """
    The argument to this function should be a string of the form 'fullscreen <arguments>'. Here is a description of the possible arguments:
       fullscreen [enable|disable|toggle] [global]
           Makes focused view fullscreen, non-fullscreen, or the opposite of what it is now. If no argument  is  given,  it
           does the same as toggle. If global is specified, the view will be fullscreen across all outputs.
    """
    if "fullscreen" not in criteria:
        criteria = "fullscreen " + criteria
    sway.command(criteria)


def gaps(criteria: str):
    """
    The argument to this function should be a string of the form 'gaps <arguments>'. Here is a description of the possible arguments:
       gaps inner|outer|horizontal|vertical|top|right|bottom|left all|current set|plus|minus|toggle <amount>
           Changes  the  inner  or outer gaps for either all workspaces or the current workspace. outer gaps can be altered
           per side with top, right, bottom, and left or per direction with horizontal and vertical.
    """
    if "gaps" not in criteria:
        criteria = "gaps" + criteria
    sway.command(criteria)


def inhibit_idle(criteria: str):
    """
    The argument to this function should be a string of the form 'inhibit_idle <arguments>'. Here is a description of the possible arguments:
       inhibit_idle focus|fullscreen|open|none|visible
           Set/unset an idle inhibitor for the view. focus will inhibit  idle  when  the  view  is  focused  by  any  seat.
           fullscreen will inhibit idle when the view is fullscreen (or a descendant of a fullscreen container) and is vis‐
           ible.  open will inhibit idle until the view is closed (or the inhibitor is unset/changed). visible will inhibit
           idle when the view is visible on any output. none will remove any existing idle inhibitor for the view.

           This can also be used with criteria to set an idle inhibitor for any existing view or  with  for_window  to  set
           idle inhibitors for future views.
    """
    if "inhibit_idle" not in criteria:
        criteria = "inhibit_idle" + criteria
    sway.command(criteria)


def layout(criteria: str):
    """
    The argument to this function should be a string of the form 'layout <arguments>'. Here is a description of the possible arguments:
       layout default|splith|splitv|stacking|tabbed
           Sets the layout mode of the focused container.

           When  using the stacking layout, only the focused window in the container is displayed, with the opened windows'
           list on the top of the container.

           The tabbed layout is similar to stacking, but the windows’ list is vertically split.

       layout toggle [split|all]
           Cycles the layout mode of the focused container though a preset list of layouts. If no argument is  given,  then
           it  cycles  through stacking, tabbed and the last split layout. If split is given, then it cycles through splith
           and splitv. If all is given, then it cycles through every layout.

       layout toggle [split|tabbed|stacking|splitv|splith] [split|tabbed|stacking|splitv|splith]...
           Cycles the layout mode of the focused container through a list of layouts.
    """
    if "layout" not in criteria:
        criteria = "layout" + criteria
    sway.command(criteria)


def max_render_time(max_criteria: str):
    """
    The argument to this function should be a string of the form 'max_render_time <arguments>'. Here is a description of the possible arguments:
       max_render_time off|<msec>
           Controls when the relevant application is told to render this window, as a positive number of  milliseconds  be‐
           fore  the  next time sway composites the output. A smaller number leads to fresher rendered frames being compos‐
           ited by sway and lower perceived input latency, but if set too low, the application may not finish rendering be‐
           fore sway composites the output, leading to delayed frames.

           When set to off, the relevant application is told to render this window immediately after display  refresh.  How
           much  time  is left for rendering before sway composites the output at that point depends on the output max_ren‐
           der_time setting.

           To set this up for optimal latency:
           1.  Set up output max_render_time.
           2.  Put the target application in full-screen and have it continuously render something.
           3.  Start by setting max_render_time 1. If the application drops frames, increment by 1.
    """
    if "max_render_time" not in max_criteria:
        max_criteria = "max_render_time" + max_criteria
    sway.command(max_criteria)


def allow_tearing(criteria: str):
    """
    The argument to this function should be a string of the form 'allow_tearing <arguments>'. Here is a description of the possible arguments:
       allow_tearing yes|no
           Allows or disallows screen tearing as a result of immediate page flips for a fullscreen application.

           When this option is not set, the tearing hints provided by the application determine whether tearing is allowed.
           When  yes  is  specified,  the application allows tearing regardless of the tearing hints. When no is specified,
           tearing will never be allowed on the application, regardless of the tearing hints.
    """
    if "allow_tearing" not in criteria:
        criteria = "allow_tearing" + criteria
    sway.command(criteria)
    

def move(criteria: str):
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
    if "move" not in criteria:
        criteria = "move " + criteria
    sway.command(criteria)


def reload():
    """
    This function reloads the sway config file and applies any changes.
    """
    sway.command("reload")


def rename(criteria: str):
    """
    The argument to this function should be a string of the form 'rename <arguments>'. Here is a description of the possible arguments:
       rename workspace [<old_name>] to <new_name>
           Rename either <old_name> or the focused workspace to the <new_name>
    """
    if "rename" not in criteria:
        criteria = "rename" + criteria
    sway.command(criteria)


def resize(criteria: str):
    """
    The argument to this function should be a string of the form 'resize <arguments>'. Here is a description of the possible arguments:
       resize shrink|grow width|height [<amount> [px|ppt]]
           Resizes the currently focused container by amount, specified in pixels or percentage points. If  the  units  are
           omitted,  floating  containers are resized in px and tiled containers by ppt. amount will default to 10 if omit‐
           ted.

       resize set height <height> [px|ppt]
           Sets the height of the container to height, specified in pixels or percentage points. If the units are  omitted,
           floating containers are resized in px and tiled containers by ppt. If height is 0, the container will not be re‐
           sized.

       resize set [width] <width> [px|ppt]
           Sets  the  width  of the container to width, specified in pixels or percentage points. If the units are omitted,
           floating containers are resized in px and tiled containers by ppt. If width is 0, the container will not be  re‐
           sized.

       resize set [width] <width> [px|ppt] [height] <height> [px|ppt]
           Sets the width and height of the container to width and height, specified in pixels or percentage points. If the
           units  are  omitted, floating containers are resized in px and tiled containers by ppt. If width or height is 0,
           the container will not be resized on that axis.
    """
    if "resize" not in criteria:
        criteria = "resize" + criteria
    sway.command(criteria)


def scratchpad():
    """
    This commands shows the scratchpad.
    """
    sway.command("scratchpad show")


def shortcuts_inhibitor(criteria: str):
    """
    The argument to this function should be a string of the form 'shortcuts_inhibitor <arguments>'. Here is a description of the possible arguments:
       shortcuts_inhibitor enable|disable
           Enables or disables the ability of clients to inhibit keyboard shortcuts for a view. This  is  primarily  useful
           for  virtualization  and remote desktop software. It affects either the currently focused view or a set of views
           selected by criteria. Subcommand disable additionally deactivates any active inhibitors for the  given  view(s).
           Criteria  are particularly useful with the for_window command to configure a class of views differently from the
           per-seat defaults established by the seat subcommand of the same name. See sway-input(5) for more ways to affect
           inhibitors.
    """
    if "shortcuts_inhibitor" not in criteria:
        criteria = "shortcuts_inhibitor" + criteria
    sway.command(criteria)


def split(criteria: str):
    """
    The argument to this function should be a string of the form 'split <arguments>'. Here is a description of the possible arguments:
       split vertical|v|horizontal|h|none|n|toggle|t
           Splits the current container, vertically or horizontally. When none is specified, the effect of a previous split
           is undone if the current container is the only child of a split parent. When toggle is  specified,  the  current
           container is split opposite to the parent container's layout.
    """
    if "split" not in criteria:
        criteria = "split" + criteria
    sway.command(criteria)


def sticky(criteria: str):
    """
    The argument to this function should be a string of the form 'sticky <arguments>'. Here is a description of the possible arguments:
       sticky enable|disable|toggle
           "Sticks" a floating window to the current output so that it shows up on all workspaces.
    """
    if "sticky" not in criteria:
        criteria = "sticky" + criteria
    sway.command(criteria)


def swap(criteria: str):
    """
    The argument to this function should be a string of the form 'swap <arguments>'. Here is a description of the possible arguments:
       swap container with id|con_id|mark <arg>
           Swaps  the  position, geometry, and fullscreen status of two containers. The first container can be selected ei‐
           ther by criteria or focus. The second container can be selected by id, con_id, or mark. id can only be used with
           xwayland views. If the first container has focus, it will retain focus unless it is moved to a  different  work‐
           space  or  the  second  container  becomes fullscreen on the same workspace as the first container. In either of
           those cases, the second container will gain focus.
    """
    if "swap" not in criteria:
        criteria = "swap" + criteria
    sway.command(criteria)


def title_format(criteria: str):
    """
    The argument to this function should be a string of the form 'title_format <arguments>'. Here is a description of the possible arguments:
       title_format <format>
           Sets the format of window titles. The following placeholders may be used:

               %title - The title supplied by the window
                         %app_id - The wayland app ID (applicable to wayland windows only)
                         %class - The X11 classname (applicable to xwayland windows only)
                         %instance - The X11 instance (applicable to xwayland windows only)
                         %shell - The protocol the window is using (typically xwayland or
                   xdg_shell)

           This command is typically used with for_window criteria. For example:

               for_window [title="."] title_format "<b>%title</b> (%app_id)"

           Note that markup requires pango to be enabled via the font command.

           The default format is "%title".
    """
    if "title_format" not in criteria:
        criteria = "title_format" + criteria
    sway.command(criteria)
   
# Create a dictionary to store full function objects with their docstrings
full_tools = {
    "focus": focus,
    "move": move,
    "fullscreen": fullscreen,
    "exit": exit,
    "reload": reload,
    "split": split,
    "floating": floating,
    "layout": layout,
    "border": border,
    "gaps": gaps,
    "inhibit_idle": inhibit_idle,
    "max_render_time": max_render_time,
    "allow_tearing": allow_tearing,
    "rename": rename,
    "resize": resize,
    "scratchpad": scratchpad,
    "shortcuts_inhibitor": shortcuts_inhibitor,
    "sticky": sticky,
    "swap": swap,
    "title_format": title_format,
}

# Create simplified versions of tools with minimal descriptions
def create_simplified_tool(tool_name: str, tool_description: str) -> BaseTool:
    """Create a simplified version of a tool with just its name and a brief description."""
    class SimplifiedTool(BaseTool):
        name: str = tool_name
        description: str = tool_description
        
        def _run(self, *args: Any, **kwargs: Any) -> str:
            return f"Please use get_docstring(tool_name=\"{name}\") first to see documentation, then call execute_code(tool_name=\"{name}\", arguments=\"your_args\")"
            
    return SimplifiedTool()

# Simple descriptions for each tool
tool_descriptions = {
    "focus": "Focus a window or workspace",
    "move": "Move a window",
    "fullscreen": "Toggle fullscreen mode for a window",
    "exit": "Exit Sway",
    "reload": "Reload Sway configuration",
    "split": "Change split direction",
    "floating": "Toggle floating mode for a window",
    "layout": "Change the layout of the current workspace",
    "border": "Set border style",
    "gaps": "Change inner or outer gaps",
    "inhibit_idle": "Set or unset idle inhibitor",
    "max_render_time": "Controls when a window is rendered",
    "allow_tearing": "Allow or disallow tearing",
    "rename": "Rename a workspace",
    "resize": "Resize a window",
    "scratchpad": "Show the scratchpad",
    "shortcuts_inhibitor": "Toggle ability to inhibit shortcuts",
    "sticky": "Sticky a window",
    "swap": "Swap containers",
    "title_format": "Set format for window titles",
}

simplified_tools = [
    create_simplified_tool(name, desc) 
    for name, desc in tool_descriptions.items()
]

class GetDocstringTool(BaseTool):
    name: str = "get_docstring"
    description: str = "Get the full documentation for a specific tool"
    
    def _run(
        self, 
        tool_name: str, 
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Get the full docstring for a tool.
        
        Args:
            tool_name: The name of the tool to get documentation for
            
        Returns:
            The full docstring of the requested tool
        """
        if tool_name not in full_tools:
            return f"Tool '{tool_name}' not found. Available tools: {', '.join(full_tools.keys())}"
        
        tool_doc = full_tools[tool_name].__doc__
        return f"Documentation for {tool_name}:\n{tool_doc}\n\nNow you can execute this tool with: execute_code(tool_name=\"{tool_name}\", arguments=\"your_args\")"

class ExecuteToolTool(BaseTool):
    name: str = "execute_code"
    description: str = "Execute a tool after reviewing its documentation"
    
    def _run(
        self, 
        tool_name: str,
        arguments: str = "",
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Execute a tool with the provided arguments.
        
        Args:
            tool_name: The name of the tool to execute
            arguments: The arguments to pass to the tool
            
        Returns:
            The result of executing the tool
        """
        if tool_name not in full_tools:
            return f"Tool '{tool_name}' not found. Available tools: {', '.join(full_tools.keys())}"
        
        try:
            if arguments:
                return full_tools[tool_name](arguments)
            else:
                return full_tools[tool_name]()
        except Exception as e:
            return f"Error executing {tool_name}: {str(e)}"

all_tools = simplified_tools + [GetDocstringTool(), ExecuteToolTool()]

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an LLM agent that runs commands to manage the Sway window manager.
This is VERY IMPORTANT: your response should be brief, and only contain tool calls.

IMPORTANT: You must follow this exact TWO-STEP PROCESS for every tool you use:

STEP 1: First get the tool's documentation by calling get_docstring
    Example: get_docstring(tool_name="focus")

STEP 2: After reviewing the documentation, execute the tool with proper arguments
    Example: execute_code(tool_name="focus", arguments="next")

DO NOT try to call any tool directly without first getting its documentation.
If a user asks you to perform an action like "focus on the next window", you MUST:
1. First call get_docstring for the relevant tool (get_docstring(tool_name="focus"))
2. Then call execute_code with the proper arguments (execute_code(tool_name="focus", arguments="next"))

Remember: All outputs are strings. Only use the tools provided.
**VERY IMPORTANT**:
THE OUTPUTS SHOULD ONLY BE TOOL CALLS.
DO NOT OUTPUT ANYTHING OTHER THAN CALL TOOLS.
DO NOT PROVIDE MULTIPLE EXAMPLES, FOCUS ON ONLY EXECUTING THE BEST ACTION.

When what the user requested is ambiguous, assume that they are talking about the focused window and execute the most likely desired action.
"""), 
    ("human", "{input}"), 
    ("placeholder", "{agent_scratchpad}"),
])

llm = ChatOllama(model="mistral-nemo", temperature=0)

agent = create_tool_calling_agent(llm, all_tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=all_tools, verbose=True)

# result = subprocess.run(["fuzzel", "-d", "-p", "> "], capture_output=True, text=True)
# if result.returncode == 0:
#     agent_executor.invoke({"input": f"{result.stdout.strip()}"})
app = QApplication([])
text, ok = QInputDialog.getText(None, "Input Dialog", "Enter your text:")
if ok:
    agent_executor.invoke({"input": text})
else:
    print("No input provided.")
