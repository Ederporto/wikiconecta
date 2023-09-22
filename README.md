# WikiConecta

WikiConecta is a open course in [Wikiversity in Portuguese](https://pt.wikiversity.org/wiki/WikiConecta). This is a Django web application for managing the
certificates for the participants of the course, available in Toolforge at https://wikiconecta.toolforge.org 

## Table of Contents

- [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
- [Contributing](#contributing)
- [License](#license)

## Getting Started

### Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3
- Django 4.2.5
- FPDF 1.7.2

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/WikiMovimentoBrasil/wikiconecta.git

2. Navigate to the project directory:

   ```bash
   cd wikiconecta

3. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv

4. Activate the virtual environment:
    * On Windows:
   ```bash
   venv\Scripts\activate
   ```
    * On macOS and Linux:
   ```bash
   source venv/bin/activate

5. Install project dependencies:
   ```bash
   pip install -r requirements.txt

6. Create the database and apply migrations:
   ```bash
   python manage.py migrate

7. Start the development server:
   ```bash
    python manage.py runserver

You should now be able to access the project at http://localhost:8000/ in your web browser.

## Contributing
Contributions are welcome! To contribute to Wikiconecta, follow these steps:

1. Fork the repository
2. Create a new branch: git checkout -b feature/your-feature
3. Make your changes and commit them: git commit -m 'Add some feature'
4. Push to the branch: git push origin feature/your-feature
5. Create a pull request on GitHub 

## License
This project is licensed under the [MIT License](https://opensource.org/license/mit) - see the LICENSE file for details.
