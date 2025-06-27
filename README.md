# LaTeX Math to Image Converter

This project provides a simple Python script to convert LaTeX **mathematical equations only** into high-quality PNG images with a transparent background. It supports both manual input and automated extraction from `.tex` files.

## Table of Contents

* [Features](#features)
* [Prerequisites](#prerequisites)
* [Installation](#installation)
* [Usage](#usage)
* [Project Structure](#project-structure)
* [Contributing](#contributing)
* [License](#license)
* [Developed By](#developed-by)

## Features

* Convert single LaTeX math equations (inline or display) to PNG images.
* Automated extraction and conversion of all math equations from a `.tex` file.
* Output images have a transparent background.
* Configurable output resolution (DPI).
* `.gitignore` included for clean version control.

## Prerequisites

Before running this Python script, you need to ensure the following are installed on your Windows system:

1.  **Python 3**:
    * Download and install the latest version from [python.org](https://www.python.org/downloads/windows/).
    * **Important:** Make sure to check the "Add Python to PATH" option during installation.

2.  **MiKTeX (or TeX Live)**:
    * This is a LaTeX distribution essential for `matplotlib` to render LaTeX equations. MiKTeX is generally recommended for Windows users due to its ease of installation and "on-the-fly" package installation.
    * Download and install the Basic MiKTeX Installer from [miktex.org/download](https://miktex.org/download).
    * During installation, ensure `pdflatex` (a component of MiKTeX) is added to your system's PATH environment variable. This usually happens automatically.

## Installation

1.  **Clone the Repository (or download files):**
    If you're using Git, clone this repository to your local machine:
    ```bash
    git clone [https://github.com/dzmarkets/latex_math_to_image_converter.git](https://github.com/dzmarkets/latex_math_to_image_converter.git)
    cd latex_math_to_image_converter
    ```
    If not using Git, simply create a folder (e.g., `latex_math_to_image_converter`) and save the `main.py`, `requirements.txt`, and `.gitignore` files into it.

2.  **Install Python Dependencies:**
    Open your Command Prompt (or terminal), navigate to the `latex_math_to_image_converter` directory, and run the following command to install the required Python libraries:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Run the Script:**
    From your Command Prompt, while inside the `latex_math_to_image_converter` directory, execute the script:

    ```bash
    python main.py
    ```

2.  **Choose Mode:**
    The script will present you with options to either "Enter equation manually (m)" or "Process LaTeX file (f)".

    * **Manual Input (m):**
        * **Enter LaTeX Equation:** You must provide your input as a **raw Python string** (e.g., `r'...'`) **AND** it must be enclosed in dollar signs (`$`, `$$`) for `matplotlib` to render it as a mathematical expression.
            * **Example (Inline Math):** `r'$\alpha + \beta = \gamma$'`
            * **Example (Display Math):** `r'$$\sum_{i=1}^{n} i^2 = \frac{n(n+1)(2n+1)}{6}$$'`
        * **Specify Output Filename:** Enter a desired name for your output PNG image (e.g., `my_equation.png`). Press `Enter` to use the default `output_equation.png`.
        * **Specify DPI:** Enter the desired Dots Per Inch (DPI) for the image. Higher DPI means higher resolution. Press `Enter` to use the default `300`.

    * **Process LaTeX File (f):**
        * **Enter LaTeX file path:** Provide the **full path** to your `.tex` file (e.g., `C:\Users\YourUser\Documents\my_report.tex`).
        * The script will then automatically find all math equations within the specified `.tex` file and convert them into separate PNG images.
        * The images will be saved in an `output_images` subfolder, located within your project directory. Each image will be named based on its extraction order (e.g., `equation_1.png`, `equation_2.png`, etc.).
        * **Specify DPI:** Enter the desired Dots Per Inch (DPI) for all generated images. Press `Enter` to use the default `300`.

The generated images will be saved in the `output_images` subfolder (for file processing mode) or the same directory as your `main.py` script (for manual input mode).

## Project Structure

```
latex_math_to_image_converter/
├── main.py                 # Main script for conversion.
├── requirements.txt        # List of Python dependencies.
├── README.md               # Project documentation (this file).
└── .gitignore              # Specifies files/folders to ignore in Git.
└── output_images/          # (Created automatically when processing a LaTeX file)
    └── equation_1.png      # Generated math images.
    └── equation_2.png
    └── ...
```

## Contributing

Feel free to open issues or submit pull requests if you have suggestions for improvements or bug fixes.

## License

This project is open-source and available under the [MIT License](LICENSE). (Note: You would need to create a LICENSE file if you publish this to GitHub).

## Developed By

M. YOUCEF Yazid (yazid.youcef@gmail.com)
