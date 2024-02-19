import os
import re


def process_subtitle(subtitle_file):
    with open(subtitle_file, "r") as f:
        lines = f.readlines()

    entries = []
    for line in lines:
        # Extract timestamp and text
        if not re.match(r"\d+\n|(\d\d:\d\d:\d\d,\d\d\d --> \d\d:\d\d:\d\d,\d\d\d)", line):
            text = line.strip()  # Remove newline
            entries.append(text)
    return entries

def save_to_pdf(entries, output_file):
    """
    Saves the processed subtitle text entries to a PDF file with page breaks and adjusted font style.

    Args:
        entries (list): A list of strings containing the subtitle text for each entry.
        output_file (str): Path to the output PDF file.
    """

    from reportlab.pdfgen import canvas

    c = canvas.Canvas(output_file)

    # Set font and style
    c.setFont("Helvetica", 12)

    # Set starting y coordinate and line height
    y = 750
    line_height = 15

    # Track total height used and add page breaks as needed
    total_height = 0
    page_height = 700  # Adjust as needed

    for entry in entries:
        # Check if new page needed
        if total_height + line_height > page_height:
            c.showPage()  # Add a new page
            y = 750
            total_height = 0

        # Adjust y coordinate and write entry
        y -= line_height
        c.drawString(
            20, y, entry
        )  # Write only the text, as timestamps are not included

        # Update total height used
        total_height += line_height

    c.save()


if __name__ == "__main__":
    # Replace these with your actual file paths
    subtitle_folder = "path/to/your/subtitle/folder"
    output_folder = "path/to/output/folder"

    for filename in os.listdir(subtitle_folder):
        # Replace startswith(filename)
        if filename.startswith("Rust for the") and filename.endswith(".srt"):
            subtitle_file = os.path.join(subtitle_folder, filename)
            entries = process_subtitle(subtitle_file)
            output_file = os.path.join(
                output_folder, os.path.splitext(filename)[0] + ".pdf"
            )
            save_to_pdf(entries, output_file)
            print(f"Subtitle saved as PDF: {output_file}")
