def hex_to_RGB(hex_color):
    """Converts hexadecimal color to RGB."""
    if hex_color.startswith('#'):
        hex_color = hex_color[1:]
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def RGB_to_hex(RGB):
    """Converts RGB to hexadecimal color."""
    return '#{:02x}{:02x}{:02x}'.format(*RGB)

def linear_gradient(start_hex, finish_hex, n=10):
    """
    Returns a list of RGB colors representing a gradient between two colors.
    
    Parameters:
    - start_hex: Starting color in hexadecimal format.
    - finish_hex: Ending color in hexadecimal format.
    - n: Number of colors in the gradient.
    """
    start_RGB = hex_to_RGB(start_hex)
    finish_RGB = hex_to_RGB(finish_hex)
    
    gradient = []
    for t in range(n):
        t_norm = t / (n - 1) if n > 1 else 0
        curr_RGB = tuple(int(start_RGB[j] + t_norm * (finish_RGB[j] - start_RGB[j])) for j in range(3))
        gradient.append(curr_RGB)
    
    return gradient


if __name__ == "__main__":
    # Example usage
    start_color = "#FFFBC4FF"
    end_color = "#3A78FFFF"
    gradient = linear_gradient(start_color, end_color, n=20)

    # Print the gradient in both RGB and hexadecimal formats
    for i, color in enumerate(gradient):
        print(f"Color {i+1}: RGB={color}, HEX={RGB_to_hex(color)}")