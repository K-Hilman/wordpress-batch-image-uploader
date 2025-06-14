# WordPress Batch Image Uploader

## Description
The WordPress Batch Image Uploader is a Python application that facilitates the upload of multiple image files to a WordPress site via its REST API. This tool allows users to upload images in batches, automatically checking for duplicates and generating a report of the upload status for each image. It features a simple and intuitive graphical user interface created using Tkinter.

Sometimes, using WordPress's native bulk uploader can overwhelm the server, potentially causing outages. This tool provides a more controlled approach by processing uploads in manageable batches. WordPress treats each upload as a standard file submission, ensuring images are properly compressed and stored according to WordPress’s default structure. This method minimizes server strain while maintaining seamless integration with your media library

## Installation and Setup

### Prerequisites
- Python 3.x
- Tkinter (usually comes pre-installed with Python)
- `requests` package

### Dependencies
You need the `requests` library to run this project. Install it using pip:

```bash
pip install requests
```

### Configuration
Before running the project, please configure the following parameters in the code:
- `WP_SITE_URL`: Your WordPress site's URL.
- `USERNAME`: Your WordPress username.
- `APP_PASSWORD`: Your WordPress application password (can be generated within WordPress admin settings).

### Running the Project
1. Clone this repository (if applicable) or copy the script into a Python environment of your choice.
2. Open the script in your code editor and modify the configuration section as described above.
3. Run the script using Python:

```bash
python main.py
```

## Usage Guidelines
1. When the GUI launches, click the "Select Images" button to browse your file system.
2. Select the image files you want to upload (supports: jpg, jpeg, png, gif, webp, bmp, tiff).
3. The progress of the uploads will be displayed through the progress bar, along with the status of each image in the main window.
4. A CSV report will be generated after the upload is complete, detailing the upload status of each image.

## Features
- Batch upload of images to a WordPress site.
- Automatic detection of duplicate images to avoid unnecessary uploads.
- Status reporting for each image upload, including successes and failures.
- Graphical user interface for ease of use.
- Adjustable parameters for batch size and sleep duration between batches.

## Configuration Options
- `BATCH_SIZE`: The number of images to upload in a single batch (default is 50).
- `SLEEP_BETWEEN_BATCHES`: The duration (in seconds) to wait between processing batches (default is 5 seconds).
- `REPORT_FILE`: The name of the CSV file that will store the upload results (default is `upload_report.csv`).

## Code Structure
- **Main Script**: Contains all the functionality to upload images and manage the GUI.
- **Functions**: Includes key functions such as `image_exists`, `upload_image`, and `upload_images` to manage the upload process and handle statuses.
- **GUI Setup**: Builds the user interface using Tkinter components such as frames, buttons, and labels.

## Contribution Guidelines
Contributions are welcome! If you'd like to contribute to this project, please follow these steps:
1. Fork the repository.
2. Create a new branch (e.g., `feature/your-feature`).
3. Make your changes and commit them with clear commit messages.
4. Push your branch and create a pull request.

Please ensure that your contributions follow best coding practices and maintain the readability of the code.

## License Information

This project is licensed under the MIT License - see the LICENSE file for details.