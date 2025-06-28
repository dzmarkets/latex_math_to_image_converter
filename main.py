# Path: latex_math_to_image_converter/main.py
# Description: Main script to convert LaTeX mathematical equations to images (no surrounding text),
#              now with an option to process equations directly from a .tex file
#              and replace them with images in a new .tex file.
# Developed by: M. YOUCEF Yazid (yazid.youcef@gmail.com)
# File Version: 2.2.0
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

        # The background will be transparent when saved with transparent=True
        
        # Add an axes object that covers the entire figure.
        ax = fig.add_axes([0, 0, 1, 1])

        # Render the LaTeX equation. Matplotlib interprets strings enclosed in $ or $$ as math.
        # The text is centered horizontally and vertically on the axes.
        ax.text(0.5, 0.5, latex_equation,
                fontsize=20,          # Font size of the equation.
                color='black',        # Color of the equation text for better visibility on a transparent background.
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
        print(f"An error occurred during image generation for '{latex_equation}': {e}")
        print("Please ensure your LaTeX equation is correctly formatted and enclosed in '$...$' or '$$...$$'.")
        print("Also, verify that a LaTeX distribution (like MiKTeX) is installed and in your system's PATH.")
        # Re-raise the exception or return a status to indicate failure if crucial for replacement logic
        raise # Re-raise to be caught by calling function for replacement logic


def extract_equations_with_spans(file_path: str) -> list[tuple[int, int, str, bool]]:
    # Extracts LaTeX mathematical equations from a .tex file,
    # including their start and end character indices.
    # It looks for inline math ($...$) and display math ($$...$$).
    # Handles potential escaped dollar signs like \$ which should not be matched.
    # Args:
    #     file_path (str): The path to the .tex file.
    # Returns:
    #     list[tuple[int, int, str, bool]]: List of (start_idx, end_idx, original_equation_str, is_display_math)
    #                                       where original_equation_str includes the delimiters ($ or $$).
    equations_data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Regex for inline math $...$
        # (?<!\\)\$: Matches '$' only if it's not preceded by a backslash (i.e., not escaped)
        # (.*?): Non-greedy match for any characters (the equation content)
        inline_pattern = r'(?<!\\)\$((?:(?!\$).)*?)(?<!\\)\$'
        
        # Regex for display math $$...$$
        # Prioritize matching $$ to avoid capturing them as two separate $
        display_pattern = r'(?<!\\)\$\$((?:(?!\$\$).)*?)(?<!\\)\$\$'

        # Find all display math matches first
        for match in re.finditer(display_pattern, content, re.DOTALL):
            # match.start(0) and match.end(0) give the span of the *entire* match ($$...$$)
            # match.group(1) gives the content *between* the delimiters
            equations_data.append((match.start(0), match.end(0), match.group(0), True))

        # Find all inline math matches (after display math might have been 'logically' removed/handled)
        # To avoid issues with re.finditer on modified content, it's better to collect all spans
        # and then process them. The replace logic handles content modification based on spans.
        for match in re.finditer(inline_pattern, content, re.DOTALL):
            # Check if this inline match is part of an already captured display math block
            # This is a simple overlap check; for truly robust parsing, a dedicated LaTeX parser is needed.
            is_overlap = False
            for disp_start, disp_end, _, _ in equations_data:
                if (match.start(0) >= disp_start and match.end(0) <= disp_end):
                    is_overlap = True
                    break
            if not is_overlap:
                equations_data.append((match.start(0), match.end(0), match.group(0), False))

        # Sort equations by their start index in the file
        equations_data.sort(key=lambda x: x[0])

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred while reading or parsing the LaTeX file: {e}")
    return equations_data


def add_graphicx_package(content: str) -> str:
    # Adds \usepackage{graphicx} to the LaTeX preamble if not already present.
    # This function is now called only for the final generated .tex file.
    if r'\usepackage{graphicx}' not in content:
        # Find a suitable place to insert, e.g., after \documentclass or before \begin{document}
        # This regex is more specific to place it after the main documentclass.
        match = re.search(r'(\\documentclass\{.*?\}.*?)(\\begin\{document\})', content, re.DOTALL)
        if match:
            # Insert after documentclass section, before begin{document}
            return match.group(1) + '\n\\usepackage{graphicx}' + match.group(2) + content[match.end(2):]
        else:
            # Fallback: just prepend it if no documentclass/begin{document} found.
            # This might happen for simple .tex snippets, but for full documents, the above is better.
            return '\\usepackage{graphicx}\n' + content
    return content

if __name__ == "__main__":
    print("Welcome to the LaTeX Math Equation to Image Converter!")
    print("-----------------------------------------------------")
    print("Choose your mode:")
    print(" (m) Enter equation manually")
    print(" (f) Process LaTeX file")
    print(" (e) Exit")
    print("-----------------------------------------------------")

    # Define the example raw strings once
    example_inline_latex = r'$\alpha + \beta = \gamma$'
    example_display_latex = r'$$\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}$$'

    while True:
        mode = input("Enter your choice (m/f/e): ").lower().strip()

        if mode == 'e':
            break
        elif mode == 'm':
            print("\n--- Manual Equation Entry Mode ---")
            print("IMPORTANT: Your LaTeX input MUST be a raw string (r'...')")
            print("           AND enclosed in dollar signs for math mode ($...$ or $$...$$).")
            # Use repr() to correctly display the raw string literal to the user
            print(f"Example (Inline): {repr(example_inline_latex)}")
            print(f"Example (Display): {repr(example_display_latex)}")
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
            
            sub_mode = input("Choose sub-mode: (i) Images only or (r) Replace in new .tex file: ").lower().strip()

            if sub_mode not in ['i', 'r']:
                print("Invalid sub-mode choice. Please enter 'i' or 'r'.")
                continue

            equations_data = extract_equations_with_spans(file_path)

            if not equations_data:
                print(f"No equations found in '{file_path}' or file could not be read. Please check the file path and content.")
                continue

            output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output_images")
            os.makedirs(output_dir, exist_ok=True) # Create output directory if it doesn't exist

            original_content = ""
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    original_content = f.read()
            except Exception as e:
                print(f"Error reading original LaTeX file: {e}")
                continue

            # This variable must be initialized before the loop
            replacements_made = 0 

            # Get the base name of the LaTeX file (e.g., 'my_document' from 'my_document.tex')
            tex_file_base_name = os.path.splitext(os.path.basename(file_path))[0]

            # Keep track of replacements in reverse order of character index
            replacements_for_content = [] 

            # First, process equations and gather replacement details
            for i, (start_idx, end_idx, original_equation_str, is_display_math) in enumerate(equations_data): # Iterate in natural order for image generation
                # New naming convention: include original .tex file name
                image_filename = f"{tex_file_base_name}_equation_{i+1}.png" 
                output_image_path = os.path.join(output_dir, image_filename)
                
                try:
                    # The equation string passed to latex_to_image must include the delimiters
                    latex_to_image(original_equation_str, output_image_path, dpi)
                    
                    if sub_mode == 'r':
                        # Construct \includegraphics command.
                        # Use os.path.basename(output_image_path) for \includegraphics as images are in the same dir as new .tex
                        image_include_command = f"\\includegraphics{{{os.path.basename(output_image_path)}}}"
                        
                        if is_display_math:
                            # Use \centering for display math within a paragraph, or a figure env for more control.
                            # For simplicity, let's replace $$...$$ with just the image include, possibly centered.
                            replacement_text = f"\n\\begin{{center}}\n{image_include_command}\n\\end{{center}}\n"
                        else:
                            # For inline images, reduce width to fit text better and adjust vertical alignment
                            # Setting width to a fraction of \linewidth to avoid Overfull \hbox
                            # The scale factor (e.g., 0.15) might need manual adjustment based on actual font size and image size.
                            replacement_text = f"\\raisebox{{-0.2\\height}}{{\\includegraphics[width=0.15\\linewidth]{{{os.path.basename(output_image_path)}}}}}"

                        replacements_for_content.append((start_idx, end_idx, replacement_text))

                except Exception as e:
                    print(f"Skipping image generation for '{original_equation_str}' due to error: {e}")
            
            if sub_mode == 'r':
                # Apply replacements in reverse order to avoid index shifts
                # Convert original_content to a mutable list of characters for efficient replacement
                final_chars = list(original_content)
                replacements_for_content.sort(key=lambda x: x[0], reverse=True) # Sort by start_idx in reverse

                for start_idx, end_idx, replacement_text in replacements_for_content:
                    final_chars[start_idx:end_idx] = list(replacement_text)
                    replacements_made += 1 # This increment happens within the loop for replacements_for_content

                final_content = "".join(final_chars)

                # Now handle \input and \include, and replace them.
                # Find all \input{file} and \include{file} commands
                # We need to correctly handle the case where the input file might contain equations
                # The current `extract_equations_with_spans` only processes the top-level file.
                # If the goal is a fully self-contained LaTeX file with images,
                # the user needs to provide a single .tex file that inputs/includes others,
                # or run the script on each sub-file separately.
                # For this version, we will only replace images in the top-level file.
                # If input/include commands exist, they will remain as is, pointing to the original files.
                # A more complex solution would recursively process included files.

                final_content = add_graphicx_package(final_content) # Ensure graphicx package is included in the new file

                original_base_name = os.path.splitext(os.path.basename(file_path))[0]
                output_tex_filename = os.path.join(output_dir, f"{original_base_name}_with_images.tex")

                try:
                    with open(output_tex_filename, 'w', encoding='utf-8') as f:
                        f.write(final_content)
                    print(f"\nSuccessfully generated new LaTeX file with images: {output_tex_filename}")
                    print(f"Total equations replaced: {replacements_made}")
                    print("IMPORTANT: If your original LaTeX file used '\\input' or '\\include' for other files,")
                    print("           those will remain as references. You might need to manually compile")
                    print("           the new .tex file and its dependencies, or modify your original project structure.")
                    print("           Also, delete all .aux, .toc, .log files before recompiling the new .tex.")
                except Exception as e:
                    print(f"Error writing new LaTeX file: {e}")
            else:
                print(f"\nFinished converting equations to images from '{file_path}'. Images saved in '{output_dir}'.")
        else:
            print("Invalid choice. Please enter 'm', 'f', or 'e'.")

    print("Thank you for using the LaTeX Math Equation to Image Converter!")
