# GTK3 Installation Guide for Windows (WeasyPrint)

WeasyPrint requires GTK3 libraries (Pango, Cairo, etc.) to render PDFs. On Windows, these are not installed automatically by pip. You must install them manually.

## Method 1: Easy Installer (Recommended for standard users)

This method renders most dependencies correctly without complex configuration.

1.  **Download the GTK3 Installer**:
    *   Go to: [https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases)
    *   Download the latest `.exe` file (e.g., `gtk3-runtime-3.24.31-2022-01-04-ts-win64.exe`).

2.  **Run the Installer**:
    *   Run the downloaded executable.
    *   **CRITICAL**: During installation, ensure the option **"Set up PATH environment variable"** is CHECKED. This allows WeasyPrint to find the libraries.

3.  **Verify**:
    *   Open a new command prompt (CMD or PowerShell).
    *   Run `python -m weasyprint --info`.
    *   If successful, you should see version information for libraries like Cairo and Pango, not error messages.

## Method 2: MSYS2 (Recommended for advanced users / developers) (Recommand)

If Method 1 fails or if you prefer a more robust dev environment (official WeasyPrint recommendation):

1.  **Install MSYS2**:
    *   Download from [https://www.msys2.org/](https://www.msys2.org/).

2.  **Install Dependencies**:
    *   Open the MSYS2 terminal (UCRT64 is recommended).
    *   Run: `pacman -S mingw-w64-x86_64-pango`

3.  **Link to Python**:
    *   Add the MSYS2 bin directory (e.g., `C:\msys64\mingw64\bin`) to your Windows User PATH environment variable.
    *   Restart your terminal/IDE.

## Troubleshooting

-   **"OSError: dlopen() failed to load a library: cairo..."**: This means the GTK3 DLLs are not in your PATH. Re-install or manually check your Environment Variables.
-   **"The specified module could not be found"**: Similar to above. Ensure you installed the **64-bit** version of GTK3 if your Python is 64-bit.
