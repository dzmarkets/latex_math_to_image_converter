# Path: latex_math_to_image_converter/main.py
# Description: Main script to convert LaTeX mathematical equations to images (no surrounding text),
#              now with an option to process equations directly from a .tex file.
# Developed by: M. YOUCEF Yazid (yazid.youcef@gmail.com)
# File Version: 1.5.0
# CreateDate: 2025-06-27
# UpdateDate: 2025-06-27

import matplotlib.pyplot as plt
import os
import re # Import the regular expression module for parsing LaTeX files

def latex_to_image(latex_equation: str, output_filename: str = 'output_equation.png', dpi: int = 300) -> None:
    r"""
    Converts a LaTeX mathematical equation (without surrounding text) into a PNG image.
    The input LaTeX string MUST be enclosed in '$...$' for inline math or '$$...$$' for display math.

    Args:
        latex_equation (str): The LaTeX math equation string (e.g., r'$\sum_{i=0}^n i^2$').
                              Remember to use raw strings (r'...') and enclose in $ or $$.
        output_filename (str): The name of the output image file (e.g., 'my_equation.png').
        dpi (int): Dots per inch for the output image. Higher DPI means higher resolution.
    """
    try:
        # Create a figure and an axes object with a minimal initial size.
        # Matplotlib's tight bounding box will adjust this automatically.
        fig = plt.figure(figsize=(1, 0.5))

        # Reverted to default background color (no explicit setting for deep purple)
        # The background will be transparent when saved with transparent=True

        # Add an axes object that covers the entire figure.
        ax = fig.add_axes([0, 0, 1, 1])

        # Render the LaTeX equation. Matplotlib interprets strings enclosed in $ or $$ as math.
        # The text is centered horizontally and vertically on the axes.
        ax.text(0.5, 0.5, latex_equation,
                fontsize=20,          # Font size of the equation.
                color='black',        # Changed color to black for better visibility on a potentially white/transparent background.
                horizontalalignment='center',
                verticalalignment='center',
                transform=ax.transAxes) # Use axes coordinates (0 to 1) for positioning.

        # Hide the x and y axes ticks and labels for a clean math image.
        ax.set_xticks([])
        ax.set_yticks([])
        ax.axis('off') # Turn off the axis lines and labels completely.

        # Save the figure as a PNG image.
        # bbox_inches='tight': Automatically crops the image to the tightest bounding box around the content.
        # pad_inches=0.1: Adds a small padding around the cropped content.
        # transparent=True: Ensures the background is transparent.
        # dpi: Sets the resolution of the output image.
        plt.savefig(output_filename, bbox_inches='tight', pad_inches=0.1, transparent=True, dpi=dpi)

        # Close the figure to free up memory, especially important in loops.
        plt.close(fig)

        print(f"Successfully converted LaTeX equation to {output_filename}")

    except Exception as e:
        # Catch any exceptions that occur during the process and print an informative error message.
        print(f"An error occurred during image generation: {e}")
        print(f"Failed to convert: {latex_equation}")
        print("Please ensure your LaTeX equation is correctly formatted and enclosed in '$...$' or '$$...$$'.")
        print("Also, verify that a LaTeX distribution (like MiKTeX) is installed and in your system's PATH.")

def extract_equations_from_tex(file_path: str) -> list[str]:
    r"""
    Extracts LaTeX mathematical equations from a .tex file.
    It looks for inline math ($...$) and display math ($$...$$).

    Args:
        file_path (str): The path to the .tex file.

    Returns:
        list[str]: A list of extracted LaTeX equation strings,
                   each formatted as a raw string with dollar signs (e.g., r'$\int x dx$').
    """
    equations = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Regex for inline math: \$ (.*?)\$
        # Regex for display math: \$\$ (.*?)\$\$
        # The 're.DOTALL' flag allows '.' to match newlines
        # The 're.findall' returns all non-overlapping matches
        
        # Combine patterns to capture both inline and display math
        # It's important to be careful with nested dollar signs.
        # For simplicity, this regex looks for non-greedy matches to avoid
        # capturing across multiple equations if they are not well-separated.
        # A more robust solution for complex LaTeX parsing might involve a dedicated LaTeX parser library.
        
        # Pattern for $...$
        inline_pattern = r'\$(.*?)\$'
        # Pattern for $$...$$
        display_pattern = r'\$\$(.*?)\$\$'

        # Find all display math first to avoid capturing $$ as two $
        display_matches = re.findall(display_pattern, content, re.DOTALL)
        for match in display_matches:
            # Re-add $$ for the image conversion function
            equations.append(r'$$' + match + r'$$')
            # Remove the found display math from content to avoid re-matching parts of it as inline
            content = content.replace(r'$$' + match + r'$$', ' ') # Replace with space to preserve offsets if needed later

        # Find all inline math after display math has been handled
        inline_matches = re.findall(inline_pattern, content) # DOTALL not typically needed for inline if on same line
        for match in inline_matches:
            # Re-add $ for the image conversion function
            equations.append(r'$' + match + r'$')

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred while reading the LaTeX file: {e}")
    return equations


if __name__ == "__main__":
    print("Welcome to the LaTeX Math Equation to Image Converter!")
    print("-----------------------------------------------------")
    print("Choose your mode:")
    print(" (m) Enter equation manually")
    print(" (f) Process LaTeX file")
    print(" (e) Exit")
    print("-----------------------------------------------------")

    while True:
        mode = input("Enter your choice (m/f/e): ").lower().strip()

        if mode == 'e':
            break
        elif mode == 'm':
            print("\n--- Manual Equation Entry Mode ---")
            print("IMPORTANT: Your LaTeX input MUST be a raw string (r'...')")
            print("           AND enclosed in dollar signs for math mode ($...$ or $$...$$).")
            print(r"Example (Inline): r'$\alpha + \beta = \gamma$'")
            print(r"Example (Display): r'$$\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}$$'")
            print("-----------------------------------------------------")

            latex_input = input("Enter LaTeX equation: ")

            # Basic validation for raw string and math mode enclosure
            if not (latex_input.startswith("r'$") or latex_input.startswith("r'$$")):
                print("\nError: Your input must start with r'$' or r'$$' and contain valid math LaTeX.")
                print("Please re-enter your equation following the format guidelines.")
                continue

            output_name = input("Enter output filename (e.g., equation.png, press Enter for 'output_equation.png'): ")
            if not output_name:
                output_name = 'output_equation.png'

            try:
                dpi_input = input("Enter DPI for the image (default: 300): ")
                dpi = int(dpi_input) if dpi_input else 300
            except ValueError:
                print("Invalid DPI. Using default 300.")
                dpi = 300

            try:
                latex_equation_str = eval(latex_input) # Safely evaluate the input string
                latex_to_image(latex_equation_str, output_name, dpi)
            except SyntaxError:
                print("Error: Invalid Python string syntax. Make sure your raw string is correctly formatted (e.g., r'formula').")
            except Exception as e:
                print(f"An unexpected error occurred during processing: {e}")

        elif mode == 'f':
            print("\n--- Process LaTeX File Mode ---")
            file_path = input("Enter the full path to your LaTeX (.tex) file: ")

            try:
                dpi_input = input("Enter DPI for the images (default: 300): ")
                dpi = int(dpi_input) if dpi_input else 300
            except ValueError:
                print("Invalid DPI. Using default 300.")
                dpi = 300

            equations_to_process = extract_equations_from_tex(file_path)

            if not equations_to_process:
                print(f"No equations found in '{file_path}' or file could not be read. Please check the file path and content.")
                continue

            output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output_images")
            os.makedirs(output_dir, exist_ok=True) # Create output directory if it doesn't exist

            print(f"\nFound {len(equations_to_process)} equations. Converting to images in '{output_dir}'...")
            for i, equation_str in enumerate(equations_to_process):
                # Generate unique filename for each extracted equation
                output_filename = os.path.join(output_dir, f"equation_{i+1}.png")
                print(f"Converting equation {i+1}: {equation_str[:50]}... to {output_filename}") # Show snippet
                latex_to_image(equation_str, output_filename, dpi)

            print("\nFinished processing LaTeX file.")

        else:
            print("Invalid choice. Please enter 'm', 'f', or 'e'.")

    print("Thank you for using the LaTeX Math Equation to Image Converter!")
