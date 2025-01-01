# 🎬 Film Management App 

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![tkinter](https://img.shields.io/badge/tkinter-included-green.svg)](https://docs.python.org/3/library/tkinter.html)

A beautiful and user-friendly desktop application for managing your personal film collection! Keep track of movies you've watched, rate them, and organize your watching experience. 🍿

## ✨ Features

- 📝 Add new films with detailed information
- 🔍 Filter films by various criteria
- ⭐ Rate films from 0 to 5 stars
- 📊 Track watching status
- ✏️ Edit existing entries
- 🗑️ Delete unwanted entries
- 💾 Persistent storage using JSON

## 🛠️ Prerequisites

- Python 3.7 or higher
- Required Python packages:
  - tkinter (usually comes with Python)
  - Pillow (PIL)
  - pathlib

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/film-management-app.git
cd film-management-app
```

2. Install required packages:
```bash
pip install Pillow
```

3. Run the application:
```bash
python InitialApp.py
```

## 🎯 Usage

### Main Menu
- Start: Add a new film to your collection
- List: View and manage your existing films

### Adding a Film
1. Click "Start" on the main menu
2. Fill in the following details:
   - Name of the film
   - Type (Action, Comedy, Drama, Horror, Sci-Fi)
   - Status (Watched/Not Watched)
   - Star Rating (0-5)
   - Notes

### Managing Films
- 🔍 **Filter**: Search through your collection using any criteria
- ✏️ **Edit**: Modify details of existing entries
- 🗑️ **Delete**: Remove films from your collection
- 🔄 **Back**: Return to main menu

## 🎨 Interface

The app features a modern, dark-themed interface with:
- Responsive design
- Easy-to-use navigation
- Clear visual hierarchy
- Comfortable color scheme

## 💾 Data Storage

All film data is stored locally in a `films.json` file, making it easy to backup and transfer your collection.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with Python and tkinter
- Uses the beautiful Nord color theme
- Icons and assets included in the assets folder

## 🐛 Troubleshooting

If you encounter any issues:
1. Ensure all required packages are installed
2. Check if `films.json` has write permissions
3. Verify that all assets are in the correct directory structure

## 📫 Contact

For any questions or suggestions, please open an issue in the repository.

---
Made with ❤️ for film enthusiasts
