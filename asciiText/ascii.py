from PIL import Image
import os

# Luminance ramp: lightest (space) to darkest (full block █)
ASCII_CHARS = " .:-=+*#%@\u2591\u2592\u2593\u2588"  # + ░▒▓█
CHAR_LEN = len(ASCII_CHARS)
BLOCK_CHAR = "\u2588"  # full block █ for pixel mode


def _char_for_luminance(lum):
    # dark pixels -> dense chars (█), bright pixels -> space
    return ASCII_CHARS[(255 - lum) * CHAR_LEN // 256]


def _rgb_to_ansi_truecolor(r, g, b):
    # 24-bit truecolor foreground escape code
    return f"\x1b[38;2;{r};{g};{b}m"


def convert_and_save_ascii(image_path, output_folder='asciiFrames', width=80, height=40, pixel_mode=False):
    try:
        img = Image.open(image_path).resize((width, height)).convert("RGB")
        pixels = list(img.getdata())

        lines = []
        for y in range(height):
            line_parts = []
            last_color = None
            for x in range(width):
                r, g, b = pixels[y * width + x]
                lum = (r * 299 + g * 587 + b * 114) // 1000

                if pixel_mode:
                    ch = BLOCK_CHAR
                else:
                    ch = _char_for_luminance(lum)

                # Only emit the escape code when the color changes (run-length compression)
                color = (r, g, b)
                if color != last_color:
                    line_parts.append(_rgb_to_ansi_truecolor(r, g, b))
                    last_color = color
                line_parts.append(ch)

            # Reset colors at the end of each line
            line_parts.append("\x1b[0m")
            lines.append("".join(line_parts))

        ascii_art = "\n".join(lines)

        base_name = os.path.basename(image_path).replace(".png", ".txt")
        ascii_path = os.path.join(output_folder, base_name)
        os.makedirs(output_folder, exist_ok=True)

        # Write to a temp file first, then rename: prevents the player from
        # reading a partially-written (empty) frame
        tmp_path = ascii_path + ".tmp"
        with open(tmp_path, "w", encoding="utf-8") as f:
            f.write(ascii_art)
        os.replace(tmp_path, ascii_path)

    except Exception as e:
        print(f"[ERROR] Failed to convert {image_path}: {e}")