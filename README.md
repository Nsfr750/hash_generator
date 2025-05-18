# Password Hash Generator

[![GitHub license](https://img.shields.io/github/license/Nsfr750/password-hash-generator)](https://github.com/Nsfr750/password-hash-generator/blob/master/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/Nsfr750/password-hash-generator)](https://github.com/Nsfr750/password-hash-generator/issues)
[![GitHub stars](https://img.shields.io/github/stars/Nsfr750/password-hash-generator)](https://github.com/Nsfr750/password-hash-generator/stargazers)

A secure and user-friendly GUI application for generating password hashes using PBKDF2 with SHA256.

## Features

- 🔐 Secure Password Hashing
  - PBKDF2 with SHA256 algorithm
  - Configurable iterations (1000-1000000)
  - Random salt generation
  - Constant-time string comparison

- 📝 User Interface
  - Clean and intuitive GUI
  - Secure password input field
  - Copy to clipboard functionality
  - Reset functionality
  - About dialog with version info
  - Sponsor dialog with support links

- 🛡️ Security Features
  - Secure password handling
  - Constant-time string comparison
  - Random salt generation
  - Configurable iterations for security
  - Secure hash storage format

## Usage

1. Launch the application:
   ```bash
   python main.py
   ```

2. Enter your password in the secure input field
3. Set desired number of iterations (1000-1000000)
4. Click "Generate Hash" to create the hash
5. The hash will be displayed in the format: `SHA256:iterations:salt:hash`
6. Use "Copy" button to copy the hash to clipboard
7. Use "Reset" button to clear all fields
8. Access additional features:
   - "About" dialog from Help menu for version info
   - "Sponsor" dialog from Help menu to support the project

## Hash Format

The generated hash follows this format:
```
SHA256:iterations:salt:hash
```
Where:
- `SHA256`: The hashing algorithm used
- `iterations`: Number of PBKDF2 iterations
- `salt`: Base64-encoded random salt
- `hash`: Base64-encoded final hash

## Requirements

- Python 3.6+
- tkinter (included with Python)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Nsfr750/password-hash-generator.git
   cd password-hash-generator
   ```

2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Support

- Report bugs at [GitHub Issues](https://github.com/Nsfr750/password-hash-generator/issues)
- Support the project through [GitHub Sponsors](https://github.com/sponsors/Nsfr750)
- Join the discussion on [GitHub Discussions](https://github.com/Nsfr750/password-hash-generator/discussions)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

- Thanks to all contributors and users
- Inspired by secure password hashing practices
- Built with Python and tkinter
