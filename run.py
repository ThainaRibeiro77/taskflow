"""Ponto de entrada para rodar o TaskFlow localmente.

Uso:
    python run.py
Depois acesse http://127.0.0.1:5000
"""

from src import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
