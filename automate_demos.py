import os
import sys
import time
import subprocess
import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Attempt importing imageio for MP4 video creation
try:
    import imageio.v3 as iio
    IMAGEIO_AVAILABLE = True
except ImportError:
    IMAGEIO_AVAILABLE = False

# Application Paths
BASE_DIR = Path(__file__).resolve().parent
DEMO_VIDEOS_DIR = BASE_DIR / "demo_videos"
DEMO_VIDEOS_DIR.mkdir(exist_ok=True)

# Font Setup (Consolas is built-in on Windows)
FONT_PATH = "C:\\Windows\\Fonts\\consola.ttf"
if not os.path.exists(FONT_PATH):
    FONT_PATH = "lucon.ttf"  # Fallback to Lucida Console

# ANSI escape sequence parser regex
ANSI_ESCAPE = re.compile(r'\x1b\[([0-9;]*)m')

# Terminal Theme Mappings
COLOR_MAP = {
    "0": (200, 200, 200),     # Reset / Light Gray
    "30": (12, 12, 12),       # Black
    "31": (247, 76, 76),      # Red
    "32": (76, 201, 240),     # Green (mapped to a premium cyan-blue in theme)
    "33": (255, 190, 11),     # Yellow
    "34": (67, 97, 238),      # Blue
    "35": (114, 9, 183),      # Magenta
    "36": (72, 202, 228),     # Cyan
    "37": (248, 249, 250),    # White
    "90": (108, 117, 125),    # Dark Gray / Muted
    "91": (247, 76, 76),
    "92": (76, 201, 240),
    "93": (255, 190, 11),
    "94": (67, 97, 238),
    "95": (114, 9, 183),
    "96": (72, 202, 228),
    "97": (248, 249, 250),
}

class TerminalSimulator:
    """Simulates a terminal window and renders text onto a PIL Image."""

    def __init__(self, width: int = 700, height: int = 580, font_size: int = 14):
        self.width = width
        self.height = height
        self.font_size = font_size
        self.bg_color = (18, 18, 18)  # Deep Charcoal Dark Mode
        self.font = ImageFont.truetype(FONT_PATH, self.font_size)
        self.line_height = self.font_size + 4
        self.padding_x = 20
        self.padding_y = 20

    def render_output(self, text: str) -> Image.Image:
        """Parses ANSI escape codes and renders the output onto an image."""
        img = Image.new("RGB", (self.width, self.height), self.bg_color)
        draw = ImageDraw.Draw(img)

        # Draw a simulated terminal top bar
        draw.rectangle([0, 0, self.width, 30], fill=(30, 30, 30))
        # Draw window control buttons
        draw.ellipse([15, 10, 23, 18], fill=(255, 95, 87))  # Close
        draw.ellipse([30, 10, 38, 18], fill=(255, 189, 46)) # Minimize
        draw.ellipse([45, 10, 53, 18], fill=(40, 200, 64))   # Maximize

        # Render console text lines
        lines = text.split("\n")
        # Keep only the last lines that fit in the terminal viewport
        max_lines = (self.height - self.padding_y - 40) // self.line_height
        visible_lines = lines[-max_lines:]

        y = self.padding_y + 20
        for line in visible_lines:
            x = self.padding_x
            # Parse ANSI sequences on the line
            parts = ANSI_ESCAPE.split(line)
            current_color = (200, 200, 200) # Reset color

            for i in range(len(parts)):
                part = parts[i]
                if i % 2 == 1:
                    # ANSI code segment
                    code = part.split(";")[-1]
                    current_color = COLOR_MAP.get(code, current_color)
                else:
                    # Actual text segment
                    if not part:
                        continue
                    # Draw text segment
                    draw.text((x, y), part, font=self.font, fill=current_color)
                    # Advance x position
                    # In a monospaced font, length is char_count * char_width
                    # Fetch width using text length
                    bbox = draw.textbbox((0, 0), part, font=self.font)
                    text_w = bbox[2] - bbox[0]
                    x += text_w
            y += self.line_height

        return img


def run_interactive_app(main_script: str, inputs: list[str]) -> list[str]:
    """Runs a Python script and feeds inputs one by one, capturing output states."""
    # Launch subprocess in a clean environment
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    process = subprocess.Popen(
        [sys.executable, main_script],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        bufsize=0,
        env=env
    )

    outputs = []
    accumulated_output = ""

    # Helper to read stdout until a prompt appears
    def read_until_prompt(proc):
        nonlocal accumulated_output
        buffer = []
        while True:
            char = proc.stdout.read(1)
            if not char:
                break
            buffer.append(char)
            # Standard CLI prompts usually end with ":" or "?" or "]"
            text = "".join(buffer)
            if text.endswith("]: ") or text.endswith(": ") or text.endswith("): ") or text.endswith("Your choice: ") or text.endswith("menu option [1-9, A, H, V, Q]: "):
                break
            # Guard against infinite loop if process finishes
            if proc.poll() is not None:
                break
        out_str = "".join(buffer)
        accumulated_output += out_str
        return out_str

    # Read initial startup banner
    read_until_prompt(process)
    outputs.append(accumulated_output)

    for user_input in inputs:
        if process.poll() is not None:
            break
        # Simulate typing: append input to accumulated log
        accumulated_output += f"{user_input}\n"
        outputs.append(accumulated_output)

        # Write to stdin
        process.stdin.write(f"{user_input}\n")
        process.stdin.flush()
        
        # Give small time to process and read response
        time.sleep(0.1)
        read_until_prompt(process)
        outputs.append(accumulated_output)

    # Make sure process exits cleanly
    try:
        process.stdin.write("Q\n")
        process.stdin.flush()
    except Exception:
        pass
    
    process.wait()
    return outputs


def create_demo_assets(task_name: str, script_path: str, inputs: list[str], screenshot_indices: list[int]):
    """Generates screenshots and MP4 videos for a task."""
    print(f"\nDemonstrating {task_name}...")
    outputs = run_interactive_app(script_path, inputs)
    
    sim = TerminalSimulator()
    frames = []

    # Compile frames for video
    for idx, out in enumerate(outputs):
        img = sim.render_output(out)
        frames.append(img)
        # Duplicate frames to slow down transitions and simulate typing delays
        if idx % 2 == 1:
            for _ in range(8):  # Pause on user actions
                frames.append(img)
        else:
            for _ in range(12): # Pause on application replies
                frames.append(img)

    # Save screenshots to task's screenshots directory
    task_dir = Path(script_path).parent
    screenshots_dir = task_dir / "screenshots"
    screenshots_dir.mkdir(exist_ok=True)
    
    print(f"Saving screenshots for {task_name}...")
    screenshot_count = 1
    for index in screenshot_indices:
        if index < len(outputs):
            img = sim.render_output(outputs[index])
            img.save(screenshots_dir / f"Screenshot_{screenshot_count}.png")
            screenshot_count += 1

    # Save video if imageio is available
    if IMAGEIO_AVAILABLE:
        video_path = DEMO_VIDEOS_DIR / f"{task_name}_Demo.mp4"
        print(f"Compiling demo video to {video_path}...")
        # Convert PIL images to numpy arrays for imageio
        import numpy as np
        np_frames = [np.array(f) for f in frames]
        # Write to MP4 at 10 fps
        iio.imwrite(video_path, np_frames, fps=10, codec="libx264")
        print(f"Demo video saved successfully at {video_path}")
    else:
        print("imageio is not installed; skipped generating video files.")


if __name__ == "__main__":
    if not IMAGEIO_AVAILABLE:
        print("Warning: 'imageio[ffmpeg]' is not installed. Video recording will be skipped.")
        print("Run: pip install imageio[ffmpeg] pillow to enable full automated video capture.")

    # 1. Run Task 1 (Todo Manager)
    # Inputs:
    # 1: Add task
    # "Finalise report", "Report description", "HIGH", "2026-06-12"
    # 2: View tasks
    # 5: Complete task
    # "1" (ID)
    # 9: Stats
    # Q: Quit
    todo_inputs = [
        "1", "Finalise internship report", "Compile documentation and video", "HIGH", "2026-06-12",
        "2",
        "5", "1",
        "9",
        "Q"
    ]
    # Highlight final view indices for screenshots
    create_demo_assets(
        task_name="Task_1",
        script_path=str(BASE_DIR / "Task_1_Todo_Manager" / "main.py"),
        inputs=todo_inputs,
        screenshot_indices=[3, 5, 9, 13]
    )

    # 2. Run Task 2 (Scientific Calculator)
    # Inputs:
    # 1: Basic -> "+" -> 15 -> 30
    # 3: Advanced -> 2: Factorial -> 5
    # 5: Trig -> 1: sin -> 90
    # 8: History -> 1: Export
    # Q: Quit
    calc_inputs = [
        "1", "+", "15", "30",
        "3", "2", "5",
        "5", "1", "90",
        "8", "1", "",
        "Q", "n" # n for no history export during quit
    ]
    create_demo_assets(
        task_name="Task_2",
        script_path=str(BASE_DIR / "Task_2_Scientific_Calculator" / "main.py"),
        inputs=calc_inputs,
        screenshot_indices=[3, 7, 10, 14]
    )

    # 3. Run Task 3 (Secure Password Generator)
    # Inputs:
    # 1: Single -> length 16 -> yes -> yes -> yes -> yes -> copy: yes
    # 2: Batch -> count 3 -> length 12 -> yes -> yes -> yes -> yes -> copy: skip
    # Q: Quit
    gen_inputs = [
        "1", "16", "y", "y", "y", "y", "y",
        "2", "3", "12", "y", "y", "y", "y", "",
        "Q"
    ]
    create_demo_assets(
        task_name="Task_3",
        script_path=str(BASE_DIR / "Task_3_Secure_Password_Generator" / "main.py"),
        inputs=gen_inputs,
        screenshot_indices=[3, 7, 12, 14]
    )

    print("\nAll automated demonstrations completed successfully!")
